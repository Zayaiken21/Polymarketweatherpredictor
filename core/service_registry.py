from dataclasses import dataclass, field
from typing import Callable, Any

@dataclass
class ServiceRegistry:
    services: dict[str, dict[str, Callable[..., Any]]] = field(default_factory=dict)
    tools: dict[str, dict[str, Callable[..., Any]]] = field(default_factory=dict)

    def register_service(self, module_name: str, func_name: str, func: Callable[..., Any]):
        self.services.setdefault(module_name, {})[func_name] = func

    def register_tool(self, module_name: str, func_name: str, func: Callable[..., Any]):
        self.tools.setdefault(module_name, {})[func_name] = func

    def get(self, name: str):
        for group in (self.services, self.tools):
            for _, funcs in group.items():
                if name in funcs:
                    return funcs[name]
        return None

    def all_functions(self):
        out = {}
        out.update({f"{m}.{f}": fn for m, funcs in self.services.items() for f, fn in funcs.items()})
        out.update({f"{m}.{f}": fn for m, funcs in self.tools.items() for f, fn in funcs.items()})
        return out

registry = ServiceRegistry()