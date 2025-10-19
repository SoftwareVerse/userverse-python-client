



<!-- CI status for your release workflow -->

[![CI - Release Tag](https://github.com/SoftwareVerse/userverse-python-client/actions/workflows/release.yml/badge.svg)](https://github.com/SoftwareVerse/userverse-python-client/actions/workflows/release.yml)

<!-- Latest release (SemVer-aware) badge → opens the latest release page -->

[![Latest Release](https://img.shields.io/github/v/release/SoftwareVerse/userverse-python-client?display_name=tag&sort=semver)](https://github.com/SoftwareVerse/userverse-python-client/releases/latest)

<!-- Optional: latest tag badge (from tags, even if not “GitHub Release”) -->

[![Latest Tag](https://img.shields.io/github/v/tag/SoftwareVerse/userverse-python-client?label=tag&sort=semver)](https://github.com/SoftwareVerse/userverse-python-client/releases/latest)

<!-- Optional: release date & total downloads badges -->

[![Release Date](https://img.shields.io/github/release-date/SoftwareVerse/userverse-python-client)](https://github.com/SoftwareVerse/userverse-python-client/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/SoftwareVerse/userverse-python-client/total)](https://github.com/SoftwareVerse/userverse-python-client/releases)

<!-- You already have Codecov; keep it (replace token if needed) -->

[![codecov](https://codecov.io/gh/SoftwareVerse/userverse-python-client/branch/main/graph/badge.svg?token=YOUR_TOKEN)](https://codecov.io/gh/SoftwareVerse/userverse-python-client)

# userverse-python-client

Python client for the Userverse HTTP server.

## Installation

Create and activate a virtual environment, then install the project in editable mode:

## linux configuration

```bash
uv venv
source .venv\Scripts\activate
uv pip install -e .
```

## windows configuration

```bash
uv venv
.venv\Scripts\activate
uv pip install -e .
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

##uv run
uv run python examples/demo.py
```

## Tests

Run the unit tests with:

```bash
python -m unittest discover -s tests -v

## uv run tests
uv run python -m unittest discover -s tests -v
```
