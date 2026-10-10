#!/usr/bin/env python3
"""Package explicit non-secret manuscript/support files; never package credentials or Git state."""
from pathlib import Path
import hashlib
import json
import re
import zipfile

ROOT=Path(__file__).resolve().parents[1]
RELEASE=ROOT/'release'
FILES=[ROOT/name for name in ['README.md','RIGHTS.md','CITATION.cff','paper.md','references.md','requirements-validation.txt']]
FILES.extend(ROOT/name for name in [
    'research/related-work.md', 'research/search-log.md',
    'research/contribution-assessment.md', 'integration/books.md',
    'scripts/build_paper.py', 'scripts/inspect_pdf.py',
    'scripts/package_release.py', 'scripts/paper-header.tex',
    'scripts/journal-template.tex',
])
for folder in ['architecture','schemas']:
    FILES.extend(p for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix not in ['.pyc'])
FILES.extend(RELEASE/name for name in ['paper.tex','metadata.json','zenodo-upload.md'])
FILES=sorted(set(FILES))
for p in FILES:
    if not p.is_file(): raise SystemExit(f'Missing release input: {p.relative_to(ROOT)}')
    if p.name.startswith('.env') or '.git' in p.parts: raise SystemExit('Forbidden archive input')
version=json.loads((RELEASE/'metadata.json').read_text())['version']
if not re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+',version):
    raise SystemExit('Expected a semantic document version')
prefix=f'orchestrator-lifecycle-{version}'
archive=RELEASE/f'{prefix}-source.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in FILES:
        name=prefix+'/'+p.relative_to(ROOT).as_posix()
        entry=zipfile.ZipInfo(name,date_time=(2026,10,9,12,0,0))
        entry.compress_type=zipfile.ZIP_DEFLATED
        entry.external_attr=0o644 << 16
        z.writestr(entry,p.read_bytes())
outputs=[RELEASE/'paper.pdf',archive]
checks=''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n' for p in outputs)
(RELEASE/'SHA256SUMS').write_text(checks)
manifest={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in FILES}
(RELEASE/'source-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(f'Packaged {len(FILES)} source/support files; checksums written')
