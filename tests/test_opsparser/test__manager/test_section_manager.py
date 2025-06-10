"""
Tests for SectionManager and SectionHandler

This module tests the SectionManager and SectionHandler classes which handle
OpenSeesPy section commands for all supported section types, including
comprehensive testing of fiber sections with patch, layer, and fiber commands.
"""

import pytest
from typing import Dict, Any

from opsparser._manager._SectionManager import SectionManager, SectionHandler
import openseespy.opensees as ops


@pytest.fixture
def section_manager_2d() -> SectionManager:
    """每个测试前初始化一个SectionManager实例"""
    ops.wipe()
    ops.model('basic', '-ndm', 2, '-ndf', 3)
    manager = SectionManager()
    manager.clear()
    return manager

@pytest.fixture
def section_manager_3d() -> SectionManager:
    """每个测试前初始化一个SectionManager实例"""
    ops.wipe()
    ops.model('basic', '-ndm', 3, '-ndf', 6)
    manager = SectionManager()
    manager.clear()
    return manager

@pytest.fixture
def configured_section_manager_2d() -> SectionManager:
    """每个测试前初始化一个配置好的SectionManager实例"""
    ops.wipe()
    ops.model('basic', '-ndm', 2, '-ndf', 3)
    manager = SectionManager()
    manager.clear()
    
    # 添加一些默认截面
    arg_map1 = {"args": ["Elastic", 1, 29000, 100, 10], "kwargs": {}}
    arg_map2 = {"args": ["Fiber", 2, "-GJ", 100], "kwargs": {}}
    arg_map3 = {"args": ["Elastic", 3, 30000, 120, 12], "kwargs": {}}
    
    manager.handle("section", arg_map1)
    manager.handle("section", arg_map2)
    manager.handle("section", arg_map3)
    
    return manager

@pytest.fixture
def configured_section_manager_3d() -> SectionManager:
    """每个测试前初始化一个配置好的SectionManager实例"""
    ops.wipe()
    ops.model('basic', '-ndm', 3, '-ndf', 6)
    manager = SectionManager()
    manager.clear()
    
    # 添加一些默认截面
    arg_map1 = {"args": ["Elastic", 1, 29000, 100, 10,5,1000,1e6,0.001,0.001], "kwargs": {}}
    arg_map2 = {"args": ["Fiber", 2, "-GJ", 100], "kwargs": {}}
    arg_map3 = {"args": ["Elastic", 3, 30000, 120, 12,5,1000,1e6,0.001,0.001], "kwargs": {}}
    
    manager.handle("section", arg_map1)
    manager.handle("section", arg_map2)
    manager.handle("section", arg_map3)
    return manager


class TestSectionManager:
    """测试SectionManager基本功能"""
    
    def test_handles(self, section_manager_2d: SectionManager, section_manager_3d: SectionManager):
        """测试SectionManager处理的命令"""
        expected_commands = ["section", "fiber", "patch", "layer"]
        assert set(section_manager_2d.handles()) == set(expected_commands)
        assert set(section_manager_3d.handles()) == set(expected_commands)

    def test_basic_section_creation(self, section_manager_2d: SectionManager):
        """测试基本截面创建"""
        # 测试弹性截面
        arg_map = {"args": ["Elastic", 1, 29000, 100, 10], "kwargs": {}}
        section_manager_2d.handle("section", arg_map)
        
        section = section_manager_2d.get_section(1)
        assert section is not None
        assert section["secType"] == "Elastic"
        assert section["secTag"] == 1

    def test_basic_section_creation_3d(self, section_manager_3d: SectionManager):
        """测试基本截面创建"""
        # 测试弹性截面
        arg_map = {"args": ["Elastic", 1, 29000, 100, 10,5,1000,1e6,0.001,0.001], "kwargs": {}}
        section_manager_3d.handle("section", arg_map)
        
        section = section_manager_3d.get_section(1)
        assert section is not None
        assert section["secType"] == "Elastic"
        assert section["secTag"] == 1

    def test_get_section_methods(self, configured_section_manager_2d: SectionManager):
        """测试获取截面的各种方法"""
        # 测试get_section_tags
        tags = configured_section_manager_2d.get_section_tags()
        assert set(tags) == {1, 2, 3}
        
        # 测试get_sections_by_type
        elastic_sections = configured_section_manager_2d.get_sections_by_type("Elastic")
        assert len(elastic_sections) == 2
        
        fiber_sections = configured_section_manager_2d.get_sections_by_type("Fiber")
        assert len(fiber_sections) == 1

    def test_clear(self, section_manager_2d: SectionManager):
        """测试清除截面数据"""
        # 添加截面
        arg_map = {"args": ["Elastic", 1, 29000, 100, 10], "kwargs": {}}
        section_manager_2d.handle("section", arg_map)
        
        assert len(section_manager_2d.sections) == 1
        section_manager_2d.clear()
        assert len(section_manager_2d.sections) == 0
        assert section_manager_2d.current_section is None


