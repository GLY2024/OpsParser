from typing import Any, Optional

from ._BaseHandler import BaseHandler


class LoadManager(BaseHandler):
    """Parse and store `pattern`, `load` and `eleLoad` commands.

    Full OpenSeesPy signatures handled here:
        pattern('Plain', patternTag, tsTag, '-fact', fact)
        pattern('UniformExcitation', patternTag, dir, '-disp', dispSeriesTag,
                '-vel', velSeriesTag, '-accel', accelSeriesTag,
                '-vel0', vel0, '-fact', fact)
        pattern('MultipleSupport', patternTag)
        load(nodeTag, *loadValues)
        eleLoad('-ele', *eleTags, '-range', eleTag1, eleTag2, '-type',
                '-beamUniform', Wy, <Wz>, Wx,
                '-beamPoint',  Py, <Pz>, Px, xL,
                '-beamThermal', *tempPts)
    """

    def __init__(self):
        self.patterns = {}  # Load patterns: tag -> {type, tsTag, ...}
        self.node_loads = {}  # Node loads: (patternTag, nodeTag) -> values
        self.ele_loads = {}  # Element loads: (patternTag, eleTag) -> {type, values}
        self.current_pattern = None  # Current load pattern

    @property
    def _COMMAND_RULES(self) -> dict[str, dict[str, Any]]:
        return {
            # pattern(patternType, patternTag, *args)
            "pattern": {
                "positional": ["patternType", "patternTag", "args*"],
                "options": {
                    "-fact?": "factor",
                    "-factor?": "factor",
                    "-disp?": "dispSeriesTag",
                    "-vel?": "velSeriesTag",
                    "-accel?": "accelSeriesTag",
                    "-vel0?": "vel0",
                },
            },
            # load(nodeTag, *loadValues)
            "load": {
                "positional": ["nodeTag", "loadValues*"],
            },
            # eleLoad(*args) - parsed manually in _handle_eleLoad because the
            # value list of '-type' contains nested '-beamUniform' etc. flags
            "eleLoad": {
                "positional": ["args*"],
            },
        }

    def handles(self):
        return ["pattern", "load", "eleLoad"]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        args, kwargs = arg_map.get("args"), arg_map.get("kwargs")
        if func_name == "pattern":
            self._handle_pattern(*args, **kwargs)
        elif func_name == "load":
            self._handle_load(*args, **kwargs)
        elif func_name == "eleLoad":
            self._handle_eleLoad(*args, **kwargs)

    def _handle_pattern(self, *args: Any, **kwargs: Any):
        """Handle load pattern command"""
        arg_map = self._parse("pattern", *args, **kwargs)

        pattern_type = arg_map.get("patternType", "")
        tag = arg_map.get("patternTag", 0)

        if not pattern_type or tag is None:
            return

        pattern_info = {"type": pattern_type, "tag": tag}

        extra_args = list(arg_map.get("args", []))

        # Plain patterns: third positional argument is the time series tag
        if pattern_type == "Plain":
            if extra_args:
                pattern_info["tsTag"] = extra_args.pop(0)
        # UniformExcitation: third positional argument is the excitation dir
        elif pattern_type == "UniformExcitation":
            if extra_args:
                pattern_info["dir"] = extra_args.pop(0)

        for key in ("factor", "dispSeriesTag", "velSeriesTag", "accelSeriesTag", "vel0"):
            if arg_map.get(key) is not None:
                pattern_info[key] = arg_map[key]

        if extra_args:
            pattern_info["args"] = extra_args

        self.patterns[tag] = pattern_info
        # Update current load pattern
        self.current_pattern = tag

    def _handle_load(self, *args: Any, **kwargs: Any):
        """Handle node load command"""
        arg_map = self._parse("load", *args, **kwargs)

        tag = arg_map.get("nodeTag")  # Node tag
        load_values = arg_map.get("loadValues", [])  # Load components

        if tag is None or not load_values:
            return

        # Store node load with key as (load pattern tag, node tag) tuple.
        # current_pattern may be None when the command is replayed standalone.
        load_key = (self.current_pattern, tag)
        self.node_loads[load_key] = load_values

    def _handle_eleLoad(self, *args: Any, **kwargs: Any):
        """Handle element load command"""
        arg_map = self._parse("eleLoad", *args, **kwargs)
        args = list(arg_map.get("args", []))

        def _is_flag(token: Any) -> bool:
            return isinstance(token, str) and token.startswith("-")

        # Extract element tag list from '-ele' and/or '-range'
        ele_tags: list[int] = []
        if "-ele" in args:
            ele_idx = args.index("-ele") + 1
            while ele_idx < len(args) and not _is_flag(args[ele_idx]):
                try:
                    ele_tags.append(int(args[ele_idx]))
                    ele_idx += 1
                except (ValueError, TypeError):
                    break

        if "-range" in args and args.index("-range") + 2 < len(args):
            range_idx = args.index("-range")
            start_tag = int(args[range_idx + 1])
            end_tag = int(args[range_idx + 2])
            ele_tags.extend(range(start_tag, end_tag + 1))

        # Get load type: the flag following '-type' (e.g. '-beamUniform')
        load_type = ""
        if "-type" in args and args.index("-type") + 1 < len(args):
            load_type = args[args.index("-type") + 1]

        # Extract load component values following the load-type flag
        load_values: list[float] = []
        if load_type and load_type in args:
            value_idx = args.index(load_type) + 1
            while value_idx < len(args) and not _is_flag(args[value_idx]):
                try:
                    load_values.append(float(args[value_idx]))
                    value_idx += 1
                except (ValueError, TypeError):
                    break

        # Store load for each element; current_pattern may be None when the
        # command is replayed standalone.
        for ele_tag in ele_tags:
            load_key = (self.current_pattern, ele_tag)
            self.ele_loads[load_key] = {"type": load_type.lstrip("-"), "values": load_values}

    # ------------------------------------------------------------------
    # Query API
    # ------------------------------------------------------------------
    def get_pattern(self, tag: int) -> Optional[dict]:
        """Get load pattern by tag"""
        return self.patterns.get(tag)

    def get_load_patterns(self) -> list[dict]:
        """Get all load patterns as a list of dicts"""
        return [
            {"pattern_type": info.get("type"), **info}
            for info in self.patterns.values()
        ]

    def get_node_load(self, pattern_tag: Optional[int], node_tag: int) -> list[float]:
        """Get node load under specified load pattern"""
        return self.node_loads.get((pattern_tag, node_tag), [])

    def get_node_loads(self) -> list[dict]:
        """Get all node loads as a list of dicts"""
        return [
            {"pattern_tag": pattern_tag, "node_tag": node_tag, "forces": values}
            for (pattern_tag, node_tag), values in self.node_loads.items()
        ]

    def get_loads_by_node(self, node_tag: int) -> list[dict]:
        """Get all loads applied to a specific node (across patterns)"""
        return [load for load in self.get_node_loads() if load["node_tag"] == node_tag]

    def get_ele_load(self, pattern_tag: Optional[int], ele_tag: int) -> dict:
        """Get element load under specified load pattern"""
        return self.ele_loads.get((pattern_tag, ele_tag), {})

    def get_element_loads(self) -> list[dict]:
        """Get all element loads as a list of dicts"""
        return [
            {
                "pattern_tag": pattern_tag,
                "element_tag": ele_tag,
                "load_type": info.get("type"),
                "values": info.get("values", []),
            }
            for (pattern_tag, ele_tag), info in self.ele_loads.items()
        ]

    def get_loads_by_element(self, ele_tag: int) -> list[dict]:
        """Get all loads applied to a specific element (across patterns)"""
        return [load for load in self.get_element_loads() if load["element_tag"] == ele_tag]

    def get_patterns_by_time_series(self, ts_tag: int) -> list[int]:
        """Get all load patterns using specific time series"""
        return [tag for tag, info in self.patterns.items() if info.get("tsTag") == ts_tag]

    def clear(self):
        """Clear all data"""
        self.patterns.clear()
        self.node_loads.clear()
        self.ele_loads.clear()
        self.current_pattern = None
