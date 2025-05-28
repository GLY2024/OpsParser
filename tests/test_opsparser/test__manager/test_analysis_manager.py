"""
Tests for AnalysisManager

This module tests the AnalysisManager class which handles
OpenSeesPy analysis commands.
"""

import pytest
from typing import Dict, Any

from opsparser._manager._AnalysisManager import AnalysisManager


@pytest.fixture
def analysis_manager() -> AnalysisManager:
    """每个测试前初始化一个AnalysisManager实例"""
    manager = AnalysisManager()
    manager.clear()
    return manager


@pytest.fixture
def configured_analysis_manager() -> AnalysisManager:
    """每个测试前初始化一个配置好的AnalysisManager实例"""
    manager = AnalysisManager()
    manager.clear()
    
    # 添加基本分析配置
    manager.handle("constraints", {"args": ["Plain"], "kwargs": {}})
    manager.handle("numberer", {"args": ["RCM"], "kwargs": {}})
    manager.handle("system", {"args": ["BandGeneral"], "kwargs": {}})
    
    return manager


def test_handles(analysis_manager: AnalysisManager):
    """测试handles方法"""
    expected_commands = [
        'constraints', 'numberer', 'system', 'test', 'algorithm',
        'integrator', 'analysis', 'eigen', 'analyze', 'modalProperties',
        'responseSpectrumAnalysis'
    ]
    handles = analysis_manager.handles()
    for cmd in expected_commands:
        assert cmd in handles


def test_constraints_command(analysis_manager: AnalysisManager):
    """测试constraints命令解析"""
    args = {"args": ["Plain"], "kwargs": {}}
    analysis_manager.handle("constraints", args)
    
    current_setup = analysis_manager.get_current_analysis_setup()
    assert current_setup["constraints"]["type"] == "Plain"


def test_numberer_command(analysis_manager: AnalysisManager):
    """测试numberer命令解析"""
    args = {"args": ["RCM"], "kwargs": {}}
    analysis_manager.handle("numberer", args)
    
    current_setup = analysis_manager.get_current_analysis_setup()
    assert current_setup["numberer"]["type"] == "RCM"


def test_system_command(analysis_manager: AnalysisManager):
    """测试system命令解析"""
    args = {"args": ["BandGeneral"], "kwargs": {}}
    analysis_manager.handle("system", args)
    
    current_setup = analysis_manager.get_current_analysis_setup()
    assert current_setup["system"]["type"] == "BandGeneral"


def test_test_command(analysis_manager: AnalysisManager):
    """测试收敛测试命令解析"""
    args = {"args": ["NormDispIncr", "1.0e-6", "10"], "kwargs": {}}
    analysis_manager.handle("test", args)
    
    current_setup = analysis_manager.get_current_analysis_setup()
    assert current_setup["test"]["type"] == "NormDispIncr"
    assert current_setup["test"]["args"] == ["1.0e-6", "10"]


def test_algorithm_command(analysis_manager: AnalysisManager):
    """测试algorithm命令解析"""
    args = {"args": ["Newton"], "kwargs": {}}
    analysis_manager.handle("algorithm", args)
    
    current_setup = analysis_manager.get_current_analysis_setup()
    assert current_setup["algorithm"]["type"] == "Newton"


def test_integrator_command(analysis_manager: AnalysisManager):
    """测试integrator命令解析"""
    args = {"args": ["LoadControl", "0.1"], "kwargs": {}}
    analysis_manager.handle("integrator", args)
    
    current_setup = analysis_manager.get_current_analysis_setup()
    assert current_setup["integrator"]["type"] == "LoadControl"
    assert current_setup["integrator"]["args"] == ["0.1"]


def test_analysis_command(analysis_manager: AnalysisManager):
    """测试analysis命令解析"""
    args = {"args": ["Static"], "kwargs": {}}
    analysis_manager.handle("analysis", args)
    
    current_setup = analysis_manager.get_current_analysis_setup()
    assert current_setup["analysis"]["type"] == "Static"


def test_eigen_command(analysis_manager: AnalysisManager):
    """测试eigen命令解析"""
    args = {"args": ["5"], "kwargs": {}}
    analysis_manager.handle("eigen", args)
    
    eigen_info = analysis_manager.get_eigen_info()
    assert len(eigen_info) == 1
    assert eigen_info[0]["num_modes"] == 5


def test_analyze_command(analysis_manager: AnalysisManager):
    """测试analyze命令解析"""
    args = {"args": ["10"], "kwargs": {}}
    analysis_manager.handle("analyze", args)
    
    history = analysis_manager.get_analysis_history()
    assert len(history) == 1
    assert history[0]["num_steps"] == 10


def test_modal_properties_command(analysis_manager: AnalysisManager):
    """测试modalProperties命令解析"""
    args = {"args": ["5"], "kwargs": {}}
    analysis_manager.handle("modalProperties", args)
    
    properties = analysis_manager.get_modal_properties()
    assert properties["args"] == ["5"]


def test_get_current_analysis_setup(configured_analysis_manager: AnalysisManager):
    """测试获取当前分析设置"""
    current_setup = configured_analysis_manager.get_current_analysis_setup()
    assert current_setup["constraints"]["type"] == "Plain"
    assert current_setup["numberer"]["type"] == "RCM"
    assert current_setup["system"]["type"] == "BandGeneral"


def test_clear(configured_analysis_manager: AnalysisManager):
    """测试清除功能"""
    # 添加一些数据
    configured_analysis_manager.handle("eigen", {"args": ["5"], "kwargs": {}})
    
    # 验证数据存在
    assert len(configured_analysis_manager.get_analysis_history()) > 0 or len(configured_analysis_manager.get_eigen_info()) > 0
    
    # 清除并验证
    configured_analysis_manager.clear()
    assert len(configured_analysis_manager.get_analysis_history()) == 0
    assert len(configured_analysis_manager.get_eigen_info()) == 0
    assert len(configured_analysis_manager.get_modal_properties()) == 0 