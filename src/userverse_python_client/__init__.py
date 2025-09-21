"""userverse_python_client package."""

from .arithmetic import add_numbers


def hello() -> str:
    return "Hello from userverse-python-client!"


__all__ = ["add_numbers", "hello"]
