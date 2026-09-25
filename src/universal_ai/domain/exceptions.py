class UniversalAIError(Exception):
    def __init__(self, message: str, code: str):
        super().__init__(message)
        self.message, self.code = message, code
class PolicyError(UniversalAIError):
    def __init__(self, message: str): super().__init__(message, "POLICY_ERROR")
class SandboxError(UniversalAIError):
    def __init__(self, message: str): super().__init__(message, "SANDBOX_ERROR")
class RoutingError(UniversalAIError):
    def __init__(self, message: str): super().__init__(message, "ROUTING_ERROR")
class ModuleError(UniversalAIError):
    def __init__(self, message: str): super().__init__(message, "MODULE_ERROR")