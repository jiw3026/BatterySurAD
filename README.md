# BatterySurAD

**BatterySurAD: A Dataset for Anomaly Detection on Pouch-Type Reflective Battery Surfaces with Spatial Zone Annotations**

Research dataset for reflective pouch-type battery surface anomaly detection with four defect classes (scratching, contamination, folding, denting), two views (front/back), and 15 spatial zones.

## Paper

Park et al., *BatterySurAD: A Dataset for Anomaly Detection on Pouch-Type Reflective Battery Surfaces with Spatial Zone Annotations*, PAKDD (published version and DOI to be added).

## Dataset access

**Kaggle dataset:** _ADD VERIFIED PUBLIC KAGGLE LINK HERE_

The initial public release contains original image files and corresponding LabelMe JSON annotation files, where available. Augmented images from the full experimental dataset are **not** part of this core release. This release must not be represented as the full image set described in the paper.

### Snapshot of available local archive inventory (2026-11-23)

- 8 source ZIPs, approximately 497.90 GiB compressed.
- 5,909 filenames classified as original images, and 59,290 as augmented images.
- 5,916 original JSON files; some annotation/image pairs require verification.
- Approximate unpacked original-image + original-JSON payload: 52.52 GiB.

These are filename-based archive inventory counts, **not** a verified count of unique, fully paired research samples. The publication reports different dataset totals; these figures should not be silently conflated.

## Layout

Download one or more `batterysurad_originals_*.zip` shards from Kaggle, then extract them. Each shard retains the source archive name as a path prefix. File and folder names are not changed except for that prefix.

## Dataset preparation

`python scripts/prepare_release.py --src PATH_TO_SOURCE_ZIPS --out PATH_TO_EMPTY_OUTPUT_DIR`

This program selects images and JSONs without `aug` in their filenames, creates archive shards, checks their CRCs, and writes SHA-256 checksums. It does not delete or alter input archives. Running it is **not** required for users who download the prepared Kaggle archives.

## Baselines and reproducibility

The paper studies FastFlow, PatchCore, STPM, CutPaste, RD4AD, DFR and DINO/CLIP feature baselines. The source notebooks are currently being curated. Exact full-dataset augmentation reproduction has **not** been verified; the release should not claim bitwise reproducibility of augmented images. No benchmark numbers have been recomputed for this release.

## License and permissions

The paper announces a CC BY 4.0 dataset release. Public redistribution of the underlying images and annotations must be confirmed with the data owner/industry collaborator before upload. Once authorized, document the exact data license and any differing code license here.

## Citation

Please cite the published PAKDD paper; add verified DOI and proceedings bibliographic details before announcing the release.
