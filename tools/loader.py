# tools/loader.py

import pkgutil
import importlib
from tools.base_tool import BaseTool
import tools


def load_tools():
    tool_instances = []

    for _, module_name, _ in pkgutil.iter_modules(tools.__path__):
        if module_name in ("base_tool", "loader"):
            continue

        module = importlib.import_module(f"tools.{module_name}")

        for attr in vars(module).values():
            if (
                isinstance(attr, type)
                and issubclass(attr, BaseTool)
                and attr is not BaseTool
            ):
                tool_instances.append(attr())

    return tool_instances
