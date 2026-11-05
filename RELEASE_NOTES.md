# PeaBox Photo Lab v0.2.30

An end-to-end UI quality release built cumulatively from v0.2.29.

## UI test coverage
- Added Streamlit AppTest automation for the complete rendered application flow.
- Tested every option across all select-box menus, including quick styles, crop ratios, creative effects, positions, export groups, formats, and every export preset.
- Tested every slider at minimum and maximum boundaries and restored defaults after each check.
- Tested every toggle in both on and off states.
- Tested all text and editable colour actions.
- Tested conditional custom width/height controls and JPEG, PNG, and WebP export paths.
- Total UI action/state checks: 284.

## Fixes
- Replaced deprecated Streamlit `use_container_width=True` calls with `width="stretch"`.
- Added deterministic `PEABOX_TEST_MODE=1` generated-image plumbing so automated tests can traverse the full app without bypassing normal upload behavior for users.

## Validation
- 14 pytest tests pass, including 8 UI end-to-end tests and 6 core/regression tests.
- Python compilation, release validation, and ZIP integrity pass.

## Release conventions
- Version: 0.2.30
- Archive: peabox-photo-lab-v0.2.30.zip
