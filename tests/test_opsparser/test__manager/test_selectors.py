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
    nodes = parser.node.sel(item='Tag', vmin=0).sel(type_=SelectType.ADD, item='Tag', vmin=2).collect()
    assert len(nodes) == 2
    
    # 测试移除选择
    nodes = parser.node.sel(item='Tag', vmin=1, vmax=3).sel(type_=SelectType.REMOVE, item='Tag', vmin=2).collect()
    assert len(nodes) == 1
    assert nodes[0][0] == 1
    assert nodes[0][1]["coords"][0] == 0.0
    
    # 测试重新选择
    nodes = parser.node.sel(item='NODE', vmin=1, vmax=4).sel(type_=SelectType.RESELECT, item='LOC', comp='X', vmin=0.0).collect()
    assert len(nodes) == 2
    assert all(node[1]["coords"][0] == 0.0 for node in nodes)
    
    # 测试反转选择
    nodes = parser.node.sel(item='NODE', vmin=1, vmax=2).sel(type_=SelectType.INVERT).collect()
    assert len(nodes) == 2
    assert all(node[1]["coords"][0] != 0.0 for node in nodes)
    
    # 测试径向距离选择
    nodes = parser.node.sel(item='RADIUS', vmin=0.0, vmax=1.0).collect()
    assert len(nodes) == 3  # 原点(0,0)和(1,0)和(0,1)
    
    # 测试角度选择
    nodes = parser.node.sel(item='ANGLE', vmin=0.0, vmax=45.0).collect()
    assert len(nodes) == 2  # (1,0)和(1,1)
    
    # 测试幅值选择
    nodes = parser.node.sel(item='MAGN', vmin=0.0, vmax=1.0).collect()
    assert len(nodes) == 3  # 原点(0,0)和(1,0)和(0,1)
    
    # 测试撤销操作
    selector = parser.node.sel()
    selector.sel(item='NODE', vmin=1, vmax=2)
    selector.sel(type_=SelectType.ADD, item='NODE', vmin=3)
    assert len(selector.collect()) == 3
    selector.undo()
    assert len(selector.collect()) == 2
    
    # 测试状态显示
    selector = parser.node.sel()
    selector.sel(item='NODE', vmin=1, vmax=2)
    selector.sel(type_=SelectType.STATUS)  # 应该打印选择状态

def test_element_selector():
    # 创建管理器
    node_manager = NodeManager()
    element_manager = ElementManager()
    material_manager = MaterialManager()
    
    # 设置管理器引用
    Selector.set_managers(
        node_manager=node_manager,
        element_manager=element_manager,
        material_manager=material_manager
    )
    
    # 创建一些测试节点和单元
    node_manager.handle("node", {"args": [1, 0.0, 0.0, 0.0], "kwargs": {"-ndf": 3}})
    node_manager.handle("node", {"args": [2, 1.0, 0.0, 0.0], "kwargs": {"-ndf": 3}})
    node_manager.handle("node", {"args": [3, 0.0, 1.0, 0.0], "kwargs": {"-ndf": 3}})
    
    element_manager.handle("element", {"args": ["truss", 1, 1, 2], "kwargs": {}})
    element_manager.handle("element", {"args": ["truss", 2, 2, 3], "kwargs": {}})
    
    # 测试基本选择
    elements = element_manager.sel().sel(item='ELEM', vmin=1, vmax=2).collect()
    assert len(elements) == 2
    
    # 测试类型选择
    elements = element_manager.sel().sel(item='TYPE', vmin='truss').collect()
    assert len(elements) == 2
    
    # 测试节点选择
    elements = element_manager.sel().sel(item='NODE', vmin=1).collect()
    assert len(elements) == 1
    assert elements[0][0] == 1  # 检查单元ID
    assert elements[0][1]["eleNodes"] == [1, 2]  # 检查单元数据
    
    # 测试链式选择
    elements = element_manager.sel().sel(item='TYPE', vmin='truss').sel(item='NODE', vmin=1).collect()
    assert len(elements) == 1
    
    # 测试添加选择
    elements = element_manager.sel().sel(item='ELEM', vmin=1).sel(type_=SelectType.ADD, item='ELEM', vmin=2).collect()
    assert len(elements) == 2
    
    # 测试移除选择
    elements = element_manager.sel().sel(item='ELEM', vmin=1, vmax=2).sel(type_=SelectType.REMOVE, item='ELEM', vmin=2).collect()
    assert len(elements) == 1
    assert elements[0][0] == 1
    assert elements[0][1]["eleTag"] == 1
    
    # 测试重新选择
    elements = element_manager.sel().sel(item='ELEM', vmin=1, vmax=2).sel(type_=SelectType.RESELECT, item='TYPE', vmin='truss').collect()
    assert len(elements) == 2
    
    # 测试反转选择
    elements = element_manager.sel().sel(item='ELEM', vmin=1).sel(type_=SelectType.INVERT).collect()
    assert len(elements) == 1
    assert elements[0][0] == 2
    assert elements[0][1]["eleTag"] == 2
    
    # 测试撤销操作
    selector = element_manager.sel()
    selector.sel(item='ELEM', vmin=1)
    selector.sel(type_=SelectType.ADD, item='ELEM', vmin=2)
    assert len(selector.collect()) == 2
    selector.undo()
    assert len(selector.collect()) == 1
    
    # 测试状态显示
    selector = element_manager.sel()
    selector.sel(item='ELEM', vmin=1)
    selector.sel(type_=SelectType.STATUS)  # 应该打印选择状态

