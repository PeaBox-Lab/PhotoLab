from pathlib import Path
import py_compile,zipfile,sys
ROOT=Path(__file__).resolve().parent
version=(ROOT/'VERSION').read_text().strip()
assert version=='0.2.29'
assert f'version = "{version}"' in (ROOT/'pyproject.toml').read_text()
assert f'v{version}' in (ROOT/'app.py').read_text()
for f in ['app.py','peabox_core.py']: py_compile.compile(str(ROOT/f),doraise=True)
for required in ['README.md','CHANGELOG.md','RELEASE_NOTES.md','SECURITY.md','LICENSE','requirements.txt','requirements-dev.txt']:
    assert (ROOT/required).exists(), required
print('release validation PASS')
