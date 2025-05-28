"""
Tests for ConstraintManager

This module tests the ConstraintManager class which handles
OpenSeesPy constraint commands.
"""

import pytest
from typing import Dict, Any

from opsparser._manager._ConstraintManager import ConstraintManager


@pytest.fixture
def constraint_manager() -> ConstraintManager:
    """每个测试前初始化一个ConstraintManager实例"""
    manager = ConstraintManager()
    manager.clear()
    return manager


def test_fix_command(constraint_manager: ConstraintManager):
    """测试fix命令"""
    arg_map = {"args": [1, 1, 1, 0], "kwargs": {}}
    constraint_manager.handle("fix", arg_map)
    
    # 验证约束是否存储
    constraint = constraint_manager.get_sp_constraint(1)
    assert constraint is not None
    assert constraint["type"] == "fix"
    assert constraint["node_tag"] == 1
    assert constraint["constraints"] == [1, 1, 0]


def test_equal_dof_command(constraint_manager: ConstraintManager):
    """测试equalDOF命令解析"""
    arg_map = {"args": [1, 2, 1, 2], "kwargs": {}}
    constraint_manager.handle("equalDOF", arg_map)
    
    # 验证MP约束是否存储
    mp_constraints = constraint_manager.get_mp_constraints()
    assert len(mp_constraints) == 1
    assert mp_constraints[0]["type"] == "equalDOF"
    assert mp_constraints[0]["retained_node"] == 1
    assert mp_constraints[0]["constrained_node"] == 2


def test_pressure_constraint_command(constraint_manager: ConstraintManager):
    """测试pressureConstraint命令解析"""
    arg_map = {"args": [1, 2, 100.0], "kwargs": {}}
    constraint_manager.handle("pressureConstraint", arg_map)
    
    # 验证压力约束是否存储
    pressure_constraints = constraint_manager.get_pressure_constraints()
    assert len(pressure_constraints) == 1
    assert pressure_constraints[0]["type"] == "pressureConstraint"
    assert pressure_constraints[0]["ele_tag1"] == 1
    assert pressure_constraints[0]["ele_tag2"] == 2
    assert pressure_constraints[0]["pressure"] == 100.0


if __name__ == "__main__":
    pytest.main([__file__]) 