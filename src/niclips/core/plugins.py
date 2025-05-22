"""Plugin capabilities to inject generation to factory."""

import importlib.util
import inspect
import logging
from pathlib import Path

from niclips.core.factory import ViewFactory
from niclips.typing import StrPath


def load_plugins_from_directory(directory: StrPath) -> None:
    """Recursively load plugins from a directory."""
    registry = ViewFactory._registry
    view_names = set(registry.keys())
    view_fns = set(registry.values())

    for plugin_path in Path(directory).glob("**/*.py"):
        module_name = plugin_path.stem
        spec = importlib.util.spec_from_file_location(module_name, plugin_path)
        if spec is None or spec.loader is None:
            continue

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Register all views that aren't already registered
        module_fns = {
            name: obj for name, obj in inspect.getmembers(module, inspect.isfunction)
        }

        # Check for name conflicts
        name_conflicts = [name for name in module_fns if name in view_names]
        for name in name_conflicts:
            logging.warning(f"Name '{name}' already used to register a view - skipping")
            continue

        if module_fns:
            for view_name, view_fn in module_fns.items():
                logging.info(f"Registering '{view_name}'")
                ViewFactory.register(view_name)(view_fn)
                view_names.add(view_name)
                view_fns.add(view_fn)


def load_default_plugins() -> None:
    """Load package available plugins by default."""
    pass
