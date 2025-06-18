import pytest
import openseespy.opensees as ops
from opsparser import OpenSeesParser
from opsparser._manager._selector._Selector import SelectType, Selector
from opsparser._manager._NodeManager import NodeManager
from opsparser._manager._ElementManager import ElementManager
from opsparser._manager._MaterialManager import MaterialManager

@pytest.fixture
def parser():
    parser = OpenSeesParser(ops)
    parser.hook_all(debug = True)
    ops.wipe()
    ops.model('basic', '-ndm', 3, '-ndf', 6)
    return parser

def test_node_selector(parser: OpenSeesParser):
    # 创建一些测试节点
    ops.node(1, 0.0, 0.0, 0.0)
    ops.node(2, 1.0, 0.0, 0.0)
    ops.node(3, 0.0, 1.0, 0.0)
    ops.node(4, 1.0, 1.0, 0.0)
    
    # 测试基本选择
    nodes = parser.node.sel(item='Tag', vmin=1, vmax=2).collect()
    assert len(nodes) == 2
    assert nodes[0][0] == 1  # 检查节点ID
    assert nodes[0][1]["coords"][0] == 0.0  # 检查节点数据
    assert nodes[1][0] == 2
    assert nodes[1][1]["coords"][0] == 1.0
    
    # 测试坐标选择
    nodes = parser.node.sel(item='Coord', comp='X', vmin=0.0, vmax=0.0).collect()
    assert len(nodes) == 2
    assert all(node[1]["coords"][0] == 0.0 for node in nodes)
    
    # 测试链式选择
    nodes = parser.node.sel(item='Coord', comp='X', vmin=0.0).sel(item='Coord', comp='Y', vmin=0.0).collect()
    print(nodes)
    assert len(nodes) == 1
    assert nodes[0][0] == 1
    assert nodes[0][1]["coords"] == [0.0, 0.0, 0.0]
    
    # 测试添加选择
    nodes = parser.node.sel(item='Tag', vmin=1).sel(type=SelectType.ADD, item='Tag', vmin=2).collect()
    assert len(nodes) == 2
    
    # 测试移除选择
    nodes = parser.node.sel(item='Tag', vmin=1, vmax=2).sel(type=SelectType.REMOVE, item='Tag', vmin=2).collect()
    assert len(nodes) == 1
    assert nodes[0][0] == 1
    assert nodes[0][1]["coords"][0] == 0.0
    
    # 测试重新选择
    nodes = parser.node.sel(item='Tag', vmin=1, vmax=4).sel(type=SelectType.RESELECT, item='Coord', comp='X', vmin=0.0, tol=1e-6).collect()
    assert len(nodes) == 2
    assert all(node[1]["coords"][0] == 0.0 for node in nodes)
    
    # 测试反转选择
    nodes = parser.node.sel(item='Tag', vmin=1, vmax=2).sel(type=SelectType.INVERT).collect()
    assert len(nodes) == 2
    assert all(node[0] not in [1, 2] for node in nodes)
    
    # 测试径向距离选择
    nodes = parser.node.sel(item='Radius', vmin=0.0, vmax=1.0).collect()
    assert len(nodes) == 3  # 原点(0,0)和(1,0)和(0,1)
    
    # 测试撤销操作
    selector = parser.node.sel()
    selector.sel(item='Tag', vmin=1, vmax=2)
    selector.sel(type=SelectType.ADD, item='Tag', vmin=3)
    assert len(selector.collect()) == 3
    selector.undo()
    assert len(selector.collect()) == 2
    
    # 测试状态显示
    selector = parser.node.sel(item='Tag', vmin=1, vmax=2)
    selector.sel(type=SelectType.STATUS)  # 应该打印选择状态


def test_element_selector(parser: OpenSeesParser):
    # 创建一些测试节点
    ops.node(1, 0.0, 0.0, 0.0)
    ops.node(2, 1.0, 0.0, 0.0)
    ops.node(3, 0.0, 1.0, 0.0)
    ops.node(4, 1.0, 1.0, 0.0)
    
    # 创建一些测试材料
    ops.uniaxialMaterial('Elastic', 1, 200e9)
    ops.uniaxialMaterial('Elastic', 2, 210e9)
    
    # 创建一些测试单元
    ops.element("Truss", 1, 1, 2, 0.01, 1)
    ops.element('Truss', 2, 2, 3, 0.01, 2)
    ops.element('Truss', 3, 3, 4, 0.01, 1)
    
    # 测试基本选择
    elements = parser.element.sel(item='Tag', vmin=1, vmax=2).collect()
    assert len(elements) == 2
    assert elements[0][0] == 1  # 检查单元ID
    assert elements[0][1]["eleTag"] == 1  # 检查单元数据
    assert elements[1][0] == 2
    assert elements[1][1]["eleTag"] == 2
    
    # 测试类型选择
    elements = parser.element.sel(item='Type', vmin='Truss').collect()
    assert len(elements) == 3
    
    # 测试材料选择
    print(parser.element.elements)
    elements = parser.element.sel(item='Material', vmin=1, vmax=1).collect()
    assert len(elements) == 2
    assert all(elem[1]["matTag"] == 1 for elem in elements)
    
    # 测试节点选择
    elements = parser.element.sel(item='Tag', vmin=1).collect()
    assert len(elements) == 1
    assert elements[0][0] == 1  # 检查单元ID
    assert elements[0][1]["eleNodes"] == [1, 2]  # 检查单元数据
    
    # 测试链式选择
    elements = parser.element.sel(item='Type', vmin='Truss').sel(item='Material', vmin=1).collect()
    assert len(elements) == 2
    
    # 测试添加选择
    elements = parser.element.sel(item='Tag', vmin=1).sel(type=SelectType.ADD, item='Tag', vmin=2).collect()
    assert len(elements) == 2
    
    # 测试移除选择
    elements = parser.element.sel(item='Tag', vmin=1, vmax=2).sel(type=SelectType.REMOVE, item='Tag', vmin=2).collect()
    assert len(elements) == 1
    assert elements[0][0] == 1
    assert elements[0][1]["eleTag"] == 1
    
    # 测试重新选择
    elements = parser.element.sel(item='Tag', vmin=1, vmax=3).sel(type=SelectType.RESELECT, item='Type', vmin='Truss').collect()
    assert len(elements) == 3
    
    # 测试反转选择
    elements = parser.element.sel(item='Tag', vmin=1).sel(type=SelectType.INVERT).collect()
    assert len(elements) == 2
    assert all(elem[0] not in [1] for elem in elements)
    
    # 测试撤销操作
    selector = parser.element.sel(item='Tag', vmin=1, vmax=2)
    selector.sel(type=SelectType.ADD, item='Tag', vmin=3)
    assert len(selector.collect()) == 3
    selector.undo()
    assert len(selector.collect()) == 2
    
    # 测试状态显示
    selector = parser.element.sel(item='Tag', vmin=1, vmax=2)
    selector.sel(type=SelectType.STATUS)  # 应该打印选择状态