class TestFiberSectionWithComponents:
    """测试纤维截面及其组件（patch、layer、fiber）"""
    
    def test_fiber_section_creation(self, section_manager_2d: SectionManager):
        """测试纤维截面创建"""
        arg_map = {"args": ["Fiber", 991, "-GJ", 1e10], "kwargs": {}}
        section_manager_2d.handle("section", arg_map)
        
        section = section_manager_2d.get_section(991)
        assert section["secType"] == "Fiber"
        assert section["secTag"] == 991
        assert section["GJ"] == 1e10
        assert "fibers" in section
        assert "patches" in section
        assert "layers" in section
        assert section_manager_2d.current_section == 991

    def test_patch_rect_creation(self, section_manager_2d: SectionManager):
        """测试矩形patch创建"""
        # 首先创建纤维截面
        section_arg = {"args": ["Fiber", 991, "-GJ", 1e10], "kwargs": {}}
        section_manager_2d.handle("section", section_arg)
        
        # 添加矩形patch
        patch_arg = {"args": ["rect", 1, 10, 1, -0.92, -0.42, 0.92, 0.42], "kwargs": {}}
        section_manager_2d.handle("patch", patch_arg)
        
        section = section_manager_2d.get_section(991)
        patches = section["patches"]
        assert len(patches) == 1
        
        patch = patches[0]
        assert patch["type"] == "rect"
        assert patch["matTag"] == 1
        assert patch["numSubdivY"] == 10
        assert patch["numSubdivZ"] == 1
        assert patch["crdsI"] == [-0.92, -0.42]
        assert patch["crdsJ"] == [0.92, 0.42]

    def test_patch_quad_creation(self, section_manager_2d: SectionManager):
        """测试四边形patch创建"""
        # 首先创建纤维截面
        section_arg = {"args": ["Fiber", 992], "kwargs": {}}
        section_manager_2d.handle("section", section_arg)
        
        # 添加四边形patch
        patch_arg = {"args": ["quad", 2, 8, 4, 
                             -1.0, -0.5, 1.0, -0.5, 
                             1.0, 0.5, -1.0, 0.5], "kwargs": {}}
        section_manager_2d.handle("patch", patch_arg)
        
        section = section_manager_2d.get_section(992)
        patches = section["patches"]
        assert len(patches) == 1
        
        patch = patches[0]
        assert patch["type"] == "quad"
        assert patch["matTag"] == 2
        assert patch["numSubdivIJ"] == 8
        assert patch["numSubdivJK"] == 4

    def test_patch_circ_creation(self, section_manager_2d: SectionManager):
        """测试圆形patch创建"""
        # 首先创建纤维截面
        section_arg = {"args": ["Fiber", 993], "kwargs": {}}
        section_manager_2d.handle("section", section_arg)
        
        # 添加圆形patch
        patch_arg = {"args": ["circ", 3, 16, 8, 0.0, 0.0, 0.0, 0.5, 0.0, 360.0], "kwargs": {}}
        section_manager_2d.handle("patch", patch_arg)
        
        section = section_manager_2d.get_section(993)
        patches = section["patches"]
        assert len(patches) == 1
        
        patch = patches[0]
        assert patch["type"] == "circ"
        assert patch["matTag"] == 3
        assert patch["numSubdivCirc"] == 16
        assert patch["numSubdivRad"] == 8

    def test_layer_straight_creation(self, section_manager_2d: SectionManager):
        """测试直线layer创建"""
        # 首先创建纤维截面
        section_arg = {"args": ["Fiber", 994], "kwargs": {}}
        section_manager_2d.handle("section", section_arg)
        
        # 添加直线layer
        layer_arg = {"args": ["straight", 3, 3, 0.02, 0.92, 0.42, 0.92, -0.42], "kwargs": {}}
        section_manager_2d.handle("layer", layer_arg)
        
        section = section_manager_2d.get_section(994)
        layers = section["layers"]
        assert len(layers) == 1
        
        layer = layers[0]
        assert layer["type"] == "straight"
        assert layer["matTag"] == 3
        assert layer["numFiber"] == 3
        assert layer["areaFiber"] == 0.02
        assert layer["start"] == [0.92, 0.42]
        assert layer["end"] == [0.92, -0.42]

    def test_layer_circ_creation(self, section_manager_2d: SectionManager):
        """测试圆形layer创建"""
        # 首先创建纤维截面
        section_arg = {"args": ["Fiber", 995], "kwargs": {}}
        section_manager_2d.handle("section", section_arg)
        
        # 添加圆形layer
        layer_arg = {"args": ["circ", 4, 20, 0.01, 0.0, 0.0, 0.4, 0.0, 360.0], "kwargs": {}}
        section_manager_2d.handle("layer", layer_arg)
        
        section = section_manager_2d.get_section(995)
        layers = section["layers"]
        assert len(layers) == 1
        
        layer = layers[0]
        assert layer["type"] == "circ"
        assert layer["matTag"] == 4
        assert layer["numFiber"] == 20
        assert layer["areaFiber"] == 0.01
        assert layer["center"] == [0.0, 0.0]
        assert layer["radius"] == 0.4

    def test_layer_rect_creation(self, section_manager_2d: SectionManager):
        """测试矩形layer创建"""
        # 首先创建纤维截面
        section_arg = {"args": ["Fiber", 996], "kwargs": {}}
        section_manager_2d.handle("section", section_arg)
        
        # 添加矩形layer
        layer_arg = {"args": ["rect", 5, 5, 3, 0.005, 0.0, 0.0, 0.8, 0.6], "kwargs": {}}
        section_manager_2d.handle("layer", layer_arg)
        
        section = section_manager_2d.get_section(996)
        layers = section["layers"]
        assert len(layers) == 1
        
        layer = layers[0]
        assert layer["type"] == "rect"
        assert layer["matTag"] == 5
        assert layer["numFiberY"] == 5
        assert layer["numFiberZ"] == 3
        assert layer["areaFiber"] == 0.005

    def test_fiber_creation(self, section_manager_2d: SectionManager):
        """测试单个纤维创建"""
        # 首先创建纤维截面
        section_arg = {"args": ["Fiber", 997], "kwargs": {}}
        section_manager_2d.handle("section", section_arg)
        
        # 添加单个纤维
        fiber_arg = {"args": [0.5, 0.3, 0.1, 2], "kwargs": {}}
        section_manager_2d.handle("fiber", fiber_arg)
        
        section = section_manager_2d.get_section(997)
        fibers = section["fibers"]
        assert len(fibers) == 1
        
        fiber = fibers[0]
        assert fiber["yloc"] == 0.5
        assert fiber["zloc"] == 0.3
        assert fiber["A"] == 0.1
        assert fiber["matTag"] == 2

    def test_complex_pier_section_like_example(self, section_manager_3d: SectionManager):
        """测试复杂的墩柱截面定义（类似用户示例）"""
        # 墩柱尺寸参数
        colWidth, colDepth = 1, 2
        cover = 0.08
        As = 0.02
        y1, z1 = colDepth / 2.0, colWidth / 2.0
        
        # 1. 创建纤维截面
        section_arg = {"args": ["Fiber", 991, "-GJ", 1e10], "kwargs": {}}
        section_manager_3d.handle("section", section_arg)
        
        # 2. 创建混凝土核心纤维
        core_patch_arg = {"args": ["rect", 1, 10, 1, 
                                  cover - y1, cover - z1, 
                                  y1 - cover, z1 - cover], "kwargs": {}}
        section_manager_3d.handle("patch", core_patch_arg)
        
        # 3. 创建混凝土保护层纤维（顶部、底部、左侧、右侧）
        patches_args = [
            # 顶部
            {"args": ["rect", 2, 10, 1, -y1, z1 - cover, y1, z1], "kwargs": {}},
            # 底部
            {"args": ["rect", 2, 10, 1, -y1, -z1, y1, cover - z1], "kwargs": {}},
            # 左侧
            {"args": ["rect", 2, 2, 1, -y1, cover - z1, cover - y1, z1 - cover], "kwargs": {}},
            # 右侧
            {"args": ["rect", 2, 2, 1, y1 - cover, cover - z1, y1, z1 - cover], "kwargs": {}}
        ]
        
        for patch_arg in patches_args:
            section_manager_3d.handle("patch", patch_arg)
        
        # 4. 创建钢筋纤维（右侧、中间、左侧）
        layers_args = [
            # 右侧
            {"args": ["straight", 3, 3, As, y1 - cover, z1 - cover, y1 - cover, cover - z1], "kwargs": {}},
            # 中间
            {"args": ["straight", 3, 2, As, 0.0, z1 - cover, 0.0, cover - z1], "kwargs": {}},
            # 左侧
            {"args": ["straight", 3, 3, As, cover - y1, z1 - cover, cover - y1, cover - z1], "kwargs": {}}
        ]
        
        for layer_arg in layers_args:
            section_manager_3d.handle("layer", layer_arg)
        
        # 5. 验证截面数据
        section = section_manager_3d.get_section(991)
        assert section["secType"] == "Fiber"
        assert section["secTag"] == 991
        assert section["GJ"] == 1e10
        
        # 验证patches（1个核心 + 4个保护层）
        patches = section["patches"]
        assert len(patches) == 5
        
        # 验证核心patch
        core_patch = patches[0]
        assert core_patch["type"] == "rect"
        assert core_patch["matTag"] == 1
        
        # 验证保护层patches
        cover_patches = patches[1:5]
        for patch in cover_patches:
            assert patch["type"] == "rect"
            assert patch["matTag"] == 2
        
        # 验证layers（3个钢筋层）
        layers = section["layers"]
        assert len(layers) == 3
        
        for layer in layers:
            assert layer["type"] == "straight"
            assert layer["matTag"] == 3
            assert layer["areaFiber"] == As
        
        # 验证钢筋数量
        assert layers[0]["numFiber"] == 3  # 右侧
        assert layers[1]["numFiber"] == 2  # 中间
        assert layers[2]["numFiber"] == 3  # 左侧

    def test_aggregator_section_with_fiber_section(self, section_manager_3d: SectionManager):
        """测试聚合截面与纤维截面结合"""
        # 1. 创建纤维截面
        fiber_section_arg = {"args": ["Fiber", 991, "-GJ", 1e10], "kwargs": {}}
        section_manager_3d.handle("section", fiber_section_arg)
        
        # 2. 创建聚合截面
        aggregator_arg = {"args": ["Aggregator", 1, 103, "T", "-section", 991], "kwargs": {}}
        section_manager_3d.handle("section", aggregator_arg)
        
        # 验证聚合截面
        aggregator_section = section_manager_3d.get_section(1)
        assert aggregator_section["secType"] == "Aggregator"
        assert aggregator_section["secTag"] == 1
        assert aggregator_section["mats"] == [103, "T"]
        assert aggregator_section["sectionTag"] == 991

    def test_get_fibers_patches_layers_methods(self, section_manager_2d: SectionManager):
        """测试获取纤维、patch、layer的方法"""
        # 创建纤维截面并添加组件
        section_arg = {"args": ["Fiber", 998], "kwargs": {}}
        section_manager_2d.handle("section", section_arg)
        
        # 添加fiber
        fiber_arg = {"args": [0.1, 0.2, 0.05, 1], "kwargs": {}}
        section_manager_2d.handle("fiber", fiber_arg)
        
        # 添加patch
        patch_arg = {"args": ["rect", 2, 5, 5, -0.5, -0.5, 0.5, 0.5], "kwargs": {}}
        section_manager_2d.handle("patch", patch_arg)
        
        # 添加layer
        layer_arg = {"args": ["straight", 3, 4, 0.01, -0.4, 0.4, 0.4, 0.4], "kwargs": {}}
        section_manager_2d.handle("layer", layer_arg)
        
        # 测试获取方法
        fibers = section_manager_2d.get_fibers(998)
        assert len(fibers) == 1
        
        patches = section_manager_2d.get_patches(998)
        assert len(patches) == 1
        
        layers = section_manager_2d.get_layers(998)
        assert len(layers) == 1
        
        # 测试不存在的截面
        assert section_manager_2d.get_fibers(999) is None
        assert section_manager_2d.get_patches(999) is None
        assert section_manager_2d.get_layers(999) is None

    def test_current_section_tracking(self, section_manager_2d: SectionManager):
        """测试当前截面跟踪"""
        # 创建弹性截面（不会设置current_section）
        elastic_arg = {"args": ["Elastic", 1, 29000, 100, 10], "kwargs": {}}
        section_manager_2d.handle("section", elastic_arg)
        assert section_manager_2d.current_section is None
        
        # 创建纤维截面（会设置current_section）
        fiber_arg = {"args": ["Fiber", 2], "kwargs": {}}
        section_manager_2d.handle("section", fiber_arg)
        assert section_manager_2d.current_section == 2
        
        # 创建另一个弹性截面（会清除current_section）
        elastic_arg2 = {"args": ["Elastic", 3, 30000, 120, 12], "kwargs": {}}
        section_manager_2d.handle("section", elastic_arg2)
        assert section_manager_2d.current_section is None

    def test_no_current_section_error(self, section_manager_2d: SectionManager):
        """测试在没有当前截面时添加组件的错误处理"""
        # 尝试在没有当前截面时添加fiber
        fiber_arg = {"args": [0.1, 0.2, 0.05, 1], "kwargs": {}}
        assert section_manager_2d.current_section is None

        with pytest.raises(ValueError, match="No current section defined"):
            section_manager_2d.handle("fiber", fiber_arg)
        
        # 尝试在没有当前截面时添加patch
        patch_arg = {"args": ["rect", 2, 5, 5, -0.5, -0.5, 0.5, 0.5], "kwargs": {}}
        
        with pytest.raises(ValueError, match="No current section defined"):
            section_manager_2d.handle("patch", patch_arg)
        
        # 尝试在没有当前截面时添加layer
        layer_arg = {"args": ["straight", 3, 4, 0.01, -0.4, 0.4, 0.4, 0.4], "kwargs": {}}
        
        with pytest.raises(ValueError, match="No current section defined"):
            section_manager_2d.handle("layer", layer_arg)


