# PeaBox Photo Lab v0.2.29

A quality-focused release built from v0.2.28. No existing editing capability is intentionally removed.

## Reliability and architecture
- Extracted the UI-independent image-processing engine to `peabox_core.py`.
- Reduced `app.py` from approximately 574 lines to a smaller UI/orchestration layer.
- Added automated tests covering representative core filters, resizing/cropping, image analysis, JPEG/PNG/WebP export, extreme dimensions, and non-destructive behavior.
- Added `validate_release.py` for version alignment, source compilation, and required-file validation.
- Added a GitHub Actions quality workflow.
- Added `requirements-dev.txt` with pytest and Ruff ranges.

## UX quality
- Consolidated the long export preset selector into logical groups: Recommended, Web, Social & sharing, Professional, Print & archive, and All presets.
- The complete v0.2.28 preset inventory remains accessible through All presets.

## Release conventions
- Version: 0.2.29
- Archive: peabox-photo-lab-v0.2.29.zip
