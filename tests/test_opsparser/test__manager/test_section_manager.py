"""
Tests for SectionManager

This module tests the SectionManager class which handles
OpenSeesPy section commands.
"""

import pytest
from typing import Dict, Any

from opsparser._manager._SectionManager import SectionManager


@pytest.fixture
def section_manager() -> SectionManager:
    """每个测试前初始化一个SectionManager实例"""
    manager = SectionManager()
    manager.clear()
    return manager


@pytest.fixture
def configured_section_manager() -> SectionManager:
    """每个测试前初始化一个配置好的SectionManager实例"""
    manager = SectionManager()
    manager.clear()
    
    # 添加一些默认截面
    arg_map1 = {"args": ["Elastic", 1, 29000, 100, 10], "kwargs": {}}
    arg_map2 = {"args": ["Fiber", 2, 0.1, 0.1], "kwargs": {}}
    arg_map3 = {"args": ["Elastic", 3, 30000, 120, 12], "kwargs": {}}
    
    manager.handle("section", arg_map1)
    manager.handle("section", arg_map2)
    manager.handle("section", arg_map3)
    
    return manager


def test_section_command_parsing(section_manager: SectionManager):
    """测试截面命令解析"""
    # 测试基本截面命令
    arg_map = {"args": ["Elastic", 1, 29000, 100, 10], "kwargs": {}}
    section_manager.handle("section", arg_map)
    
    # 验证截面是否存储
    section = section_manager.get_section(1)
    assert section is not None
    assert section["type"] == "Elastic"
    assert section["tag"] == 1


def test_get_sections_by_type(configured_section_manager: SectionManager):
    """测试按类型获取截面"""
    # 获取弹性截面
    elastic_sections = configured_section_manager.get_sections_by_type("Elastic")
    assert len(elastic_sections) == 2
    
    # 获取纤维截面
    fiber_sections = configured_section_manager.get_sections_by_type("Fiber")
    assert len(fiber_sections) == 1


def test_clear(configured_section_manager: SectionManager):
    """测试清除截面数据"""
    assert len(configured_section_manager.sections) == 3
    configured_section_manager.clear()
    assert len(configured_section_manager.sections) == 0


if __name__ == "__main__":
    pytest.main([__file__]) 