"""Systematic validation of every command parser.

Three layers of checks:
1. Rule audit - synthesize argument combinations (positional only, each
   option alone, all options together) for *every* rule of *every* handler
   and verify ``_parse`` round-trips them (2D and 3D models).
2. Real-run combination tests - replay documented parameter combinations of
   timeSeries / pattern / load / eleLoad through a live openseespy module
   (run results are the source of truth) and verify the captured state.
3. Hook robustness - `wipe` must reset every manager singleton and
   repeated `hook_all` must not double-dispatch commands.
"""
import pytest
import openseespy.opensees as ops

from opsparser import OpenSeesParser
from tests.rule_audit import run_audit


# ---------------------------------------------------------------------------
# 1. Rule-driven audit over all handlers
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("ndm,ndf", [(2, 3), (3, 6)])
def test_rule_audit_all_handlers(ndm, ndf):
    report, counts = run_audit(ndm, ndf)
    issues = [f"{h}: {msg}" for h, msgs in report.items() for msg in msgs]
    assert counts["rules"] > 400, "rule discovery looks broken"
    assert not issues, "\n".join(issues)


# ---------------------------------------------------------------------------
# 2. Real-run combination tests
# ---------------------------------------------------------------------------
@pytest.fixture
def parser():
    p = OpenSeesParser(ops)
    p.hook_all()
    ops.wipe()
    p.clear()
    ops.model("basic", "-ndm", 2, "-ndf", 3)
    return p


TIME_SERIES_CASES = [
    # (args, expected subset of stored info)
    (("Constant", 1), {"type": "Constant"}),
    (("Constant", 2, "-factor", 1.5), {"factor": 1.5}),
    (("Constant", 3, 2.5), {"factor": 2.5}),  # positional factor (accepted by OpenSees)
    (("Linear", 4), {"type": "Linear"}),
    (("Linear", 5, "-factor", 2.0), {"factor": 2.0}),
    (("Trig", 6, 0.0, 10.0, 1.0), {"tStart": 0.0, "tEnd": 10.0, "period": 1.0}),
    (("Trig", 7, 0.0, 10.0, 1.0, "-factor", 1.2, "-shift", 0.5, "-zeroShift", 0.1),
     {"factor": 1.2, "shift": 0.5, "zeroShift": 0.1}),
    (("Triangle", 8, 0.0, 10.0, 2.0, "-factor", 0.8), {"period": 2.0, "factor": 0.8}),
    (("Rectangular", 9, 1.0, 5.0, "-factor", 3.0), {"tStart": 1.0, "tEnd": 5.0, "factor": 3.0}),
    (("Pulse", 10, 0.0, 10.0, 1.0, "-width", 0.3, "-shift", 0.1, "-factor", 1.1),
     {"width": 0.3, "shift": 0.1, "factor": 1.1}),
    (("Path", 11, "-dt", 0.1, "-values", 1.0, 2.0, 3.0, "-factor", 1.5),
     {"dt": 0.1, "values": [1.0, 2.0, 3.0], "factor": 1.5}),
    (("Path", 12, "-time", 0.0, 1.0, 2.0, "-values", 1.0, 2.0, 3.0),
     {"time": [0.0, 1.0, 2.0], "values": [1.0, 2.0, 3.0]}),
    (("Path", 13, "-dt", 0.1, "-values", 1.0, 2.0, "-useLast", "-prependZero"),
     {"useLast": True, "prependZero": True}),
    (("Path", 14, "-dt", 0.1, "-values", 1.0, 2.0, "-startTime", 5.0),
     {"startTime": 5.0}),
]


@pytest.mark.parametrize("args,expected", TIME_SERIES_CASES,
                         ids=[f"{c[0][0]}-{c[0][1]}" for c in TIME_SERIES_CASES])
def test_time_series_combinations(parser: OpenSeesParser, args, expected):
    ops.timeSeries(*args)  # real run: openseespy must accept it
    info = parser.timeseries.get_time_series(args[1])
    assert info, f"timeSeries {args} was not captured"
    assert info["tag"] == args[1]
    for key, value in expected.items():
        assert info.get(key) == value, f"{key}: expected {value}, got {info.get(key)}"


def test_pattern_combinations(parser: OpenSeesParser):
    ops.timeSeries("Linear", 1)
    ops.timeSeries("Path", 2, "-dt", 0.1, "-values", 0.0, 1.0, 0.0)

    ops.pattern("Plain", 1, 1)
    assert parser.load.get_pattern(1) == {"type": "Plain", "tag": 1, "tsTag": 1}

    ops.pattern("Plain", 2, 1, "-fact", 2.0)
    assert parser.load.get_pattern(2)["factor"] == 2.0

    ops.pattern("UniformExcitation", 3, 1, "-accel", 2, "-fact", 1.5)
    info = parser.load.get_pattern(3)
    assert info["type"] == "UniformExcitation"
    assert info["dir"] == 1
    assert info["accelSeriesTag"] == 2
    assert info["factor"] == 1.5

    ops.pattern("MultipleSupport", 4)
    assert parser.load.get_pattern(4)["type"] == "MultipleSupport"

    assert parser.load.get_patterns_by_time_series(1) == [1, 2]


