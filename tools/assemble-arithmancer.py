"""Verify and assemble only the pinned Arithmancer WebGL player into Pages."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import sys
import zipfile


def assemble(archive, site, manifest):
    archive, site = Path(archive), Path(site)
    if hashlib.sha256(archive.read_bytes()).hexdigest() != manifest['sha256']:
        raise ValueError('Arithmancer archive checksum does not match the reviewed release')
    if not (site / 'index.html').is_file():
        raise ValueError('Assemble the main site first')
    destination = site / 'betas/arithmancer'
    if destination.exists():
        raise ValueError('Arithmancer destination must be fresh')
    with zipfile.ZipFile(archive) as source:
        files, seen, total = [], set(), 0
        for entry in source.infolist():
            name = entry.filename
            path = PurePosixPath(name)
            if '\\' in name or path.is_absolute() or '..' in path.parts or stat.S_ISLNK(entry.external_attr >> 16):
                raise ValueError('Unsafe archive path: ' + name)
            if entry.is_dir():
                continue
            if name.casefold() in seen:
                raise ValueError('Duplicate archive path: ' + name)
            seen.add(name.casefold())
            allowed = name == 'index.html' or (path.parts[0] in ('Build', 'StreamingAssets') and path.suffix.lower() in ('.js', '.unityweb', '.wasm', '.data', '.bundle', '.json', '.hash', '.bin'))
            if not allowed or any(x in name.lower() for x in ('symbols', 'provenance', 'sourcemap', 'donotship')):
                raise ValueError('Unexpected player file: ' + name)
            total += entry.file_size
            if total > 500 * 1024 * 1024:
                raise ValueError('Player exceeds the reviewed size budget')
            files.append(entry)
        if 'index.html' not in seen or not any(x.filename.endswith('.loader.js') for x in files):
            raise ValueError('Unity entry point or loader missing')
        html = source.read('index.html').decode('utf-8')
        if 'noindex, nofollow' not in html or 'matchWebGLToCanvasSize: true' not in html:
            raise ValueError('Beta indexing policy or responsive canvas configuration missing')
        # Validate the complete archive before writing anything into the Pages output.
        for entry in files:
            output = destination.joinpath(*PurePosixPath(entry.filename).parts)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(source.read(entry))
    return {'route': '/betas/arithmancer/', 'files': len(files), 'bytes': total, 'release': manifest['release']}


if __name__ == '__main__':
    config = json.loads(Path('betas/arithmancer.release.json').read_text())
    print(json.dumps(assemble(sys.argv[1], sys.argv[2], config)))
