"""
Tests for BlockManager

This module tests the BlockManager class which handles
OpenSeesPy block commands.
"""

import pytest
from typing import Dict, Any

from opsparser._manager._BlockManager import BlockManager


@pytest.fixture
def block_manager() -> BlockManager:
    """每个测试前初始化一个BlockManager实例"""
    manager = BlockManager()
    manager.clear()
    return manager


def test_block2d_command_parsing(block_manager: BlockManager):
    """测试block2D命令解析"""
    arg_map = {
        "nx": 2,
        "ny": 3,
        "start_node": 1,
        "start_ele": 10,
        "ele_type": "quad",
        "ele_args": [1, 2, 3, 4]
    }
    block_manager._handle_block2d(arg_map)
    
    # 验证块是否存储
    block = block_manager.get_block("2D_1_10")
    assert block is not None
    assert block["type"] == "block2D"
    assert block["dimensions"]["nx"] == 2
    assert block["dimensions"]["ny"] == 3
    
    # 检查生成的节点计算
    assert len(block["generated_nodes"]) == (2+1) * (3+1)  # (nx+1) * (ny+1)


def test_block3d_command_parsing(block_manager: BlockManager):
    """测试block3D命令解析"""
    arg_map = {
        "nx": 2, "ny": 2, "nz": 2,
        "start_node": 1, "start_ele": 10,
        "ele_type": "brick", "ele_args": []
    }
    block_manager._handle_block3d(arg_map)
    
    # 验证块是否存储
    block = block_manager.get_block("3D_1_10")
    assert block is not None
    assert block["type"] == "block3D"
    
    # 检查生成的节点计算
    assert len(block["generated_nodes"]) == (2+1) * (2+1) * (2+1)  # (nx+1) * (ny+1) * (nz+1)


if __name__ == "__main__":
    pytest.main([__file__]) 