#!/usr/bin/env python3
"""Read-only inventory and optional copy-out of non-augmented JPG + companion JSON from ZIPs.
Python 3.9+. No third-party dependencies. Does not change source ZIPs.
"""
import argparse, csv, hashlib, json, re, shutil, sys, zipfile
from pathlib import Path, PurePosixPath

IMG = {'.jpg', '.jpeg', '.png', '.tif', '.tiff', '.bmp'}
AUG = re.compile(r'(?:^|[_\-])aug(?:ment(?:ed|ation)?)?[_\-]?\d*(?=\.|[_\-]|$)', re.I)
FIELDS=['archive','member','kind','is_aug','size_bytes','compressed_bytes','paired_json']

def classify(name):
    base=PurePosixPath(name.replace('\\','/')).name
    ext=PurePosixPath(base).suffix.lower()
    if ext in IMG: kind='image'
    elif ext == '.json': kind='json'
    else: kind='other'
    return kind, bool(AUG.search(base))

def collect(src):
    zips=sorted(src.glob('*.zip'))
    if not zips: raise RuntimeError('No ZIP files found in folder: '+str(src))
    dataset=[]; entries=[]
    for path in zips:
        print('Scanning:',path.name,flush=True)
        with zipfile.ZipFile(path) as z:
            members=[i for i in z.infolist() if not i.is_dir()]
            names={i.filename for i in members}
            stats={'zip':path.name,'zip_bytes':path.stat().st_size,'entries':len(members),'original_images':0,'aug_images':0,'original_json':0,'aug_json':0,'other':0,'original_payload_bytes':0,'original_compressed_bytes':0,'missing_original_json':0}
            for i in members:
                kind,aug=classify(i.filename)
                if kind=='image':
                    stats['aug_images' if aug else 'original_images']+=1
                elif kind=='json': stats['aug_json' if aug else 'original_json']+=1
                else: stats['other']+=1
                partner=str(PurePosixPath(i.filename).with_suffix('.json')) if kind=='image' and not aug else ''
                paired=(partner in names) if partner else ''
                if kind=='image' and not aug and not paired: stats['missing_original_json']+=1
                if kind in ('image','json') and not aug:
                    stats['original_payload_bytes']+=i.file_size
                    stats['original_compressed_bytes']+=i.compress_size
                entries.append(dict(archive=path.name,member=i.filename,kind=kind,is_aug=aug,size_bytes=i.file_size,compressed_bytes=i.compress_size,paired_json=paired))
            dataset.append(stats)
    return zips,dataset,entries

def csvwrite(path, rows, headers):
    with path.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=headers,extrasaction='ignore');w.writeheader();w.writerows(rows)

def export(zips,entries,target,max_gib):
    if target.exists() and any(target.iterdir()): raise RuntimeError('Output directory must be empty: '+str(target))
    selected=[r for r in entries if r['kind'] in ('image','json') and not r['is_aug']]
    raw=sum(r['size_bytes'] for r in selected)
    required=min(raw, int(max_gib*1024**3))+2*1024**3
    free=shutil.disk_usage(target.parent).free
    print(f'Estimated uncompressed original + JSON: {raw/1024**3:.2f} GiB')
    print(f'Free space at output: {free/1024**3:.2f} GiB')
    if free < required:
        raise RuntimeError('Not enough free space for safe processing even one shard. Use external drive as --out.')
    target.mkdir(parents=True,exist_ok=True)
    checks=[]; maxb=int(max_gib*1024**3); shard=0; outf=None; outsize=0; written=0
    try:
        for src in zips:
            chosen=[r for r in selected if r['archive']==src.name]
            with zipfile.ZipFile(src) as inp:
                for r in chosen:
                    member=inp.getinfo(r['member'])
                    if member.file_size > maxb: raise RuntimeError('One member larger than shard size: '+member.filename)
                    # Store images without recompressing JPEG; compress JSON normally.
                    if outf is None or (outsize and outsize+member.file_size > maxb):
                        if outf: outf.close()
                        shard+=1; p=target/f'batterysurad_originals_{shard:03d}.zip'
                        outf=zipfile.ZipFile(p,'w',allowZip64=True)
                        checks.append({'file':p.name})
                        outsize=0
                        print('Writing:',p.name,flush=True)
                    suffix=PurePosixPath(member.filename).suffix.lower()
                    typ=zipfile.ZIP_STORED if suffix in IMG else zipfile.ZIP_DEFLATED
                    arcname=f'{src.stem}/{member.filename.replace(chr(92), "/")}'
                    with inp.open(member) as reader, outf.open(zipfile.ZipInfo(arcname), 'w',force_zip64=True) as writer:
                        # output ZIP member streams are stored uncompressed; do not require memory
                        while True:
                            buf=reader.read(4*1024*1024)
                            if not buf: break
                            writer.write(buf)
                    outsize+=member.file_size
                    written+=1
    finally:
        if outf: outf.close()
    # Validate generated ZIP member CRCs before suggesting any upload.
    for item in checks:
        path=target/item['file']
        with zipfile.ZipFile(path) as z:
            first_bad=z.testzip()
            if first_bad: raise RuntimeError(f'CRC mismatch in {path.name}: {first_bad}')
        h=hashlib.sha256()
        with path.open('rb') as f:
            for buf in iter(lambda:f.read(8*1024*1024),b''): h.update(buf)
        item['sha256']=h.hexdigest();item['bytes']=path.stat().st_size
    csvwrite(target/'upload_checksums.csv',checks,['file','sha256','bytes'])
    print(f'Exported {written} images/JSON files into {len(checks)} verified ZIP shard(s).')
    print('Important: Original 8 ZIPs were NOT changed. Do not delete until you verify download and backups.')

def main():
    p=argparse.ArgumentParser(description='Inventory BatterySurAD ZIP archives, optionally export only files without aug in filename.')
    p.add_argument('--src',required=True,help='Folder with 8 ZIPs')
    p.add_argument('--report',default='',help='Folder for small CSV report (default: current folder)')
    p.add_argument('--out',default='',help='Optional EMPTY output folder for original+JSON ZIP shards; best on external drive')
    p.add_argument('--shard-gib',type=float,default=8.0,help='Target maximum uncompressed payload per ZIP shard (default 8GiB)')
    args=p.parse_args()
    src=Path(args.src).expanduser().resolve(); report=Path(args.report or '.').expanduser().resolve()
    report.mkdir(parents=True,exist_ok=True)
    zips,stats,entries=collect(src)
    csvwrite(report/'batterysurad_archive_summary.csv',stats,list(stats[0].keys()))
    csvwrite(report/'batterysurad_file_manifest.csv',entries,FIELDS)
    print('\nSummary:')
    for s in stats: print(f"{s['zip']}: original {s['original_images']} images; aug {s['aug_images']} images; original JSON {s['original_json']} ")
    print('Source ZIP total: %.2f GiB'%(sum(s['zip_bytes'] for s in stats)/1024**3))
    print('Original image + JSON unpacked estimate: %.2f GiB'%(sum(s['original_payload_bytes'] for s in stats)/1024**3))
    print('Reports saved:',report)
    if args.out:
        if args.shard_gib <= 0: raise RuntimeError('--shard-gib must be positive')
        export(zips,entries,Path(args.out).expanduser().resolve(),args.shard_gib)

if __name__=='__main__':
    try:main()
    except Exception as e:
        print('ERROR:',e,file=sys.stderr); sys.exit(1)
