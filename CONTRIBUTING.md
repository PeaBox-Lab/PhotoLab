# Contributing

Thank you for improving PeaBox Photo Lab.

1. Open an issue describing the user problem.
2. Fork the repository and create a focused branch.
3. Create a Python 3.10+ virtual environment and install `requirements.txt`.
4. Keep image processing local and non-destructive. Do not add telemetry or upload services without explicit disclosure and opt-in.
5. Run `python -m py_compile app.py` and manually test JPG, PNG, and WebP import/export.
6. Submit a pull request with screenshots and clear test steps.

Use small, reviewable changes. Never commit photographs, API keys, `.env` files, or Streamlit secrets.
