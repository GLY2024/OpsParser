"""
Tests for BeamIntegrationManager

This module tests the BeamIntegrationManager class which handles
OpenSeesPy beamIntegration commands.
"""

import pytest
from typing import Dict, Any

from opsparser._manager._BeamIntegrationManager import BeamIntegrationManager


@pytest.fixture
def beam_integration_manager() -> BeamIntegrationManager:
    """每个测试前初始化一个BeamIntegrationManager实例"""
    manager = BeamIntegrationManager()
    manager.clear()
    return manager


@pytest.fixture
def configured_beam_integration_manager() -> BeamIntegrationManager:
    """每个测试前初始化一个配置好的BeamIntegrationManager实例"""
    manager = BeamIntegrationManager()
    manager.clear()
    
    # 添加使用截面10的积分
    arg_map1 = {"integration_type": "Lobatto", "tag": 1, "args": [10, 5]}
    arg_map2 = {"integration_type": "Legendre", "tag": 2, "args": [10, 3]}
    arg_map3 = {"integration_type": "Lobatto", "tag": 3, "args": [20, 4]}
    
    manager._handle_beam_integration(arg_map1)
    manager._handle_beam_integration(arg_map2)
    manager._handle_beam_integration(arg_map3)
    
    return manager


def test_beam_integration_command_parsing(beam_integration_manager: BeamIntegrationManager):
    """测试beamIntegration命令解析"""
    arg_map = {
        "integration_type": "Lobatto",
        "tag": 1,
        "args": [10, 5]  # secTag, N
    }
    beam_integration_manager._handle_beam_integration(arg_map)
    
    # 验证积分是否存储
    integration = beam_integration_manager.get_integration(1)
    assert integration is not None
    assert integration["type"] == "Lobatto"
    assert integration["sec_tag"] == 10
    assert integration["N"] == 5


def test_get_integrations_using_section(configured_beam_integration_manager: BeamIntegrationManager):
    """测试获取使用特定截面的积分"""
    # 获取使用截面10的积分
    integrations = configured_beam_integration_manager.get_integrations_using_section(10)
    assert len(integrations) == 2


if __name__ == "__main__":
    pytest.main([__file__]) 