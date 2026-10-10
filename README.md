# PeaBox Photo Lab

A privacy-first, local photo editor for creators, bloggers, small businesses, and everyday users. It runs in a browser while Python, Streamlit, Pillow, and NumPy perform the editing.

## Highlights

- Non-destructive adjustments and live before/after preview
- Smart auto optimization and five creative presets
- Light, colour, crop, rotate, mirror, borders, and watermark controls
- Selective colour, duotone, dreamy glow, pencil sketch, pixel art, and vignette
- Dominant colour palette extraction
- Downloadable style proof sheet
- Social format pack for square, portrait, landscape, and story crops
- Image health check and fresh exports without copied EXIF metadata
- JPEG, PNG, and WebP export

## Run locally

### Windows

Double-click `run_windows.bat`.

### Linux or macOS

```bash
chmod +x run_linux_mac.sh
./run_linux_mac.sh
```

### Manual setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

## Privacy

When run locally, the application processes image bytes on your computer and does not intentionally persist uploads. Exports are newly encoded and original EXIF metadata is not copied. A remote deployment necessarily receives uploaded files on that server, so operators must secure the deployment.

## Repository topics

`python`, `streamlit`, `pillow`, `photo-editor`, `image-processing`, `creator-tools`, `privacy-first`, `webp`, `peabox`

## Contributing and security

Read `CONTRIBUTING.md`. Report security issues using `SECURITY.md`, not a public issue.

## License

MIT
