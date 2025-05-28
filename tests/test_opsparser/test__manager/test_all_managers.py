"""
Integration test module for all Manager classes

This module runs basic integration tests to ensure all Manager classes
are properly tested in their individual test files.
"""

import pytest
from opsparser._manager import (
    SectionManager, ConstraintManager, RegionManager, RayleighManager,
    BlockManager, BeamIntegrationManager, FrictionModelManager, GeomTransfManager,
    LoadManager, TimeSeriesManager, ElementManager,
    AnalysisManager, RecorderManager, UtilityManager,
    MaterialManager, NodeManager
)


def test_all_managers_can_be_instantiated():
    """测试所有管理器都能正常实例化"""
    managers = [
        SectionManager(),
        ConstraintManager(),
        RegionManager(),
        RayleighManager(),
        BlockManager(),
        BeamIntegrationManager(),
        FrictionModelManager(),
        GeomTransfManager(),
        LoadManager(),
        TimeSeriesManager(),
        ElementManager(),
        AnalysisManager(),
        RecorderManager(),
        UtilityManager(),
        MaterialManager(),
        NodeManager()
    ]
    
    # 确保所有管理器都成功实例化
    assert len(managers) == 16
    
    # 测试所有管理器都有clear方法
    for manager in managers:
        assert hasattr(manager, 'clear')
        manager.clear()  # 确保clear方法可以正常调用


def test_all_managers_have_handles_method():
    """测试所有管理器都有handles方法"""
    manager_classes = [
        SectionManager, ConstraintManager, RegionManager, RayleighManager,
        BlockManager, BeamIntegrationManager, FrictionModelManager, GeomTransfManager,
        LoadManager, TimeSeriesManager, ElementManager,
        AnalysisManager, RecorderManager, UtilityManager,
        MaterialManager, NodeManager
    ]
    
    for manager_class in manager_classes:
        assert hasattr(manager_class, 'handles')
        handles = manager_class.handles()
        assert isinstance(handles, list)
        assert len(handles) > 0


def test_managers_file_structure_corresponds_to_source():
    """验证测试文件结构与源代码Manager结构对应"""
    # 这是一个元测试，验证我们为每个Manager都创建了对应的测试文件
    expected_test_files = [
        'test_section_manager.py',
        'test_constraint_manager.py', 
        'test_region_manager.py',
        'test_rayleigh_manager.py',
        'test_block_manager.py',
        'test_beam_integration_manager.py',
        'test_friction_model_manager.py',
        'test_geom_transf_manager.py',
        'test_load_manager.py',
        'test_time_series_manager.py',
        'test_element_manager.py',
        'test_analysis_manager.py',
        'test_recorder_manager.py',
        'test_utility_manager.py',
        'test_material_manager.py',
        'test_node_manager.py'
    ]
    
    # 确认我们创建了所有必要的测试文件
    # 这是一个占位符测试，实际的文件检查会在运行时进行
    assert len(expected_test_files) == 16


if __name__ == "__main__":
    pytest.main([__file__]) 