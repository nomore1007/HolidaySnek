"""Persistent user preferences."""
from __future__ import annotations
import json, os
from pathlib import Path
DEFAULTS = {"scene": "halloween", "speed": 1.0, "intensity": 0.7}
def config_path():
    root = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return root / "holidaysnek" / "config.json"
def clamp(value, low, high):
    try: return max(low, min(high, float(value)))
    except (TypeError, ValueError): return (low + high) / 2
def load_settings():
    settings = dict(DEFAULTS)
    try:
        data = json.loads(config_path().read_text(encoding="utf-8"))
        if isinstance(data, dict): settings.update({k: data[k] for k in DEFAULTS if k in data})
    except (OSError, ValueError, TypeError): pass
    settings["speed"] = clamp(settings.get("speed", 1), .25, 3)
    settings["intensity"] = clamp(settings.get("intensity", .7), .1, 1)
    return settings
def save_settings(settings):
    path = config_path(); path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)
