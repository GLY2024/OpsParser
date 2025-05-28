"""
Tests for FrictionModelManager

This module tests the FrictionModelManager class which handles
OpenSeesPy frictionModel commands.
"""

import pytest
from typing import Dict, Any

from opsparser._manager._FrictionModelManager import FrictionModelManager


@pytest.fixture
def friction_model_manager() -> FrictionModelManager:
    """每个测试前初始化一个FrictionModelManager实例"""
    manager = FrictionModelManager()
    manager.clear()
    return manager


def test_friction_model_command_parsing(friction_model_manager: FrictionModelManager):
    """测试frictionModel命令解析"""
    arg_map = {
        "model_type": "Coulomb",
        "tag": 1,
        "args": [0.3]  # mu
    }
    friction_model_manager._handle_friction_model(arg_map)
    
    # 验证摩擦模型是否存储
    model = friction_model_manager.get_friction_model(1)
    assert model is not None
    assert model["type"] == "Coulomb"
    assert model["mu"] == 0.3


def test_vel_dependent_friction_model(friction_model_manager: FrictionModelManager):
    """测试VelDependent摩擦模型解析"""
    arg_map = {
        "model_type": "VelDependent",
        "tag": 2,
        "args": [0.2, 0.1, 50.0]  # muSlow, muFast, transRate
    }
    friction_model_manager._handle_friction_model(arg_map)
    
    # 验证摩擦模型是否存储
    model = friction_model_manager.get_friction_model(2)
    assert model is not None
    assert model["type"] == "VelDependent"
    assert model["mu_slow"] == 0.2
    assert model["mu_fast"] == 0.1
    assert model["trans_rate"] == 50.0


if __name__ == "__main__":
    pytest.main([__file__]) 