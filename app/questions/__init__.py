import importlib
import pkgutil
from pathlib import Path

for _, module_name, _ in pkgutil.walk_packages(
    path=[str(Path(__file__).parent)],
    prefix="app.questions.",
):
    if not any(s in module_name for s in ("schema", "registry", "runner")):
        importlib.import_module(module_name)