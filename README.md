# PeaBox Photo Lab

A practical, privacy-first photo editor built with Python, Streamlit, Pillow and NumPy.

## Features

- Live browser-based preview
- Brightness, contrast, saturation, sharpness, temperature, tint, shadows and highlights
- Crop presets, rotation and flips
- Smart Auto Optimize using histogram-aware exposure and contrast correction
- Creative Lab: Selective Colour Pop, Duotone, Dreamy Glow, Pencil Sketch, Pixel Art and Focus Vignette
- Borders and configurable watermark
- Long-edge resizing
- JPEG, PNG and WebP export
- Fresh encoding strips original EXIF metadata by default
- Non-destructive editing: every change is regenerated from the original upload

## Quick start

### Windows
Double-click `run_windows.bat`.

### Linux/macOS
```bash
chmod +x run_linux_mac.sh
./run_linux_mac.sh
```

### Manual
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

Open the URL shown in the terminal, normally `http://localhost:8501`.

## Requirements

- Python 3.10 or newer, 64-bit recommended
- Modern browser
- Approximately 250 MB free space for Python environment and packages
- 4 GB RAM minimum; 8 GB recommended for large photos

## Privacy

The app processes the upload in the Streamlit server process. When run locally, the image stays on your computer. The app does not intentionally write uploads to disk. Export creates a newly encoded image without copying original EXIF metadata. If deployed to a remote server, uploaded image bytes are necessarily sent to that server, so secure the deployment appropriately.

## Project structure

```text
PeaBox-Photo-Lab/
├── app.py
├── requirements.txt
├── run_windows.bat
├── run_linux_mac.sh
├── LICENSE
└── README.md
```

## Limitations

- Crop is center-based rather than a drag-to-select canvas.
- Very large images can consume several times their compressed file size in memory.
- Effects are intended for still images, not animated GIF/WebP files.

## License

MIT
