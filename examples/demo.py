"""Small demo script showing how to use the userverse_python_client package."""

import sys
from pathlib import Path

# Allow running the example without installing the package first.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from userverse_python_client import add_numbers, hello


def main() -> None:
    print(hello())
    print(f"1 + 2 = {add_numbers(1, 2)}")


if __name__ == "__main__":  # pragma: no cover
    main()
