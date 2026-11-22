# jsonb releases

## 1.0.1
- Added support for passing additional keyword arguments through to the
underlying `json` module calls (`loads`, `load`, `dumps`, `dump`).
- Fixed `add_class` so it takes `(constructor, callback)` as documented,
instead of requiring an unused first argument.
- Migrated packaging from `setup.py` / `setup.cfg` to `pyproject.toml`.
- `add_class` now resolves handlers via the instance MRO, so a registered
subclass is preferred over a registered parent regardless of order.

## 1.0.0
- Initial release.