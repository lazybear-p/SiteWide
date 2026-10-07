"""Package the review folder; exclude the output ZIP and transient caches."""
from pathlib import Path
import hashlib
import zipfile

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'deliverables'
OUT.mkdir(exist_ok=True)
archive=OUT/'ppp-website-review.zip'
files=[]
for path in sorted(ROOT.rglob('*')):
    if not path.is_file():continue
    relative=path.relative_to(ROOT)
    if 'deliverables' in relative.parts or '__pycache__' in relative.parts or path.name=='.DS_Store':continue
    files.append(path)
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as package:
    for path in files:package.write(path,Path('ppp')/path.relative_to(ROOT))
with zipfile.ZipFile(archive) as package:
    assert package.testzip() is None
    names=package.namelist()
    assert 'ppp/START-HERE.html' in names
    assert 'ppp/preview.html' in names
    assert 'ppp/review/founder-pack.pdf' in names
    assert all(name.startswith('ppp/') and '..' not in Path(name).parts for name in names)
digest=hashlib.sha256(archive.read_bytes()).hexdigest()
(OUT/'SHA256SUMS.txt').write_text(f'{digest}  {archive.name}\n')
print(f'Archive verified: {len(files)} files; {archive.stat().st_size:,} bytes')
print(archive)
