"""
Tests for ElementManager

This module tests the ElementManager class which handles
OpenSeesPy element commands.
"""

import pytest
from typing import Dict, Any

from opsparser._manager._ElementManager import ElementManager


@pytest.fixture
def element_manager() -> ElementManager:
    """每个测试前初始化一个ElementManager实例"""
    manager = ElementManager()
    manager.clear()
    return manager


@pytest.fixture
def configured_element_manager() -> ElementManager:
    """每个测试前初始化一个配置好的ElementManager实例"""
    manager = ElementManager()
    manager.clear()
    
    # 添加一些默认单元
    arg_map1 = {"args": ["truss", 1, 1, 2, 100, 1], "kwargs": {}}
    arg_map2 = {"args": ["beam2D", 2, 2, 3, 200, 1, 1], "kwargs": {}}
    
    manager.handle("element", arg_map1)
    manager.handle("element", arg_map2)
    
    return manager


def test_element_command_parsing(element_manager: ElementManager):
    """测试单元命令解析"""
    # 测试桁架单元命令
    arg_map = {"args": ["truss", 1, 1, 2, 100, 1], "kwargs": {}}
    element_manager.handle("element", arg_map)
    
    # 验证单元是否存储
    element = element_manager.get_element(1)
    assert element is not None
    assert element["type"] == "truss"
    assert element["tag"] == 1
    assert element["nodes"] == [1, 2]


def test_beam_element_parsing(element_manager: ElementManager):
    """测试梁单元解析"""
    # 测试梁单元命令
    arg_map = {"args": ["forceBeamColumn", 2, 1, 2, 1, 1], "kwargs": {}}
    element_manager.handle("element", arg_map)
    
    # 验证单元是否存储
    element = element_manager.get_element(2)
    assert element is not None
    assert element["type"] == "forceBeamColumn"
    assert element["tag"] == 2
    assert element["nodes"] == [1, 2]


def test_get_elements_by_type(configured_element_manager: ElementManager):
    """测试按类型获取单元"""
    # 获取桁架单元
    truss_elements = configured_element_manager.get_elements_by_type("truss")
    assert len(truss_elements) == 1
    
    # 获取梁单元
    beam_elements = configured_element_manager.get_elements_by_type("beam2D")
    assert len(beam_elements) == 1


def test_get_elements_by_node(configured_element_manager: ElementManager):
    """测试获取包含特定节点的单元"""
    # 获取包含节点2的单元
    elements = configured_element_manager.get_elements_with_node(2)
    assert len(elements) == 2  # 两个单元都包含节点2


def test_clear(configured_element_manager: ElementManager):
    """测试清除单元数据"""
    assert len(configured_element_manager.get_all_elements()) == 2
    configured_element_manager.clear()
    assert len(configured_element_manager.get_all_elements()) == 0


if __name__ == "__main__":
    pytest.main([__file__]) 