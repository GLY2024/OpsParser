"""
Tests for GeomTransfManager

This module tests the GeomTransfManager class which handles
OpenSeesPy geomTransf commands.
"""

import pytest
from typing import Dict, Any

from opsparser._manager._GeomTransfManager import GeomTransfManager


@pytest.fixture
def geom_transf_manager() -> GeomTransfManager:
    """每个测试前初始化一个GeomTransfManager实例"""
    manager = GeomTransfManager()
    manager.clear()
    return manager


@pytest.fixture
def configured_geom_transf_manager() -> GeomTransfManager:
    """每个测试前初始化一个配置好的GeomTransfManager实例"""
    manager = GeomTransfManager()
    manager.clear()
    
    # 添加2D变换
    arg_map_2d = {"transf_type": "Linear", "tag": 1, "args": []}
    manager._handle_geom_transf(arg_map_2d)
    
    # 添加3D变换
    arg_map_3d = {"transf_type": "Corotational", "tag": 2, "args": [1.0, 0.0, 0.0]}
    manager._handle_geom_transf(arg_map_3d)
    
    return manager


def test_geom_transf_2d_command_parsing(geom_transf_manager: GeomTransfManager):
    """测试2D geomTransf命令解析"""
    arg_map = {
        "transf_type": "Linear",
        "tag": 1,
        "args": []  # 2D情况
    }
    geom_transf_manager._handle_geom_transf(arg_map)
    
    # 验证变换是否存储
    transf = geom_transf_manager.get_transformation(1)
    assert transf is not None
    assert transf["type"] == "Linear"
    assert transf["dimension"] == "2D"


def test_geom_transf_3d_command_parsing(geom_transf_manager: GeomTransfManager):
    """测试3D geomTransf命令解析"""
    arg_map = {
        "transf_type": "PDelta",
        "tag": 2,
        "args": [0.0, 0.0, 1.0]  # 3D的vecxz
    }
    geom_transf_manager._handle_geom_transf(arg_map)
    
    # 验证变换是否存储
    transf = geom_transf_manager.get_transformation(2)
    assert transf is not None
    assert transf["type"] == "PDelta"
    assert transf["vecxz"] == [0.0, 0.0, 1.0]


def test_get_transformations_by_dimension(configured_geom_transf_manager: GeomTransfManager):
    """测试按维度获取变换"""
    # 检查2D和3D变换
    transf_2d = configured_geom_transf_manager.get_2d_transformations()
    transf_3d = configured_geom_transf_manager.get_3d_transformations()
    
    assert len(transf_2d) == 1
    assert len(transf_3d) == 1
    assert transf_2d[0]["tag"] == 1
    assert transf_3d[0]["tag"] == 2


if __name__ == "__main__":
    pytest.main([__file__]) 