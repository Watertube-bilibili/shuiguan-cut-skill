#!/usr/bin/env python3
"""Build a deterministic, allowlisted Skill archive with Python's standard library."""
from pathlib import Path
import hashlib
import json
import zipfile

root = Path(__file__).resolve().parents[1]
files = [
    'shuiguan-cut/SKILL.md',
    'shuiguan-cut/agents/openai.yaml',
    'shuiguan-cut/references/recipe.md',
    'shuiguan-cut/scripts/shuiguan-cut.cjs',
    'shuiguan-cut/LICENSE',
    'shuiguan-cut/SOURCE.md',
]
output = root / 'dist'
output.mkdir(exist_ok=True)
archive = output / 'shuiguan-cut.zip'
if archive.exists() or (output / 'SHA256SUMS.txt').exists():
    raise SystemExit('Release output already exists; use a clean checkout/output directory.')

entries = {name: (root / name).read_text(encoding='utf-8').encode('utf-8') for name in files}
for language in ('README.md', 'README.en.md'):
    # The installed folder is the archive root. Adjust only local documentation links.
    content = (root / language).read_text(encoding='utf-8')
    content = content.replace('(shuiguan-cut/references/', '(references/')
    content = content.replace('(shuiguan-cut/SOURCE.md)', '(SOURCE.md)')
    entries['shuiguan-cut/' + language] = content.encode('utf-8')

with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as packed:
    for name in sorted(entries):
        info = zipfile.ZipInfo(name, (2026, 10, 5, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        packed.writestr(info, entries[name])

with zipfile.ZipFile(archive) as packed:
    assert packed.testzip() is None
    assert sorted(packed.namelist()) == sorted(entries)
    for name, data in entries.items():
        assert packed.read(name) == data, name

digest = hashlib.sha256(archive.read_bytes()).hexdigest()
(output / 'SHA256SUMS.txt').write_text(f'{digest}  shuiguan-cut.zip\n', encoding='utf-8')
print(json.dumps({'archive': archive.name, 'sha256': digest, 'bytes': archive.stat().st_size,
                  'files': sorted(entries)}, indent=2))