class TestSections:
    """测试SectionHandler的各种截面类型,直接利用SectionManager的handle方法"""
    
    def test_elastic_section_2d(self, section_manager_2d: SectionManager):
        """测试弹性截面 2D"""
        args = ["Elastic", 1, 29000, 100, 10]
        kwargs = {}
        arg_map = {"args": args, "kwargs": kwargs}
        
        section_manager_2d.handle("section", arg_map)
        
        assert 1 in section_manager_2d.sections
        section = section_manager_2d.sections[1]
        assert section["secType"] == "Elastic"
        assert section["secTag"] == 1
        assert section["E_mod"] == 29000
        assert section["A"] == 100
        assert section["Iz"] == 10

    def test_elastic_section_3d(self, section_manager_3d: SectionManager):
        """测试弹性截面 3D"""
        args = ["Elastic", 1, 29000, 100, 10, 8, 11000, 15]
        kwargs = {"alphaY": 0.8, "alphaZ": 0.9}
        arg_map = {"args": args, "kwargs": kwargs}
        
        section_manager_3d.handle("section", arg_map)
        
        section = section_manager_3d.sections[1]
        assert section["secType"] == "Elastic"
        assert section["E_mod"] == 29000
        assert section["A"] == 100
        assert section["Iz"] == 10
        assert section["Iy"] == 8
        assert section["G_mod"] == 11000
        assert section["Jxx"] == 15
        assert section["alphaY"] == 0.8
        assert section["alphaZ"] == 0.9

    def test_all_fiber_section_types(self, section_manager_2d: SectionManager):
        """测试所有纤维截面类型"""
        # Fiber
        fiber_arg = {"args": ["Fiber", 1, "-GJ", 100], "kwargs": {}}
        section_manager_2d.handle("section", fiber_arg)
        section = section_manager_2d.sections[1]
        assert section["secType"] == "Fiber"
        assert "fibers" in section
        assert "patches" in section
        assert "layers" in section
        
        # FiberThermal
        fiber_thermal_arg = {"args": ["FiberThermal", 2, "-GJ", 80], "kwargs": {}}
        section_manager_2d.handle("section", fiber_thermal_arg)
        section = section_manager_2d.sections[2]
        assert section["secType"] == "FiberThermal"
        assert "fibers" in section
        
        # NDFiber
        ndfiber_arg = {"args": ["NDFiber", 3], "kwargs": {}}
        section_manager_2d.handle("section", ndfiber_arg)
        section = section_manager_2d.sections[3]
        assert section["secType"] == "NDFiber"
        assert "fibers" in section
        
        # PlateFiber
        plate_fiber_arg = {"args": ["PlateFiber", 4, 1, 0.5], "kwargs": {}}
        section_manager_2d.handle("section", plate_fiber_arg)
        section = section_manager_2d.sections[4]
        assert section["secType"] == "PlateFiber"
        assert "fibers" in section

    def test_special_section_types(self, section_manager_2d: SectionManager):
        """测试特殊截面类型"""
        # WFSection2d
        wf_arg = {"args": ["WFSection2d", 1, 1, 24, 0.5, 12, 0.75, 10, 16], "kwargs": {}}
        section_manager_2d.handle("section", wf_arg)
        section = section_manager_2d.sections[1]
        assert section["secType"] == "WFSection2d"
        
        # RCSection2d
        rc_arg = {"args": ["RCSection2d", 2, 1, 2, 3, 24, 12, 2, 6, 6, 2, 8, 6, 4], "kwargs": {}}
        section_manager_2d.handle("section", rc_arg)
        section = section_manager_2d.sections[2]
        assert section["secType"] == "RCSection2d"
        
        # Parallel
        parallel_arg = {"args": ["Parallel", 3, [1, 2, 3]], "kwargs": {}}
        section_manager_2d.handle("section", parallel_arg)
        section = section_manager_2d.sections[3]
        assert section["secType"] == "Parallel"
        
        # Uniaxial
        uniaxial_arg = {"args": ["Uniaxial", 4, 1, "P"], "kwargs": {}}
        section_manager_2d.handle("section", uniaxial_arg)
        section = section_manager_2d.sections[4]
        assert section["secType"] == "Uniaxial"

    def test_unknown_section_handling(self, section_manager_2d: SectionManager):
        """测试未知截面类型处理"""
        # 创建未知截面类型
        unknown_arg = {"args": ["UnknownSection", 99, "param1", "param2"], "kwargs": {}}
        section_manager_2d.handle("section", unknown_arg)
        
        # 验证未知截面被存储
        section = section_manager_2d.get_section(99)
        assert section is not None
        assert section["secType"] == "UnknownSection"
        assert section["secTag"] == 99
        assert section["args"] == ["param1", "param2"]
        assert section["sectionType"] == "section"


if __name__ == "__main__":
    pytest.main([__file__]) 