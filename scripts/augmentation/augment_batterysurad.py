#!/usr/bin/env python3
"""Safe, optional BatterySurAD JPG + LabelMe JSON augmentation example.

Inspired by the author's shared historical notebooks; NOT a verified bitwise
reproduction of the augmented images in the PAKDD 2026 experiments.

Default behavior is PREVIEW ONLY (no writes). Use --run to create files.
Outputs always go to a new, separate directory and original input stays unchanged.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

import cv2
import numpy as np

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png'}
AUG_PATTERN = re.compile(r'(?:^|[_-])aug\d*(?=\.|[_-]|$)', re.IGNORECASE)


def is_original(path: Path) -> bool:
    return path.suffix.lower() in IMAGE_EXTENSIONS and not AUG_PATTERN.search(path.name)


def image_read(path: Path):
    array = np.fromfile(str(path), dtype=np.uint8)
    return cv2.imdecode(array, cv2.IMREAD_COLOR)


def image_save(path: Path, image: np.ndarray, jpeg_quality: int) -> None:
    suffix = path.suffix.lower()
    options = [cv2.IMWRITE_JPEG_QUALITY, jpeg_quality] if suffix in ('.jpg', '.jpeg') else []
    ok, encoded = cv2.imencode(suffix, image, options)
    if not ok:
        raise RuntimeError(f'Could not encode: {path}')
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded.tofile(str(path))


def choose_seed(global_seed: int, relative_path: Path, variant: int) -> int:
    key = f'{global_seed}|{relative_path.as_posix()}|{variant}'.encode('utf-8')
    return int.from_bytes(hashlib.sha256(key).digest()[:8], 'little')


def augment_image_and_labels(image, metadata, index, rng, rotation_limit, jpeg_quality):
    """Change image and polygon coordinates consistently for a rotation.

    This is a representative, conservative pipeline, NOT a historical replay.
    """
    h, w = image.shape[:2]
    out = image.copy()
    labels = json.loads(json.dumps(metadata, ensure_ascii=False))  # deep copy
    variant = (index - 1) % 5
    transform = None
    operation = 'identity'

    if variant == 0:  # photometric: no change to polygons
        alpha = float(rng.uniform(0.85, 1.15))
        beta = float(rng.uniform(-12, 12))
        out = np.clip(out.astype(np.float32) * alpha + beta, 0, 255).astype(np.uint8)
        operation = f'brightness_contrast(alpha={alpha:.4f}, beta={beta:.4f})'
    elif variant == 1:  # spatial change: apply affine to polygon points
        angle = float(rng.uniform(-rotation_limit, rotation_limit))
        transform = cv2.getRotationMatrix2D(((w-1)/2, (h-1)/2), angle, 1.0)
        out = cv2.warpAffine(out, transform, (w, h), flags=cv2.INTER_LINEAR,
                             borderMode=cv2.BORDER_REFLECT_101)
        operation = f'rotation(angle_deg={angle:.4f})'
    elif variant == 2:
        sigma = float(rng.uniform(2.0, 7.0))
        noise = rng.normal(0, sigma, out.shape).astype(np.float32)
        out = np.clip(out.astype(np.float32) + noise, 0, 255).astype(np.uint8)
        operation = f'gaussian_noise(sigma={sigma:.4f})'
    elif variant == 3:
        out = cv2.GaussianBlur(out, (3, 3), 0)
        operation = 'gaussian_blur(kernel=3)'
    else:
        gamma = float(rng.uniform(0.85, 1.15))
        lut = np.clip((np.arange(256) / 255.0) ** gamma * 255, 0, 255).astype(np.uint8)
        out = cv2.LUT(out, lut)
        operation = f'gamma(gamma={gamma:.4f})'

    if transform is not None:
        for shape in labels.get('shapes', []):
            pts = shape.get('points', [])
            if not pts:
                continue
            arr = np.asarray(pts, dtype=np.float64)
            if arr.ndim != 2 or arr.shape[1] != 2:
                raise ValueError('Unsupported LabelMe points shape')
            xy = np.concatenate([arr, np.ones((len(arr), 1))], axis=1) @ transform.T
            # Do not independently clamp polygon vertices; boundary-truncated
            # polygons may need human review.
            shape['points'] = xy.tolist()
    labels['imageData'] = None  # do not duplicate full image inside JSON
    labels['imageHeight'] = int(h)
    labels['imageWidth'] = int(w)
    return out, labels, operation


def discover(input_dir: Path):
    pairs, missing, invalid = [], [], []
    for path in sorted(input_dir.rglob('*')):
        if not path.is_file() or not is_original(path):
            continue
        annotation = path.with_suffix('.json')
        if not annotation.exists():
            missing.append(path.relative_to(input_dir).as_posix())
            continue
        pairs.append((path, annotation))
    return pairs, missing, invalid


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--input', required=True, help='YOUR EXTRACTED DATA DIRECTORY (e.g. D:\\BatterySurAD\\Scratching\\Front)')
    parser.add_argument('--output', required=True, help='NEW OUTPUT DIRECTORY (must not exist)')
    parser.add_argument('--num-aug', type=int, default=2, help='Augmented images per original, 1..10 (default: 2)')
    parser.add_argument('--max-samples', type=int, default=2, help='Maximum original images to process (default: 2). Use 0 for all.')
    parser.add_argument('--seed', type=int, default=2026)
    parser.add_argument('--rotate-max-deg', type=float, default=10.0)
    parser.add_argument('--jpeg-quality', type=int, default=90)
    parser.add_argument('--run', action='store_true', help='ACTUALLY write images. Without this flag: preview only')
    parser.add_argument('--allow-large-run', action='store_true', help='Required when --max-samples 0; high disk usage!')
    args = parser.parse_args()
    source = Path(args.input).expanduser().resolve()
    target = Path(args.output).expanduser().resolve()
    if not source.is_dir(): parser.error('Input directory does not exist. Extract a Kaggle archive first.')
    if source == target or source in target.parents or target in source.parents:
        parser.error('Input and output must be separate, neither nested inside the other.')
    if target.exists(): parser.error('Output directory already exists. Choose a new empty path to avoid overwrites.')
    if not 1 <= args.num_aug <= 10: parser.error('--num-aug must be between 1 and 10')
    if args.max_samples < 0: parser.error('--max-samples must be >= 0')
    if args.max_samples == 0 and not args.allow_large_run:
        parser.error('All originals requested: add --allow-large-run after confirming available disk space')
    if not 0 <= args.rotate_max_deg <= 10: parser.error('Rotation demo supports 0..10 degrees')
    if not 1 <= args.jpeg_quality <= 100: parser.error('Invalid JPEG quality')

    pairs, missing, _ = discover(source)
    selected = pairs if args.max_samples == 0 else pairs[:args.max_samples]
    source_bytes = sum(im.stat().st_size + js.stat().st_size for im,js in selected)
    # Conservative warning estimate (actual depends on encoding, image characteristics).
    estimated = source_bytes * (args.num_aug + 1) * 2
    free = shutil.disk_usage(target.parent).free if target.parent.exists() else None
    print(f'Found {len(pairs)} exact image/JSON pairs, {len(missing)} images without a matching JSON.')
    print(f'Selected {len(selected)} originals; creates up to {len(selected)*args.num_aug} augmented JPG/JSON pairs.')
    print(f'Input selected size: {source_bytes / 2**30:.3f} GiB')
    print(f'Conservative output budget estimate: {estimated / 2**30:.3f} GiB (not a guarantee)')
    if free is not None: print(f'Available output-disk space: {free / 2**30:.3f} GiB')
    print('Input files never modified. Missing annotation images will be skipped.')
    if not args.run:
        print('DRY RUN ONLY. Nothing was written. To create files, repeat with --run.')
        return 0
    if free is not None and free < estimated + 2*2**30:
        parser.error('Not enough free space for conservative output budget + 2 GiB reserve. Try --max-samples 1.')
    target.mkdir(parents=True, exist_ok=False)
    log_rows = []
    errors = []
    for img_path, ann_path in selected:
        rel = img_path.relative_to(source)
        try:
            image = image_read(img_path)
            if image is None: raise ValueError('Cannot decode image')
            with ann_path.open('r', encoding='utf-8-sig') as f: metadata = json.load(f)
            if not isinstance(metadata.get('shapes'), list):
                raise ValueError('JSON lacks a LabelMe shapes array')
            out_dir = target / rel.parent
            out_dir.mkdir(parents=True, exist_ok=True)
            for i in range(1, args.num_aug + 1):
                random_seed = choose_seed(args.seed, rel, i)
                rng = np.random.default_rng(random_seed)
                transformed, labels, operation = augment_image_and_labels(
                    image, metadata, i, rng, args.rotate_max_deg, args.jpeg_quality)
                stem = f'{img_path.stem}_aug{i}'
                out_img = out_dir / f'{stem}{img_path.suffix.lower()}'
                out_ann = out_dir / f'{stem}.json'
                labels['imagePath'] = out_img.name
                image_save(out_img, transformed, args.jpeg_quality)
                with out_ann.open('w', encoding='utf-8') as f:
                    json.dump(labels, f, indent=2, ensure_ascii=False)
                log_rows.append((rel.as_posix(), out_img.relative_to(target).as_posix(), operation, random_seed))
            print('Completed:',rel.as_posix())
        except Exception as e:
            errors.append((rel.as_posix(),str(e)))
            print('SKIPPED:',rel.as_posix(),str(e), file=sys.stderr)
    with (target / 'augmentation_log.csv').open('w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f);w.writerow(['source_image','augmented_image','operation','seed']);w.writerows(log_rows)
    with (target / 'skipped.csv').open('w', newline='', encoding='utf-8-sig') as f:
        w=csv.writer(f);w.writerow(['source_image','reason']);w.writerows(errors)
    print(f'Finished: {len(log_rows)} augmented image/JSON pairs, {len(errors)} failed originals.')
    print('IMPORTANT: illustrative pipeline only; not a bitwise recreation of the paper dataset.')
    return 0 if not errors else 1


if __name__ == '__main__':
    raise SystemExit(main())
