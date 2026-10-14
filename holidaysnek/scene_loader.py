"""Discover scene plugins from folders, without hard-coded registrations."""
from __future__ import annotations
import importlib.util, os, site, sys, tomllib
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "scenes"
PACKAGED_ROOTS = [
    Path(sys.prefix) / "share" / "holidaysnek" / "scenes",
    Path(site.getuserbase()) / "share" / "holidaysnek" / "scenes",
]

@dataclass
class ScenePlugin:
    id: str
    name: str
    description: str
    module: object
    path: Path
    def create(self): return self.module.Scene()

def scene_roots():
    roots = [ROOT, *PACKAGED_ROOTS]
    roots.extend(Path(p).expanduser() for p in os.environ.get("HOLIDAYSNEK_SCENES", "").split(os.pathsep) if p.strip())
    seen = set()
    for root in roots:
        try: key = root.resolve()
        except OSError: continue
        if key not in seen and key.is_dir():
            seen.add(key)
            yield key

def discover_scenes():
    found = {}
    for root in scene_roots():
        for folder in sorted(root.iterdir()):
            manifest, source = folder / "scene.toml", folder / "scene.py"
            if not folder.is_dir() or not manifest.is_file() or not source.is_file(): continue
            try:
                meta = tomllib.loads(manifest.read_text(encoding="utf-8"))
                sid, name = str(meta["id"]).strip(), str(meta["name"]).strip()
                if not sid or not name or sid in found: continue
                spec = importlib.util.spec_from_file_location("holidaysnek_scene_" + "".join(c if c.isalnum() else "_" for c in sid), source)
                if spec is None or spec.loader is None: continue
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if not callable(getattr(module, "Scene", None)): continue
                found[sid] = ScenePlugin(sid, name, str(meta.get("description", "")), module, folder)
            except Exception as exc:
                print(f"HolidaySnek: skipping scene in {folder}: {exc}", file=sys.stderr)
    return sorted(found.values(), key=lambda p: p.name.casefold())
