# userverse-python-client

Python client for the Userverse HTTP server.

## Installation

Create and activate a virtual environment, then install the project in editable mode:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage

The package currently exposes a greeting helper and a simple arithmetic function. The example below prints both results:

```python
from userverse_python_client import add_numbers, hello

print(hello())
print(add_numbers(1.5, 2.5))
```

You can also run the bundled example module:

```bash
python examples/demo.py
```

## Tests

Run the unit tests with:

```bash
python -m unittest discover -s tests -v
```
