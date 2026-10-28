#!/usr/bin/env python3
"""Sync the local reviewed showcase into the repository's release allowlist.

Usage: python3 -I release/tools/sync_showcase.py [--check]
The source directory is intentionally ignored by Git; no research data is copied.
Embedded SVG figures are split into visuals/ so every tracked file stays under 1MB;
the offline bundle (对外展示包.zip) is distributed outside Git.
"""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import re
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'showcase-2026-10'
DEST = ROOT / 'release/showcase'
SOURCES = ('index.html', '对外展示包.zip', 'verification/web/cards-desktop.png')
SVG_URI = re.compile(r'data:image/svg\+xml;base64,([A-Za-z0-9+/=]+)')

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def release_files():
    files = {}
    def extract(match):
        data = base64.b64decode(match.group(1))
        name = f'visuals/{sha256(data)[:16]}.svg'
        files[name] = data
        return name
    html = SVG_URI.sub(extract, (SOURCE / 'index.html').read_text(encoding='utf-8'))
    files['index.html'] = html.encode('utf-8')
    files['preview.png'] = (SOURCE / 'verification/web/cards-desktop.png').read_bytes()
    return dict(sorted(files.items()))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Check without writing files')
    args = parser.parse_args()
    for source in SOURCES:
        if not (SOURCE / source).is_file():
            parser.error(f'Missing reviewed source: {SOURCE / source}')
    checks = [json.loads((SOURCE / 'verification/web' / name).read_text())
              for name in ('checks.json', 'cards-checks.json')]
    if any(not item['pass'] for result in checks for item in result['checks']):
        parser.error('Source browser checks contain failures')
    with zipfile.ZipFile(SOURCE / '对外展示包.zip') as archive:
        if archive.testzip() or archive.read('index.html') != (SOURCE / 'index.html').read_bytes():
            parser.error('Offline bundle does not match the reviewed HTML')
    files = release_files()
    if not args.check:
        shutil.rmtree(DEST / 'visuals', ignore_errors=True)
        (DEST / '对外展示包.zip').unlink(missing_ok=True)
        for target, data in files.items():
            (DEST / target).parent.mkdir(parents=True, exist_ok=True)
            (DEST / target).write_bytes(data)
    for target, data in files.items():
        if not (DEST / target).is_file() or (DEST / target).read_bytes() != data:
            parser.error(f'Out of sync: {target}')
    extra = {f'visuals/{p.name}' for p in (DEST / 'visuals').iterdir()} - set(files)
    if extra or (DEST / '对外展示包.zip').exists():
        parser.error(f'Stale release files: {sorted(extra) or ["对外展示包.zip"]}')
    manifest = {'source': 'showcase-2026-10',
                'files': {target: sha256(data) for target, data in files.items()}}
    if args.check:
        if json.loads((DEST / 'manifest.json').read_text()) != manifest:
            parser.error('Release manifest is out of sync')
    else:
        (DEST / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(f'OK: {len(files)} release files match the reviewed local showcase')

if __name__ == '__main__':
    main()
