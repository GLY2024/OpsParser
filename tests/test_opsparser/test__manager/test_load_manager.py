"""
Tests for LoadManager

This module tests the LoadManager class which handles
OpenSeesPy load commands.
"""

import pytest
from typing import Dict, Any

from opsparser._manager._LoadManager import LoadManager


@pytest.fixture
def load_manager() -> LoadManager:
    """每个测试前初始化一个LoadManager实例"""
    manager = LoadManager()
    manager.clear()
    return manager


@pytest.fixture
def configured_load_manager() -> LoadManager:
    """每个测试前初始化一个配置好的LoadManager实例"""
    manager = LoadManager()
    manager.clear()
    
    # 添加一些默认载荷
    arg_map1 = {"args": [1, 100.0, 200.0], "kwargs": {}}
    arg_map2 = {"args": [2, -50.0, 0.0, 100.0], "kwargs": {}}
    
    manager.handle("load", arg_map1)
    manager.handle("load", arg_map2)
    
    return manager


def test_load_command_parsing(load_manager: LoadManager):
    """测试载荷命令解析"""
    # 测试节点载荷命令
    arg_map = {"args": [1, 100.0, 200.0], "kwargs": {}}
    load_manager.handle("load", arg_map)
    
    # 验证载荷是否存储
    loads = load_manager.get_node_loads()
    assert len(loads) == 1
    assert loads[0]["node_tag"] == 1
    assert loads[0]["forces"] == [100.0, 200.0]


def test_element_load_command_parsing(load_manager: LoadManager):
    """测试单元载荷命令解析"""
    # 测试单元载荷命令
    arg_map = {"args": ["-ele", 1, "-type", "-beamUniform", 10.0], "kwargs": {}}
    load_manager.handle("eleLoad", arg_map)
    
    # 验证单元载荷是否存储
    loads = load_manager.get_element_loads()
    assert len(loads) == 1
    assert loads[0]["element_tag"] == 1
    assert loads[0]["load_type"] == "beamUniform"


def test_pattern_command_parsing(load_manager: LoadManager):
    """测试载荷模式命令解析"""
    # 测试载荷模式命令
    arg_map = {"args": ["Plain", 1, 1], "kwargs": {}}
    load_manager.handle("pattern", arg_map)
    
    # 验证载荷模式是否存储
    patterns = load_manager.get_load_patterns()
    assert len(patterns) == 1
    assert patterns[0]["pattern_type"] == "Plain"
    assert patterns[0]["tag"] == 1


def test_get_loads_by_node(configured_load_manager: LoadManager):
    """测试按节点获取载荷"""
    # 获取节点1的载荷
    node_loads = configured_load_manager.get_loads_by_node(1)
    assert len(node_loads) == 1
    assert node_loads[0]["forces"] == [100.0, 200.0]


def test_clear(configured_load_manager: LoadManager):
    """测试清除载荷数据"""
    assert len(configured_load_manager.get_node_loads()) == 2
    configured_load_manager.clear()
    assert len(configured_load_manager.get_node_loads()) == 0


if __name__ == "__main__":
    pytest.main([__file__]) 