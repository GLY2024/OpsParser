from collections import defaultdict
from typing import Any

from ._BaseHandler import BaseHandler


class TimeSeriesManager(BaseHandler):
    """Parse and store every `timeSeries` command defined by OpenSeesPy.

    Supported types (see https://openseespydoc.readthedocs.io):
        Constant, Linear, Trig, Triangle, Rectangular, Pulse, Path
    Unknown types fall back to a generic ``(typeName, tag, *args)`` rule so
    no command is ever lost.
    """

    def __init__(self):
        self.time_series = {}

    @property
    def _COMMAND_RULES(self) -> dict[str, dict[str, Any]]:
        # Generic fallback rule for series types not explicitly listed below
        generic_rule = {
            "positional": ["typeName", "tag", "args*"],
        }
        rules = defaultdict(lambda: generic_rule)
        rules["alternative"] = True

        # timeSeries('Constant', tag, '-factor', factor=1.0)
        rules["Constant"] = {
            "positional": ["typeName", "tag"],
            "options": {"-factor?": "factor"},
        }
        # timeSeries('Linear', tag, '-factor', factor=1.0)
        rules["Linear"] = {
            "positional": ["typeName", "tag"],
            "options": {"-factor?": "factor"},
        }
        # timeSeries('Trig', tag, tStart, tEnd, period,
        #            '-factor', factor=1.0, '-shift', shift=0.0, '-zeroShift', zeroShift=0.0)
        rules["Trig"] = {
            "positional": ["typeName", "tag", "tStart", "tEnd", "period"],
            "options": {
                "-factor?": "factor",
                "-shift?": "shift",
                "-zeroShift?": "zeroShift",
            },
        }
        # timeSeries('Triangle', tag, tStart, tEnd, period,
        #            '-factor', factor=1.0, '-shift', shift=0.0, '-zeroShift', zeroShift=0.0)
        rules["Triangle"] = {
            "positional": ["typeName", "tag", "tStart", "tEnd", "period"],
            "options": {
                "-factor?": "factor",
                "-shift?": "shift",
                "-zeroShift?": "zeroShift",
            },
        }
        # timeSeries('Rectangular', tag, tStart, tEnd, '-factor', factor=1.0)
        rules["Rectangular"] = {
            "positional": ["typeName", "tag", "tStart", "tEnd"],
            "options": {"-factor?": "factor"},
        }
        # timeSeries('Pulse', tag, tStart, tEnd, period, '-width', width=0.5,
        #            '-shift', shift=0.0, '-factor', factor=1.0, '-zeroShift', zeroShift=0.0)
        rules["Pulse"] = {
            "positional": ["typeName", "tag", "tStart", "tEnd", "period"],
            "options": {
                "-width?": "width",
                "-shift?": "shift",
                "-factor?": "factor",
                "-zeroShift?": "zeroShift",
            },
        }
        # timeSeries('Path', tag, '-dt', dt=0.0, '-values', *values, '-time', *time,
        #            '-filePath', filePath='', '-fileTime', fileTime='',
        #            '-factor', factor=1.0, '-startTime', startTime=0.0,
        #            '-useLast', '-prependZero')
        rules["Path"] = {
            "positional": ["typeName", "tag"],
            "options": {
                "-dt?": "dt",
                "-values?": "values*",
                "-time?": "time*",
                "-filePath?": "filePath",
                "-fileTime?": "fileTime",
                "-factor?": "factor",
                "-startTime?": "startTime",
                "-useLast?": "useLast",
                "-prependZero?": "prependZero",
            },
            # values of these flags are filenames (plain strings)
            "string_flags": ["-filePath", "-fileTime"],
        }

        return {"timeSeries": rules}

    def handles(self):
        return ["timeSeries"]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        args, kwargs = arg_map.get("args"), arg_map.get("kwargs")
        if func_name == "timeSeries":
            self._handle_time_series(*args, **kwargs)

    def _handle_time_series(self, *args: Any, **kwargs: Any):
        arg_map = self._parse("timeSeries", *args, **kwargs)

        tag = arg_map.get("tag")
        if tag is None:
            return

        series_type = arg_map.get("typeName")
        if not series_type:
            return

        info: dict[str, Any] = {"type": series_type, "tag": tag}

        # Boolean flags: presence (parsed as None) means True
        for bool_flag in ("useLast", "prependZero"):
            if bool_flag in arg_map:
                arg_map[bool_flag] = True

        # Copy every parsed (non-None) field except the ones already stored
        for key, value in arg_map.items():
            if key in ("typeName", "tag") or value is None:
                continue
            info[key] = value

        # Compatibility: a single trailing numeric token is the load factor
        # (e.g. ``timeSeries('Constant', tag, factor)`` written positionally)
        leftover = info.get("args")
        if (
            "factor" not in info
            and isinstance(leftover, list)
            and len(leftover) == 1
            and isinstance(leftover[0], (int, float))
        ):
            info["factor"] = leftover[0]
            info.pop("args")

        self.time_series[tag] = info

    def get_time_series(self, tag: int) -> dict:
        """Get time series by tag"""
        return self.time_series.get(tag, {})

    def get_all_time_series(self) -> dict[int, dict]:
        """Get all stored time series keyed by tag"""
        return dict(self.time_series)

    def get_time_series_by_type(self, series_type: str) -> list[int]:
        """Get all time series tags of a specific type"""
        return [tag for tag, info in self.time_series.items()
                if info.get("type") == series_type]

    # Alias kept for API symmetry with other managers
    def get_series_by_type(self, series_type: str) -> list[int]:
        """Get all time series tags of a specific type (alias)"""
        return self.get_time_series_by_type(series_type)

    def clear(self):
        """Clear all time series data"""
        self.time_series.clear()
