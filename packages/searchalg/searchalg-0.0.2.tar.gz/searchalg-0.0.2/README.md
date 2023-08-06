# searchalg

## Development Setup

1. Create and activate virtual environment
    ```
    python -m venv venv
    source venv/bin/activate or venv\Scripts\activate
    ```
2. Install dev-dependencies (editable)
    ```
    flit install
    ```
   

## Publish to Pypi

1. Update the `__version__` in `searchalg/__init__.py`
2. Set `SOURCE_DATE_EPOCH=$(date +%s)` (see [flit reproducible builds](https://flit.readthedocs.io/en/latest/reproducible.html))
3. Update the `CHANGELOG.md` including the value of `SOURCE_DATE_EPOCH` variable
4. Publish the package to pypi: `flit publish`
