"""Rule-driven audit: for every handler command rule, synthesize argument
combinations (positional only / each option alone / all options together)
and verify that ``_parse`` maps them back correctly.

Run directly for a report:  python tests/rule_audit.py
Imported by the systematic validation test as well.
"""
from collections import defaultdict

TYPE_NAME_KEYS = {
    "eleType", "matType", "typeName", "patternType", "secType", "type",
    "integrationType", "frnType", "transfType", "seriesType", "command",
}


def iter_handlers():
    """Yield every handler singleton (managers + element/material subhandlers)."""
    from opsparser.OpenSeesParser import OpenSeesCommand

    seen = set()
    for member in OpenSeesCommand:
        manager = member.instance
        if id(manager) not in seen:
            seen.add(id(manager))
            yield manager
        # Sub-handlers (e.g. element/material type handlers)
        for registry_attr in ("_command2typehandler",):
            registry = getattr(manager, registry_attr, None)
            if isinstance(registry, dict):
                for type_map in registry.values():
                    for sub in type_map.values():
                        if id(sub) not in seen:
                            seen.add(id(sub))
                            yield sub


def iter_rules(handler):
    """Yield (command, type_key_or_None, rule) for every concrete rule."""
    try:
        rules = handler._COMMAND_RULES
    except Exception as exc:  # pragma: no cover - defensive
        yield ("<error>", None, exc)
        return
    for command, rule in rules.items():
        if not isinstance(rule, dict):
            continue
        if rule.get("alternative"):
            for key, subrule in rule.items():
                if key == "alternative" or not isinstance(subrule, dict):
                    continue
                yield (command, key, subrule)
        else:
            yield (command, None, rule)


def make_value(name, type_key, index):
    """Synthesize a plausible argument value for parameter *name*."""
    clean = name.rstrip("*?0123456789").rstrip("*?")
    if clean in TYPE_NAME_KEYS and type_key is not None:
        return type_key
    if clean.lower().endswith("tag") or clean.lower().endswith("tags"):
        return index + 1
    if clean.lower().endswith(("nodes", "node")):
        return index + 1
    return float(index + 1)


def build_positional(rule, type_key):
    """Build a synthetic positional argument list for *rule*."""
    from opsparser._manager._BaseHandler import BaseHandler

    args = []
    expected = {}
    for i, name in enumerate(rule.get("positional", [])):
        clean, count = BaseHandler.get_name_and_count(name)
        if count == "all":
            values = [make_value(name, type_key, i), make_value(name, type_key, i + 1)]
            # values for star-args must not collide with option flags
            values = [v if not isinstance(v, str) or not v.startswith("-") else 1.0
                      for v in values]
            args.extend(values)
            expected[clean] = values
        elif count == 1:
            v = make_value(name, type_key, i)
            args.append(v)
            expected[clean] = v
        else:
            values = [make_value(name, type_key, i + j) for j in range(count)]
            args.extend(values)
            expected[clean] = values
    return args, expected


def build_option(flag, spec, type_key):
    """Build synthetic tokens & expectations for a single option flag."""
    from opsparser._manager._BaseHandler import BaseHandler

    pure_flag = flag.split("*")[0].rstrip("?")
    tokens = [pure_flag]
    expected = {}
    specs = spec if isinstance(spec, (list, tuple)) else [spec]
    for j, subname in enumerate(specs):
        clean, count = BaseHandler.get_name_and_count(subname)
        if count == "all":
            values = [float(j + 1), float(j + 2)]
            tokens.extend(values)
            expected[clean] = values
        elif count == 0:
            # boolean flag: parser records presence as None
            expected[clean] = None
        elif count == 1:
            v = float(j + 1)
            tokens.append(v)
            expected[clean] = v
        else:
            values = [float(j + k + 1) for k in range(count)]
            tokens.extend(values)
            expected[clean] = values
    return tokens, expected


def audit_rule(handler, command, type_key, rule):
    """Run all synthesized combinations for one rule. Returns list of issues."""
    issues = []
    pos_args, pos_expected = build_positional(rule, type_key)
    options = rule.get("options", {}) or {}

    combos = [([], {})]  # no options
    for flag, spec in options.items():
        try:
            tokens, expected = build_option(flag, spec, type_key)
        except Exception as exc:
            issues.append(f"option spec invalid {flag!r}: {exc}")
            continue
        combos.append((tokens, expected))
    # all options together
    if len(options) > 1:
        all_tokens, all_expected = [], {}
        for flag, spec in options.items():
            try:
                tokens, expected = build_option(flag, spec, type_key)
            except Exception:
                continue
            all_tokens.extend(tokens)
            all_expected.update(expected)
        combos.append((all_tokens, all_expected))

    for opt_tokens, opt_expected in combos:
        full_args = list(pos_args) + list(opt_tokens)
        label = f"{command}({type_key or ''}) args={full_args}"
        try:
            result = handler._parse(command, *full_args)
        except Exception as exc:
            issues.append(f"PARSE ERROR {label}: {type(exc).__name__}: {exc}")
            continue
        for key, expected_value in {**pos_expected, **opt_expected}.items():
            got = result.get(key, "<missing>")
            if got != expected_value:
                issues.append(
                    f"MISMATCH {label}: {key!r} expected {expected_value!r}, got {got!r}"
                )
    return issues


def ensure_model(ndm=3, ndf=6):
    """Some handlers build their rules from the live model dimension
    (``ops.getNDM()``), so a model must exist before rules are inspected."""
    import openseespy.opensees as ops

    ops.wipe()
    ops.model("basic", "-ndm", ndm, "-ndf", ndf)


def run_audit(ndm=3, ndf=6):
    """Audit every rule of every handler. Returns {handler_name: [issues]}."""
    ensure_model(ndm, ndf)
    report = defaultdict(list)
    counts = {"rules": 0, "handlers": 0}
    for handler in iter_handlers():
        counts["handlers"] += 1
        hname = handler.__class__.__name__
        for command, type_key, rule in iter_rules(handler):
            if isinstance(rule, Exception):
                report[hname].append(f"_COMMAND_RULES error: {rule}")
                continue
            counts["rules"] += 1
            issues = audit_rule(handler, command, type_key, rule)
            report[hname].extend(issues)
    return report, counts


if __name__ == "__main__":
    report, counts = run_audit()
    total = sum(len(v) for v in report.values())
    print(f"handlers={counts['handlers']} rules={counts['rules']} issues={total}")
    for hname, issues in sorted(report.items()):
        if not issues:
            continue
        print(f"\n=== {hname} ({len(issues)}) ===")
        for issue in issues:
            print("  -", issue)
