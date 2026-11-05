# Quality Report - v0.2.29

## Closed audit items
- Automated functional tests added.
- Runtime-oriented core smoke tests added.
- Regression tests cover tiny/extreme dimensions and non-destructive behavior.
- Image-processing core extracted from the Streamlit UI into peabox_core.py.
- Export preset UX grouped while preserving the full existing preset inventory.
- Development dependency profile added for pytest and Ruff.
- Repeatable release validation script added.
- GitHub Actions quality workflow added.

## Local validation results
- Python compilation: PASS
- Release gate: PASS
- pytest: 6 tests PASS
- ZIP integrity: PASS

## Scope
This quality release intentionally preserves all features from v0.2.28 while improving architecture, testability, release governance, and export navigation.
