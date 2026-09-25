from typing import List
from universal_ai.interfaces.modules import BaseModule
from universal_ai.domain.models import Capability
from universal_ai.domain.exceptions import ModuleError

class ModuleRegistry:
    def __init__(self): self._modules: dict[str, BaseModule] = {}
    def register(self, module: BaseModule) -> None:
        if module.metadata.module_id in self._modules:
            raise ModuleError(f"Module {module.metadata.module_id} already registered")
        self._modules[module.metadata.module_id] = module
    def get(self, module_id: str) -> BaseModule:
        if module_id not in self._modules:
            raise ModuleError(f"Module {module_id} not found")
        return self._modules[module_id]
    def list(self) -> List[BaseModule]: return list(self._modules.values())