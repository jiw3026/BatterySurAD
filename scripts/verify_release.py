#!/usr/bin/env python3
"""Verify local BatterySurAD defect ZIPs against published SHA-256 checksums.

Only checks archive identity/integrity. Does not assess image/JSON annotation correctness.
"""
import argparse
import csv
import hashlib
from pathlib import Path
import sys
import zipfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dir', required=True, type=Path, help='Folder with downloaded defect ZIPs')
    parser.add_argument('--checksums', required=True, type=Path, help='downloaded upload_checksums.csv')
    parser.add_argument('--zip-crc', action='store_true', help='Also decompress all ZIP members to check CRCs (slow)')
    args = parser.parse_args()
    with args.checksums.open('r', encoding='utf-8-sig', newline='') as f:
        records = list(csv.DictReader(f))
    if not records:
        parser.error('Checksum CSV is empty')
    failed = False
    for row in records:
        name = row['file']
        p = args.dir / name
        if p.name != name or p.suffix.lower() != '.zip':
            print('SKIP invalid filename:', name)
            failed = True
            continue
        if not p.is_file():
            print('MISSING:', p)
            failed = True
            continue
        expected_bytes = int(row['size_bytes'])
        hasher = hashlib.sha256()
        with p.open('rb') as f:
            for chunk in iter(lambda: f.read(8 * 1024 * 1024), b''):
                hasher.update(chunk)
        ok = p.stat().st_size == expected_bytes and hasher.hexdigest().lower() == row['sha256'].lower()
        if ok and args.zip_crc:
            with zipfile.ZipFile(p) as z:
                ok = z.testzip() is None
        print(('PASS' if ok else 'FAIL') + ': ' + name)
        failed |= not ok
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
