class ModuleNotFound(Exception):
    """Raised whenever a module is not found. Not to be confused with ModuleNotFoundError which is completely unrelated."""


class FunctionNotFound(Exception):
    """Raised whenever a function is not found."""
