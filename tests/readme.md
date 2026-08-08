# Testing guide

Run the test suite from the project root:

```bash
uv run python -m pytest
```

Notes:
- Tests rely on lightweight stubs defined in `tests/conftest.py` to avoid installing the external shared models.
- `test_shared_models_compatibility.py` starts a clean Python process and validates
  the installed `shared-models` v0.1.14 package against the Userverse v0.7.0
  company, role, and permission contracts.
- Install project dependencies before running the full suite so the compatibility
  test can import the pinned shared-model release.
