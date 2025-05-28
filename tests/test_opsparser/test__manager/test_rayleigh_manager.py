"""
Tests for RayleighManager

This module tests the RayleighManager class which handles
OpenSeesPy Rayleigh damping commands.
"""

import pytest
from typing import Dict, Any

from opsparser._manager._RayleighManager import RayleighManager


@pytest.fixture
def rayleigh_manager() -> RayleighManager:
    """每个测试前初始化一个RayleighManager实例"""
    manager = RayleighManager()
    manager.clear()
    return manager


def test_rayleigh_command_parsing(rayleigh_manager: RayleighManager):
    """测试Rayleigh命令解析"""
    arg_map = {
        "alphaM": 0.01,
        "betaK": 0.02,
        "betaKinit": 0.0,
        "betaKcomm": 0.0
    }
    rayleigh_manager._handle_rayleigh(arg_map)
    
    # 验证Rayleigh参数是否存储
    params = rayleigh_manager.get_current_rayleigh()
    assert params is not None
    assert params["alphaM"] == 0.01
    assert params["betaK"] == 0.02
    assert rayleigh_manager.has_rayleigh_damping()


def test_rayleigh_history(rayleigh_manager: RayleighManager):
    """测试Rayleigh阻尼历史"""
    # 添加第一组参数
    arg_map1 = {"alphaM": 0.01, "betaK": 0.02, "betaKinit": 0.0, "betaKcomm": 0.0}
    rayleigh_manager._handle_rayleigh(arg_map1)
    
    # 添加第二组参数
    arg_map2 = {"alphaM": 0.02, "betaK": 0.04, "betaKinit": 0.0, "betaKcomm": 0.0}
    rayleigh_manager._handle_rayleigh(arg_map2)
    
    # 检查历史
    history = rayleigh_manager.get_rayleigh_history()
    assert len(history) == 2
    assert history[0]["alphaM"] == 0.01
    assert history[1]["alphaM"] == 0.02


if __name__ == "__main__":
    pytest.main([__file__]) 