def test_material_selector(parser: OpenSeesParser):
    # 创建一些测试材料
    ops.uniaxialMaterial('Elastic', 1, 200e9)
    ops.uniaxialMaterial('Elastic', 2, 210e9)
    ops.nDMaterial('ElasticIsotropic', 3, 200e9, 0.3)
    
    # 测试基本选择
    materials = parser.material.sel(item='Tag', vmin=1, vmax=2).collect()
    assert len(materials) == 2
    assert materials[0][0] == 1  # 检查材料ID
    assert materials[0][1]["matTag"] == 1  # 检查材料数据
    assert materials[1][0] == 2
    assert materials[1][1]["matTag"] == 2
    
    # 测试类型选择
    materials = parser.material.sel(item='Type', vmin='Elastic').collect()
    assert len(materials) == 2
    
    # 测试类别选择
    materials = parser.material.sel(item='Category', vmin='uniaxial').collect()
    assert len(materials) == 2
    
    # 测试属性选择
    materials = parser.material.sel(item='Property', comp='E', vmin=200e9).collect()
    assert len(materials) == 2
    
    # 测试链式选择
    materials = parser.material.sel(item='Category', vmin='uniaxial').sel(item='Property', comp='E', vmin=200e9).collect()
    assert len(materials) == 1
    
    # 测试添加选择
    materials = parser.material.sel(item='Tag', vmin=1).sel(type=SelectType.ADD, item='Tag', vmin=2).collect()
    assert len(materials) == 2
    
    # 测试移除选择
    materials = parser.material.sel(item='Tag', vmin=1, vmax=2).sel(type=SelectType.REMOVE, item='Tag', vmin=2).collect()
    assert len(materials) == 1
    assert materials[0][0] == 1
    assert materials[0][1]["matTag"] == 1
    
    # 测试重新选择
    materials = parser.material.sel(item='Tag', vmin=1, vmax=3).sel(type=SelectType.RESELECT, item='Type', vmin='Elastic').collect()
    assert len(materials) == 2
    
    # 测试反转选择
    materials = parser.material.sel(item='Tag', vmin=1).sel(type=SelectType.INVERT).collect()
    assert len(materials) == 2
    assert all(mat[0] in [2, 3] for mat in materials)
    
    # 测试撤销操作
    selector = parser.material.sel(item='Tag', vmin=1)
    selector.sel(type=SelectType.ADD, item='Tag', vmin=2)
    assert len(selector.collect()) == 2
    selector.undo()
    assert len(selector.collect()) == 1
    
    # 测试状态显示
    selector = parser.material.sel(item='Tag', vmin=1, vmax=2)
    selector.sel(type=SelectType.STATUS)  # 应该打印选择状态

def test_cross_manager_selection(parser: OpenSeesParser):
    # 创建测试数据
    ops.node(1, 0.0, 0.0, 0.0)
    ops.node(2, 1.0, 0.0, 0.0)
    
    ops.uniaxialMaterial('Elastic', 1, 200e9)
    
    ops.element('Truss', 1, 1, 2, 0.01, 1)
    
    # 测试跨管理器查询
    # 1. 获取使用特定材料的所有单元（sel（）默认全选）
    elements = parser.material.sel().by_type("Elastic").used_by_elements()
    assert len(elements) == 1
    assert elements[0] == 1
    
    # 2. 获取与特定节点连接的所有单元
    elements = parser.node.sel().by_coords(x=0.0).get_connected_elements()
    assert len(elements) == 1
    assert elements[0] == 1
    
    # 3. 获取与特定单元连接的所有节点
    nodes = parser.element.sel().by_type("Truss").connected_nodes()
    assert len(nodes) == 2
    assert 1 in nodes
    assert 2 in nodes 