def test_load_and_eleload_combinations(parser: OpenSeesParser):
    ops.node(1, 0.0, 0.0)
    ops.node(2, 1.0, 0.0)
    ops.node(3, 2.0, 0.0)
    ops.geomTransf("Linear", 1)
    ops.section("Elastic", 1, 200e9, 0.01, 1e-4)
    ops.beamIntegration("Lobatto", 1, 1, 3)
    ops.element("forceBeamColumn", 1, 1, 2, 1, 1)
    ops.element("forceBeamColumn", 2, 2, 3, 1, 1)
    ops.timeSeries("Linear", 1)
    ops.pattern("Plain", 1, 1)

    # node load
    ops.load(2, 1.0, -2.0, 3.0)
    assert parser.load.get_node_load(1, 2) == [1.0, -2.0, 3.0]
    assert parser.load.get_loads_by_node(2) == [
        {"pattern_tag": 1, "node_tag": 2, "forces": [1.0, -2.0, 3.0]}
    ]

    # eleLoad: -ele with single tag, uniform load (2D: Wy <Wx>)
    ops.eleLoad("-ele", 1, "-type", "-beamUniform", -10.0)
    assert parser.load.get_ele_load(1, 1) == {"type": "beamUniform", "values": [-10.0]}

    # eleLoad: -ele with multiple tags and 2 components
    ops.eleLoad("-ele", 1, 2, "-type", "-beamUniform", -10.0, 5.0)
    assert parser.load.get_ele_load(1, 1)["values"] == [-10.0, 5.0]
    assert parser.load.get_ele_load(1, 2)["values"] == [-10.0, 5.0]

    # eleLoad: -range, point load (2D: Py xL <Px>)
    ops.eleLoad("-range", 1, 2, "-type", "-beamPoint", -5.0, 0.5)
    assert parser.load.get_ele_load(1, 1) == {"type": "beamPoint", "values": [-5.0, 0.5]}
    assert parser.load.get_ele_load(1, 2) == {"type": "beamPoint", "values": [-5.0, 0.5]}

    loads = parser.load.get_element_loads()
    assert {load["element_tag"] for load in loads} == {1, 2}
    assert all(load["load_type"] == "beamPoint" for load in loads)


# ---------------------------------------------------------------------------
# 3. Hook robustness
# ---------------------------------------------------------------------------
def test_wipe_clears_all_managers(parser: OpenSeesParser):
    ops.node(1, 0.0, 0.0)
    ops.uniaxialMaterial("Elastic", 1, 200e9)
    ops.timeSeries("Linear", 1)
    ops.pattern("Plain", 1, 1)
    ops.load(1, 1.0, 1.0, 0.0)

    assert parser.node.nodes
    assert parser.material.materials
    assert parser.timeseries.time_series
    assert parser.load.patterns

    ops.wipe()

    assert not parser.node.nodes
    assert not parser.material.materials
    assert not parser.timeseries.time_series
    assert not parser.load.patterns
    assert not parser.load.node_loads
    assert parser.load.current_pattern is None


def test_hook_all_is_idempotent(parser: OpenSeesParser):
    # hooking again (same or new parser instance) must not double-dispatch
    parser.hook_all()
    p2 = OpenSeesParser(ops)
    p2.hook_all()

    # commands are appended to utility_history once per dispatch, so a
    # double-wrapped module would record this command more than once
    before = len(parser.utility.utility_history)
    ops.setTime(0.5)
    assert len(parser.utility.utility_history) - before == 1

    # the newest hooking parser owns the call log; exactly one entry
    p2.call_log.clear()
    ops.node(1, 0.0, 0.0)
    assert len(p2.call_log["node"]) == 1
    assert parser.node.get_node_coords(1) == [0.0, 0.0]


def test_hook_object_style_interpreter():
    """Instance-bound methods (xara.Model style) can be hooked too."""

    class FakeModel:
        def __init__(self):
            self.executed = []

        def node(self, tag, *coords):
            self.executed.append(("node", tag, coords))

        def timeSeries(self, name, tag, *args):
            self.executed.append(("timeSeries", name, tag, args))

    model = FakeModel()
    p = OpenSeesParser(model)
    p.hook_all()
    p.clear()

    model.node(7, 1.0, 2.0)
    model.timeSeries("Linear", 9, "-factor", 2.0)

    # underlying methods still executed
    assert model.executed == [("node", 7, (1.0, 2.0)), ("timeSeries", "Linear", 9, ("-factor", 2.0))]
    # and the managers captured the parsed commands
    assert p.node.get_node_coords(7) == [1.0, 2.0]
    assert p.timeseries.get_time_series(9)["factor"] == 2.0

    p.restore_all()
    assert not hasattr(model.node, "__opsparser_original__")
