"""
Tests for RegionManager

This module tests the RegionManager class which handles
OpenSeesPy region commands.
"""

import pytest
from typing import Dict, Any

from opsparser._manager._RegionManager import RegionManager


@pytest.fixture
def region_manager() -> RegionManager:
    """每个测试前初始化一个RegionManager实例"""
    manager = RegionManager()
    manager.clear()
    return manager


def test_region_command_parsing(region_manager: RegionManager):
    """测试区域命令解析"""
    # 模拟解析后的区域命令参数
    arg_map = {
        "tag": 1,
        "node_tags": [1, 2, 3],
        "ele_tags": [10, 11],
        "ele_range": [20, 25],
        "rayleigh_params": [0.01, 0.02, 0.0, 0.0]
    }
    region_manager._handle_region(arg_map)
    
    # 验证区域是否存储
    region = region_manager.get_region(1)
    assert region is not None
    assert region["tag"] == 1
    assert 1 in region["node_tags"]
    assert 10 in region["ele_tags"]
    assert 20 in region["ele_tags"]  # 来自范围
    assert "rayleigh" in region


def test_get_regions_with_node(region_manager: RegionManager):
    """测试获取包含特定节点的区域"""
    # 创建包含特定节点的区域
    arg_map = {"tag": 1, "node_tags": [5, 6, 7], "ele_tags": []}
    region_manager._handle_region(arg_map)
    
    # 查找包含节点6的区域
    regions = region_manager.get_regions_with_node(6)
    assert len(regions) == 1
    assert regions[0]["tag"] == 1


if __name__ == "__main__":
    pytest.main([__file__]) 