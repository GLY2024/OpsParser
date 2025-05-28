"""
Tests for RecorderManager

This module tests the RecorderManager class which handles
OpenSeesPy recorder and output commands.
"""

import pytest
from typing import Dict, Any

from opsparser._manager._RecorderManager import RecorderManager


@pytest.fixture
def recorder_manager() -> RecorderManager:
    """每个测试前初始化一个RecorderManager实例"""
    manager = RecorderManager()
    manager.clear()
    return manager


@pytest.fixture
def configured_recorder_manager() -> RecorderManager:
    """每个测试前初始化一个配置好的RecorderManager实例"""
    manager = RecorderManager()
    manager.clear()
    
    # 添加一些默认记录器
    args = {"args": ["Node", "-file", "output.out", "-time", "-node", 1, 2, 3, "disp"], "kwargs": {}}
    manager.handle("recorder", args)
    
    args = {"args": ["Element", "-file", "forces.out", "-element", 1, 2, "force"], "kwargs": {}}
    manager.handle("recorder", args)
    
    return manager


def test_handles(recorder_manager: RecorderManager):
    """测试handles方法"""
    expected_commands = [
        'recorder', 'record', 'nodeDisp', 'nodeVel', 'nodeAccel',
        'nodeReaction', 'nodeResponse', 'eleForce', 'eleResponse',
        'getTime', 'getNodeTags', 'getEleTags', 'nodeCoord', 'nodeBounds',
        'printModel', 'printA', 'printB'
    ]
    handles = recorder_manager.handles()
    for cmd in expected_commands:
        assert cmd in handles


def test_recorder_node_command(recorder_manager: RecorderManager):
    """测试节点记录器命令解析"""
    args = {"args": ["Node", "-file", "output.out", "-time", "-node", 1, 2, 3, "disp"], "kwargs": {}}
    recorder_manager.handle("recorder", args)
    
    recorders = recorder_manager.get_recorders()
    assert len(recorders) == 1
    
    recorder = list(recorders.values())[0]
    assert recorder["type"] == "Node"
    assert recorder["output_file"] == "output.out"
    assert recorder["include_time"] == True
    assert recorder["nodes"] == [1, 2, 3]


def test_recorder_element_command(recorder_manager: RecorderManager):
    """测试单元记录器命令解析"""
    args = {"args": ["Element", "-file", "forces.out", "-element", 1, 2, "force"], "kwargs": {}}
    recorder_manager.handle("recorder", args)
    
    recorders = recorder_manager.get_recorders()
    assert len(recorders) == 1
    
    recorder = list(recorders.values())[0]
    assert recorder["type"] == "Element"
    assert recorder["output_file"] == "forces.out"
    assert recorder["elements"] == [1, 2]


def test_record_command(recorder_manager: RecorderManager):
    """测试record命令"""
    args = {"args": [], "kwargs": {}}
    recorder_manager.handle("record", args)
    
    assert recorder_manager.get_recording_trigger_count() == 1


def test_node_query_commands(recorder_manager: RecorderManager):
    """测试节点查询命令"""
    # 测试 nodeDisp
    args = {"args": ["1", "1"], "kwargs": {}}
    recorder_manager.handle("nodeDisp", args)
    
    # 测试 nodeVel
    args = {"args": ["1"], "kwargs": {}}
    recorder_manager.handle("nodeVel", args)
    
    queries = recorder_manager.get_output_queries()
    assert len(queries) == 2
    assert queries[0]["type"] == "node_query"
    assert queries[0]["command"] == "nodeDisp"
    assert queries[1]["command"] == "nodeVel"


def test_element_query_commands(recorder_manager: RecorderManager):
    """测试单元查询命令"""
    # 测试 eleForce
    args = {"args": ["1"], "kwargs": {}}
    recorder_manager.handle("eleForce", args)
    
    # 测试 eleResponse
    args = {"args": ["1", "force"], "kwargs": {}}
    recorder_manager.handle("eleResponse", args)
    
    queries = recorder_manager.get_output_queries()
    assert len(queries) == 2
    assert queries[0]["type"] == "element_query"
    assert queries[0]["command"] == "eleForce"
    assert queries[1]["command"] == "eleResponse"


def test_general_query_commands(recorder_manager: RecorderManager):
    """测试通用查询命令"""
    # 测试 getTime
    args = {"args": [], "kwargs": {}}
    recorder_manager.handle("getTime", args)
    
    # 测试 getNodeTags
    args = {"args": [], "kwargs": {}}
    recorder_manager.handle("getNodeTags", args)
    
    queries = recorder_manager.get_output_queries()
    assert len(queries) == 2
    assert queries[0]["type"] == "general_query"
    assert queries[0]["command"] == "getTime"
    assert queries[1]["command"] == "getNodeTags"


def test_print_commands(recorder_manager: RecorderManager):
    """测试打印命令"""
    # 测试 printModel with -JSON flag
    args = {"args": ["-JSON"], "kwargs": {}}
    recorder_manager.handle("printModel", args)
    
    # 测试 printA with file
    args = {"args": ["-file", "matrix.out"], "kwargs": {}}
    recorder_manager.handle("printA", args)
    
    queries = recorder_manager.get_output_queries()
    assert len(queries) == 2
    assert queries[0]["type"] == "print_command"
    assert queries[0]["command"] == "printModel"
    assert "json_flag" in queries[0]["options"]
    assert queries[1]["command"] == "printA"
    assert queries[1]["output_file"] == "matrix.out"


def test_get_recorders_by_type(configured_recorder_manager: RecorderManager):
    """测试按类型获取记录器"""
    node_recorders = configured_recorder_manager.get_recorders_by_type("Node")
    element_recorders = configured_recorder_manager.get_recorders_by_type("Element")
    
    assert len(node_recorders) == 1
    assert len(element_recorders) == 1
    assert node_recorders[0]["type"] == "Node"
    assert element_recorders[0]["type"] == "Element"


def test_clear(configured_recorder_manager: RecorderManager):
    """测试清除功能"""
    # 验证数据存在
    assert len(configured_recorder_manager.get_recorders()) > 0
    
    # 添加一些查询数据
    configured_recorder_manager.handle("record", {"args": [], "kwargs": {}})
    
    # 清除并验证
    configured_recorder_manager.clear()
    assert len(configured_recorder_manager.get_recorders()) == 0
    assert len(configured_recorder_manager.get_output_queries()) == 0
    assert configured_recorder_manager.get_recording_trigger_count() == 0 