def test_material_selector():
    # 创建管理器
    node_manager = NodeManager()
    element_manager = ElementManager()
    material_manager = MaterialManager()
    
    # 设置管理器引用
    Selector.set_managers(
        node_manager=node_manager,
        element_manager=element_manager,
        material_manager=material_manager
    )
    
    # 创建一些测试材料
    material_manager.handle("uniaxialMaterial", {"args": ["Elastic", 1, 200e9], "kwargs": {}})
    material_manager.handle("uniaxialMaterial", {"args": ["Elastic", 2, 210e9], "kwargs": {}})
    material_manager.handle("nDMaterial", {"args": ["ElasticIsotropic", 3, 200e9, 0.3], "kwargs": {}})
    
    # 测试基本选择
    materials = material_manager.sel().sel(item='MAT', vmin=1, vmax=2).collect()
    assert len(materials) == 2
    
    # 测试类型选择
    materials = material_manager.sel().sel(item='TYPE', vmin='Elastic').collect()
    assert len(materials) == 2
    
    # 测试类别选择
    materials = material_manager.sel().sel(item='CATEGORY', vmin='uniaxial').collect()
    assert len(materials) == 2
    
    # 测试属性选择
    materials = material_manager.sel().sel(item='PROP', comp='E', vmin=200e9).collect()
    assert len(materials) == 2
    
    # 测试链式选择
    materials = material_manager.sel().sel(item='CATEGORY', vmin='uniaxial').sel(item='PROP', comp='E', vmin=200e9).collect()
    assert len(materials) == 2
    
    # 测试添加选择
    materials = material_manager.sel().sel(item='MAT', vmin=1).sel(type_=SelectType.ADD, item='MAT', vmin=2).collect()
    assert len(materials) == 2
    
    # 测试移除选择
    materials = material_manager.sel().sel(item='MAT', vmin=1, vmax=2).sel(type_=SelectType.REMOVE, item='MAT', vmin=2).collect()
    assert len(materials) == 1
    assert materials[0]["matTag"] == 1
    
    # 测试重新选择
    materials = material_manager.sel().sel(item='MAT', vmin=1, vmax=3).sel(type_=SelectType.RESELECT, item='TYPE', vmin='Elastic').collect()
    assert len(materials) == 2
    
    # 测试反转选择
    materials = material_manager.sel().sel(item='MAT', vmin=1).sel(type_=SelectType.INVERT).collect()
    assert len(materials) == 2
    assert all(mat["matTag"] in [2, 3] for mat in materials)
    
    # 测试撤销操作
    selector = material_manager.sel()
    selector.sel(item='MAT', vmin=1)
    selector.sel(type_=SelectType.ADD, item='MAT', vmin=2)
    assert len(selector.collect()) == 2
    selector.undo()
    assert len(selector.collect()) == 1
    
    # 测试状态显示
    selector = material_manager.sel()
    selector.sel(item='MAT', vmin=1)
    selector.sel(type_=SelectType.STATUS)  # 应该打印选择状态

def test_cross_manager_selection():
    # 创建管理器
    node_manager = NodeManager()
    element_manager = ElementManager()
    material_manager = MaterialManager()
    
    # 设置管理器引用
    Selector.set_managers(
        node_manager=node_manager,
        element_manager=element_manager,
        material_manager=material_manager
    )
    
    # 创建测试数据
    node_manager.handle("node", {"args": [1, 0.0, 0.0, 0.0], "kwargs": {"-ndf": 3}})
    node_manager.handle("node", {"args": [2, 1.0, 0.0, 0.0], "kwargs": {"-ndf": 3}})
    
    material_manager.handle("uniaxialMaterial", {"args": ["Elastic", 1, 200e9], "kwargs": {}})
    
    element_manager.handle("element", {"args": ["truss", 1, 1, 2], "kwargs": {"-mat": 1}})
    
    # 测试跨管理器查询
    # 1. 获取使用特定材料的所有单元
    elements = material_manager.sel().by_type("Elastic").used_by_elements()
    assert len(elements) == 1
    assert elements[0] == 1
    
    # 2. 获取与特定节点连接的所有单元
    elements = node_manager.sel().by_coords(x=0.0).connected_elements()
    assert len(elements) == 1
    assert elements[0] == 1
    
    # 3. 获取与特定单元连接的所有节点
    nodes = element_manager.sel().by_type("truss").connected_nodes()
    assert len(nodes) == 2
    assert 1 in nodes
    assert 2 in nodes 