"""
Tests for TimeSeriesManager

This module tests the TimeSeriesManager class which handles
OpenSeesPy timeSeries commands.
"""

import pytest
from typing import Dict, Any

from opsparser._manager._TimeSeriesManager import TimeSeriesManager


@pytest.fixture
def time_series_manager() -> TimeSeriesManager:
    """每个测试前初始化一个TimeSeriesManager实例"""
    manager = TimeSeriesManager()
    manager.clear()
    return manager


@pytest.fixture
def configured_time_series_manager() -> TimeSeriesManager:
    """每个测试前初始化一个配置好的TimeSeriesManager实例"""
    manager = TimeSeriesManager()
    manager.clear()
    
    # 添加一些默认时间序列
    arg_map1 = {"args": ["Linear", 1], "kwargs": {}}
    arg_map2 = {"args": ["Constant", 2, 1.5], "kwargs": {}}
    
    manager.handle("timeSeries", arg_map1)
    manager.handle("timeSeries", arg_map2)
    
    return manager


def test_time_series_command_parsing(time_series_manager: TimeSeriesManager):
    """测试时间序列命令解析"""
    # 测试线性时间序列命令
    arg_map = {"args": ["Linear", 1], "kwargs": {}}
    time_series_manager.handle("timeSeries", arg_map)
    
    # 验证时间序列是否存储
    series = time_series_manager.get_time_series(1)
    assert series is not None
    assert series["type"] == "Linear"
    assert series["tag"] == 1


def test_constant_time_series_parsing(time_series_manager: TimeSeriesManager):
    """测试常数时间序列解析"""
    # 测试常数时间序列命令
    arg_map = {"args": ["Constant", 2, 1.5], "kwargs": {}}
    time_series_manager.handle("timeSeries", arg_map)
    
    # 验证时间序列是否存储
    series = time_series_manager.get_time_series(2)
    assert series is not None
    assert series["type"] == "Constant"
    assert series["tag"] == 2
    assert series["factor"] == 1.5


def test_get_series_by_type(configured_time_series_manager: TimeSeriesManager):
    """测试按类型获取时间序列"""
    # 获取线性时间序列
    linear_series = configured_time_series_manager.get_series_by_type("Linear")
    assert len(linear_series) == 1
    
    # 获取常数时间序列
    constant_series = configured_time_series_manager.get_series_by_type("Constant")
    assert len(constant_series) == 1


def test_clear(configured_time_series_manager: TimeSeriesManager):
    """测试清除时间序列数据"""
    assert len(configured_time_series_manager.get_all_time_series()) == 2
    configured_time_series_manager.clear()
    assert len(configured_time_series_manager.get_all_time_series()) == 0


if __name__ == "__main__":
    pytest.main([__file__]) 