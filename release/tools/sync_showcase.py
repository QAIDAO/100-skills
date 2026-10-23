#!/usr/bin/env python3
"""Sync the local reviewed showcase into the repository's release allowlist.

Usage: python3 -I release/tools/sync_showcase.py [--check]
The source directory is intentionally ignored by Git; no research data is copied.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'showcase-2026-10'
DEST = ROOT / 'release/showcase'
FILES = {
    'index.html': 'index.html',
    '对外展示包.zip': '对外展示包.zip',
    'verification/web/cards-desktop.png': 'preview.png',
}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Check without writing files')
    args = parser.parse_args()
    for source in FILES:
        if not (SOURCE / source).is_file():
            parser.error(f'Missing reviewed source: {SOURCE / source}')
    checks = [json.loads((SOURCE / 'verification/web' / name).read_text())
              for name in ('checks.json', 'cards-checks.json')]
    if any(not item['pass'] for result in checks for item in result['checks']):
        parser.error('Source browser checks contain failures')
    with zipfile.ZipFile(SOURCE / '对外展示包.zip') as archive:
        if archive.testzip() or archive.read('index.html') != (SOURCE / 'index.html').read_bytes():
            parser.error('Offline bundle does not match the reviewed HTML')
    if not args.check:
        DEST.mkdir(parents=True, exist_ok=True)
        for source, target in FILES.items():
            shutil.copy2(SOURCE / source, DEST / target)
    for source, target in FILES.items():
        if not (DEST / target).is_file() or (SOURCE / source).read_bytes() != (DEST / target).read_bytes():
            parser.error(f'Out of sync: {target}')
    manifest = {'source': 'showcase-2026-10', 'files': {
        target: hashlib.sha256((DEST / target).read_bytes()).hexdigest()
        for target in FILES.values()
    }}
    if args.check:
        if json.loads((DEST / 'manifest.json').read_text()) != manifest:
            parser.error('Release manifest is out of sync')
    else:
        (DEST / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(f'OK: {len(FILES)} release files match the reviewed local showcase')

if __name__ == '__main__':
    main()
