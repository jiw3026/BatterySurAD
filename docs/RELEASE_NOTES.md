# BatterySurAD public release notes

## Kaggle Version 2 — defect-organized Core Release

- Four category archives: `Scratching.zip`, `Contamination.zip`, `Folding.zip`, `Denting.zip`.
- Each category contains `Front/` and `Back/`, preserving original zone-directory nesting.
- 5,909 original images and 5,916 JSON files selected by excluding names containing the augmentation pattern (`aug`).
- `dataset_manifest.csv` and `upload_checksums.csv` included.
- Original source archives were not altered by the release packaging script.

## Distinction from published paper

The PAKDD 2026 paper reports 129,405 images including augmented samples and an acquisition count of 8,559 images. Public Kaggle v2 contains 5,909 filename-classified original images, and does not represent the complete paper corpus. Counts are based on the provided eight local source archives and export convention; differences have not been exhaustively reconciled.

## Known limitations

- Scratching: 1,461 original images and 1,468 JSON files, so not all records can be assumed paired.
- Image–JSON pair validation has not been completed for this release.
- No verified normal-only training partition is supplied.
- Augmented image files and exact original augmentation recipes are not publicly distributed in this release.
- Benchmarks in the article are reported historical experiments; do not infer re-computation on this Core Release.

## Version 1 / Version 2

Version 1 was distributed as seven size-based shards (`batterysurad_originals_001`–`007`). Version 2 restructures the same filename-selected Core Release into four defect-based archives; this is a **packaging change**, not an additional data collection or experiment.
