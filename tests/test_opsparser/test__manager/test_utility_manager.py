"""
Tests for UtilityManager

This module tests the UtilityManager class which handles
OpenSeesPy utility commands.
"""

import pytest
from typing import Dict, Any

from opsparser._manager._UtilityManager import UtilityManager


@pytest.fixture
def utility_manager() -> UtilityManager:
    """每个测试前初始化一个UtilityManager实例"""
    manager = UtilityManager()
    manager.clear()
    return manager


@pytest.fixture
def configured_utility_manager() -> UtilityManager:
    """每个测试前初始化一个配置好的UtilityManager实例"""
    manager = UtilityManager()
    manager.clear()
    
    # 添加一些默认配置
    manager.handle("setTime", {"args": ["5.0"], "kwargs": {}})
    manager.handle("setPrecision", {"args": ["8"], "kwargs": {}})
    manager.handle("save", {"args": ["1"], "kwargs": {}})
    
    return manager


def test_handles(utility_manager: UtilityManager):
    """测试handles方法"""
    expected_commands = [
        'wipe', 'wipeAnalysis', 'reset', 'remove', 'save', 'restore',
        'loadConst', 'reactions', 'setTime', 'getTime', 'setPrecision',
        'setParameter', 'database', 'logFile', 'setNodeCoord', 'setNodeDisp',
        'setNodeVel', 'setNodeAccel', 'setElementRayleighDampingFactors',
        'modalDamping', 'start', 'stop', 'updateElementDomain', 'updateMaterialStage'
    ]
    handles = utility_manager.handles()
    for cmd in expected_commands:
        assert cmd in handles


def test_save_restore_commands(utility_manager: UtilityManager):
    """测试保存和恢复命令"""
    # 测试保存
    args = {"args": ["1"], "kwargs": {}}
    utility_manager.handle("save", args)
    
    states = utility_manager.get_model_states()
    assert 1 in states
    assert states[1]["time"] == 0.0  # 默认时间
    
    # 测试恢复
    args = {"args": ["1"], "kwargs": {}}
    utility_manager.handle("restore", args)
    
    assert utility_manager.get_current_time() == 0.0


def test_set_time_command(utility_manager: UtilityManager):
    """测试setTime命令"""
    args = {"args": ["5.0"], "kwargs": {}}
    utility_manager.handle("setTime", args)
    
    assert utility_manager.get_current_time() == 5.0


def test_set_precision_command(utility_manager: UtilityManager):
    """测试setPrecision命令"""
    args = {"args": ["10"], "kwargs": {}}
    utility_manager.handle("setPrecision", args)
    
    assert utility_manager.get_precision() == 10


def test_set_parameter_command(utility_manager: UtilityManager):
    """测试setParameter命令"""
    args = {"args": ["1", "100.0"], "kwargs": {}}
    utility_manager.handle("setParameter", args)
    
    parameters = utility_manager.get_parameters()
    assert 1 in parameters
    assert parameters[1]["value"] == 100.0


def test_load_const_command(utility_manager: UtilityManager):
    """测试loadConst命令"""
    args = {"args": ["-time", "2.5"], "kwargs": {}}
    utility_manager.handle("loadConst", args)
    
    load_info = utility_manager.get_load_constant_info()
    assert load_info["time"] == "2.5"


def test_reactions_command(utility_manager: UtilityManager):
    """测试reactions命令"""
    args = {"args": ["-dynamic"], "kwargs": {}}
    utility_manager.handle("reactions", args)
    
    reactions_info = utility_manager.get_reactions_info()
    assert reactions_info["dynamic"] == True


def test_database_command(utility_manager: UtilityManager):
    """测试database命令"""
    args = {"args": ["File", "mydb.db"], "kwargs": {}}
    utility_manager.handle("database", args)
    
    db_info = utility_manager.get_database_info()
    assert db_info["type"] == "File"
    assert db_info["name"] == "mydb.db"


def test_log_file_command(utility_manager: UtilityManager):
    """测试logFile命令"""
    args = {"args": ["log.txt"], "kwargs": {}}
    utility_manager.handle("logFile", args)
    
    assert utility_manager.get_log_file() == "log.txt"


def test_timing_commands(utility_manager: UtilityManager):
    """测试计时启动/停止命令"""
    # 测试启动
    args = {"args": [], "kwargs": {}}
    utility_manager.handle("start", args)
    assert utility_manager.is_timing_active() == True
    
    # 测试停止
    args = {"args": [], "kwargs": {}}
    utility_manager.handle("stop", args)
    assert utility_manager.is_timing_active() == False


def test_wipe_commands(configured_utility_manager: UtilityManager):
    """测试wipe命令"""
    # 验证配置存在
    assert configured_utility_manager.get_current_time() == 5.0
    assert configured_utility_manager.get_precision() == 8
    
    # 测试wipe
    args = {"args": [], "kwargs": {}}
    configured_utility_manager.handle("wipe", args)
    
    assert configured_utility_manager.get_current_time() == 0.0
    assert configured_utility_manager.get_precision() == 6


def test_remove_command(utility_manager: UtilityManager):
    """测试remove命令"""
    args = {"args": ["element", "1", "2", "3"], "kwargs": {}}
    utility_manager.handle("remove", args)
    
    # 检查命令是否记录在历史中
    history = utility_manager.get_utility_history()
    remove_commands = [h for h in history if h["command"] == "remove"]
    assert len(remove_commands) == 1


def test_set_node_property_commands(utility_manager: UtilityManager):
    """测试setNode*命令"""
    # 测试setNodeCoord
    args = {"args": ["1", "0.0", "0.0", "0.0"], "kwargs": {}}
    utility_manager.handle("setNodeCoord", args)
    
    # 测试setNodeDisp
    args = {"args": ["1", "0.1", "0.2"], "kwargs": {}}
    utility_manager.handle("setNodeDisp", args)
    
    history = utility_manager.get_utility_history()
    set_commands = [h for h in history if h["command"].startswith("setNode")]
    assert len(set_commands) == 2


def test_clear(configured_utility_manager: UtilityManager):
    """测试清除功能"""
    # 验证数据存在
    assert configured_utility_manager.get_current_time() > 0.0
    assert len(configured_utility_manager.get_model_states()) > 0
    
    # 清除并验证
    configured_utility_manager.clear()
    assert configured_utility_manager.get_current_time() == 0.0
    assert len(configured_utility_manager.get_model_states()) == 0
    assert len(configured_utility_manager.get_parameters()) == 0
    assert len(configured_utility_manager.get_utility_history()) == 0 