class NeedModule(ImportError):
    def __init__(self, value):
        self.value = value
    def __str__(self, value):
        return "Module Dependency not met: " + repr(self.value)