# xara 命令解析兼容设计

> 状态：设计稿（部分基础设施已落地）
> 目标：让 OpsParser 既能解析 `openseespy.opensees` 模块式命令，也能解析
> [xara](https://xara.so)（STAIRLab 维护的 OpenSees 现代封装）的命令调用。

## 1. 背景：xara 与 openseespy 的差异

xara（`pip install xara`，包名 `opensees`）对 OpenSees 内核做了重新封装，
与 openseespy 相比有三类差异：

| 差异 | openseespy | xara |
| --- | --- | --- |
| 调用形态 | 模块级函数 `ops.node(...)` | `Model` 对象方法 `model.node(...)`（无全局状态，可多模型并存） |
| 参数风格 | 扁平位置参数 + Tcl 风格 `-flag` 选项 | 同时支持扁平风格、关键字参数（如 `model.node(1, (0.0, 0.0))` 坐标元组）与 kwargs（如 `section=...`） |
| 兼容层 | — | `opensees.openseespy` 提供与 openseespy 同名的模块级 API |

因此兼容工作可以分层进行，**数据模型层（各 Manager / Handler）完全复用**，
只需在"挂钩层"和"参数规范化层"做适配。

## 2. 总体架构

```
用户代码 (openseespy 模块 / xara.Model 实例)
        │
        ▼
┌──────────────────────────────┐
│ ① 挂钩层 hook_all             │  模块函数 与 实例方法 统一拦截
├──────────────────────────────┤
│ ② 参数规范化层 (新增)          │  kwargs/嵌套序列 → 扁平 openseespy 风格
├──────────────────────────────┤
│ ③ 命令别名层 (新增)            │  xara 独有命名 → 规范命令名
├──────────────────────────────┤
│ ④ 分发与解析 (现有, 不变)      │  dispatch_table → Manager._parse
├──────────────────────────────┤
│ ⑤ 数据存储 (现有, 不变)        │  NodeManager.nodes / ElementManager.elements ...
└──────────────────────────────┘
```

### 2.1 挂钩层（已实现）

`OpenSeesParser.hook_all` 不再假定目标是模块：`_HOOKABLE_TYPES` 同时覆盖
`FunctionType` / `BuiltinFunctionType`（模块函数）与 `MethodType` /
`MethodWrapperType`（实例绑定方法），因此下列两种用法都能工作：

```python
# openseespy（现状）
parser = OpenSeesParser(ops); parser.hook_all()

# xara（目标用法）
model = xara.Model(ndm=2, ndf=3)
parser = OpenSeesParser(model); parser.hook_all()
```

对实例做 `setattr(instance, name, wrapper)` 会以实例属性遮蔽类方法，
不污染 `xara.Model` 类本身；`restore_all()` 删除实例属性即可还原。
重复挂钩通过 `__opsparser_original__` 标记自动解包重包，保证永远只有一层包装。

### 2.2 参数规范化层（待实现）

xara 风格调用需在进入 `handler.handle` 之前规范化为 openseespy 扁平风格，
建议在 `_hook_function` 的 wrapper 中插入一个可插拔的 normalizer：

```python
class ArgNormalizer:
    def normalize(self, func_name: str, args: tuple, kwargs: dict) -> tuple[tuple, dict]:
        ...

class XaraArgNormalizer(ArgNormalizer):
    """1. 展开嵌套坐标/节点元组: node(1, (0.,0.)) -> node(1, 0., 0.)
       2. kwargs 直通: BaseHandler._parse 已让 kwargs 覆盖位置解析结果,
          xara 的 section=1 等关键字天然兼容, 只需做键名映射(见 2.3)
       3. 规范化数值类型(xara 接受 numpy 标量/数组)"""
```

`OpenSeesParser(target, normalizer=None)`，默认 `None` 表示直通（openseespy
行为完全不变）；检测到 target 是 `xara.Model` 时自动选用 `XaraArgNormalizer`。

### 2.3 命令与参数别名层（待实现）

少数命令/参数在 xara 中改名或扩展，集中维护一张别名表而不是改各 Handler：

```python
XARA_COMMAND_ALIASES = {
    # "xara 命令名": "规范命令名"
}
XARA_KWARG_ALIASES = {
    "element": {"material": "matTag", "section": "secTag", "transform": "transfTag"},
    ...
}
```

别名表为纯数据，便于随 xara 版本演进单独更新与单测。

### 2.4 `Model` 构造参数

xara 在 `Model(ndm=2, ndf=3)` 构造时即确定模型维度，不经过 `model()` 命令。
而部分 Handler（BeamColumn、ZeroLength 等）的解析规则依赖 `ops.getNDM()`。
适配方案：

1. 抽象出 `ModelContext`（保存 ndm/ndf），由挂钩层在挂接时写入：
   - openseespy：继续从 `model` 命令/`getNDM()` 获取；
   - xara：挂接 `Model` 实例时直接读 `model.getNDM()`（xara 同样提供该查询）。
2. Handler 内部统一改为从 `ModelContext` 取 ndm，避免直接 import openseespy。

## 3. 渐进式路线图

| 阶段 | 内容 | 状态 |
| --- | --- | --- |
| P0 | 挂钩层支持实例方法；重复挂钩防护 | ✅ 已完成 |
| P1 | `ModelContext` 抽象，移除 Handler 对 `openseespy` 的直接依赖 | 待做 |
| P2 | `ArgNormalizer` 插件点 + `XaraArgNormalizer`（坐标元组展开、kwargs 键名映射） | 待做 |
| P3 | 别名表 + 针对 xara 实际运行结果的回归测试（CI 可选安装 `xara`） | 待做 |
| P4 | 文档与示例（`OpenSeesParser(xara.Model(...))` 快速上手） | 待做 |

## 4. 测试策略

- **单元层**：用 FakeModel（模拟 xara.Model 的绑定方法接口）测试挂钩层，
  不依赖 xara 安装（见 `tests/test_opsparser/test_systematic_validation.py`
  中的对象挂钩测试）。
- **规则层**：现有 `tests/rule_audit.py` 规则审计与目标解释器无关，
  P2 之后对规范化层补充 xara 风格输入 → 扁平输出的等价性断言。
- **集成层**：CI 中以可选依赖安装 xara，将现有 openseespy 集成测试
  在 `opensees.openseespy` 兼容模块与 `xara.Model` 两种形态下复跑，
  以实际运行结果为准（与 openseespydoc / OpenSees wiki 交叉核对）。
