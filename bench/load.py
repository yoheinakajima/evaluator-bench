"""Read data/ into plain dicts and validate against schema/."""
from __future__ import annotations
import json, pathlib
from typing import Any
try:
    import jsonschema
except ImportError:  # pragma: no cover
    jsonschema = None

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SCHEMA = ROOT / "schema"
DIMS = ["F","G","P","A","S","R","M","X"]

def _read(p: pathlib.Path) -> Any:
    return json.loads(p.read_text())

def _schema(name: str) -> dict | None:
    p = SCHEMA / f"{name}.schema.json"
    return _read(p) if p.exists() else None

def _validate(obj: Any, name: str, where: str) -> list[str]:
    s = _schema(name)
    if not s or jsonschema is None:
        return []
    errs = []
    v = jsonschema.Draft202012Validator(s)
    for e in sorted(v.iter_errors(obj), key=lambda e: e.path):
        errs.append(f"{where}: {'/'.join(str(x) for x in e.path) or '<root>'}: {e.message}")
    return errs

def load(strict: bool = True) -> dict:
    """Return {'dimensions','presets','types','sources','evaluators','signals','assessments','errors'}."""
    out: dict[str, Any] = {"errors": []}
    out["dimensions"] = _read(DATA / "dimensions.json")
    out["presets"] = _read(DATA / "presets.json")
    out["types"] = _read(DATA / "types.json")
    out["sources"] = {}
    for p in sorted((DATA / "sources").glob("*.json")):
        s = _read(p); out["errors"] += _validate(s, "source", p.name); out["sources"][s["id"]] = s
    out["evaluators"] = {}
    for p in sorted((DATA / "evaluators").glob("*.json")):
        e = _read(p); out["errors"] += _validate(e, "evaluator", p.name); out["evaluators"][e["id"]] = e
    out["signals"] = {}
    for p in sorted((DATA / "signals").glob("*.json")):
        for s in _read(p):
            out["errors"] += _validate(s, "signal", f"{p.name}:{s.get('id')}"); out["signals"][s["id"]] = s
    out["assessments"] = []
    for p in sorted((DATA / "assessments").glob("*.json")):
        for a in _read(p):
            out["errors"] += _validate(a, "assessment", f"{p.name}:{a.get('dimension')}"); out["assessments"].append(a)
    if strict and out["errors"]:
        raise ValueError("schema errors:\n" + "\n".join(out["errors"]))
    return out
