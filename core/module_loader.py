import importlib.util
import inspect
from pathlib import Path

from core.service_registry import registry

PROJECT_FOLDERS = {"core", "services", "ui", "auth", "storage", "tools", "agents"}
SKIP_DIRS = {".venv", "venv", "__pycache__", "site-packages", "dist-packages", ".git", "node_modules"}

def _should_skip(path: Path) -> bool:
    parts = {p.lower() for p in path.parts}
    return any(d in parts for d in SKIP_DIRS)

def _in_project_tree(path: Path, root: Path) -> bool:
    try:
        rel = path.resolve().relative_to(root.resolve())
        return bool(rel.parts) and rel.parts[0] in PROJECT_FOLDERS
    except Exception:
        return False

def load_module_from_path(path: Path):
    module_name = f"_dyn_{path.parent.name}_{path.stem}"
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def auto_discover(root_dir: str = "."):
    root = Path(root_dir).resolve()

    for path in root.rglob("*.py"):
        if _should_skip(path):
            continue
        if path.name.startswith("__"):
            continue
        if not _in_project_tree(path, root):
            continue
        if not (path.name.endswith("_service.py") or path.name.endswith("_tools.py")):
            continue

        module = load_module_from_path(path)

        for func_name, func in inspect.getmembers(module, inspect.isfunction):
            if func.__module__ != module.__name__:
                continue
            if path.name.endswith("_service.py"):
                registry.register_service(path.stem, func_name, func)
            else:
                registry.register_tool(path.stem, func_name, func)

    return registry