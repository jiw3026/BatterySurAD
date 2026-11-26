# BatterySurAD

**BatterySurAD: A Dataset for Anomaly Detection on Pouch-Type Reflective Battery Surfaces with Spatial Zone Annotations**

<<<<<<< HEAD
[![Paper: PAKDD 2026](https://img.shields.io/badge/Paper-PAKDD%202026-2563eb)](https://doi.org/10.1007/978-981-92-1462-4_22)
[![Dataset: Kaggle](https://img.shields.io/badge/Dataset-Kaggle-20beff)](https://www.kaggle.com/datasets/roseannejiwonpark/batterysurad)
[![Dataset license: CC BY 4.0](https://img.shields.io/badge/Dataset%20license-CC%20BY%204.0-228b22)](https://creativecommons.org/licenses/by/4.0/)

Official repository for the **BatterySurAD** dataset and benchmark, published at **PAKDD 2026**.

## Overview

BatterySurAD supports research on anomaly detection over reflective battery surfaces, where object geometry, viewing direction, and spatial location can affect anomaly appearance and model behavior.

- **Four defect types:** Scratching, Contamination, Folding, Denting
- **Two views:** Front and Back
- **15 spatial zones** per surface
- **LabelMe JSON** polygon annotations accompanying image files, subject to the availability notes below
- **Paper benchmarks:** FastFlow, PatchCore, STPM, CutPaste, RD4AD, DFR; additional DINO/CLIP feature baselines

The **published study** describes 129,405 images including augmentation, and reports zone-, defect-, and view-specific analyses. **This public Kaggle v2 Core Release is smaller:** it contains only original (non-`aug`) images and available corresponding JSON files. It must not be confused with the full augmented experimental corpus.

## Dataset download

**[Download BatterySurAD on Kaggle](https://www.kaggle.com/datasets/roseannejiwonpark/batterysurad)**

### Core Release (Kaggle Version 2)

| Defect | Original images | JSON files |
| --- | ---: | ---: |
| Scratching | 1,461 | 1,468 |
| Contamination | 1,501 | 1,501 |
| Folding | 1,452 | 1,452 |
| Denting | 1,495 | 1,495 |
| **Total** | **5,909** | **5,916** |

*Counts reflect filename-based export inventory, not confirmation of every image–annotation match. In particular, the Scratching group has seven more JSON files than original images. The release uses the source archives' original filenames without renaming their individual records.*

Kaggle Data Explorer organizes the release by defect and view:

```text
BatterySurAD/
├── Scratching/
│   ├── Front/
│   └── Back/
├── Contamination/
│   ├── Front/
│   └── Back/
├── Folding/
│   ├── Front/
│   └── Back/
├── Denting/
│   ├── Front/
│   └── Back/
├── dataset_manifest.csv
└── upload_checksums.csv
```

The four distribution archives are `Scratching.zip`, `Contamination.zip`, `Folding.zip`, and `Denting.zip`. Each includes its corresponding `Front/` and `Back/` folders and preserves any nested source-zone directories. When extracting locally, use one folder per ZIP (named after the defect) to obtain the layout shown above.

- `dataset_manifest.csv`: released archive name, logical path, source archive/member, and byte size for each exported image/JSON.
- `upload_checksums.csv`: SHA-256 digest and byte size of each distribution ZIP, for integrity checking.

Run `python scripts/verify_release.py --dir PATH_TO_DOWNLOADED_ZIPS --checksums PATH_TO_CHECKSUM_CSV` to verify downloaded archives against published checksums. This check does **not** establish annotation correctness or image/JSON completeness.

## Annotation and reuse notes

Images are grouped by four defects, two inspection views, and zone directories. Annotation files follow the **LabelMe JSON** convention. The current Core Release is not a cleanly verified one-to-one annotation corpus: use `dataset_manifest.csv` and pair image/JSON files by relative path and basename in your data loader, and handle unmatched records explicitly.

**Important:** the Core Release currently includes anomaly examples, not a verified normal-only training partition. The published DINO/CLIP study used surrogate difficulty labels based on annotation area because normal-only data were not available for that setting. Do not assume this release directly supplies standard normal-train/anomaly-test splits.

## Reproducibility status

The paper reports the benchmark protocols and results for classical anomaly detectors and foundation-feature baselines. The source augmentation notebooks contain multiple historical experiments; the exact final image-by-image augmentation recipe, random states, library versions, and polygon transformations have **not** been established as bitwise reproducible. Pre-generated augmented images, trained weights, model predictions, and full precomputed embeddings are **not included in this Core Release** unless explicitly added in a future version.

The archived Kaggle Version 1 used size-based distribution shards; the current Version 2 presents defect-based folders. See [Release notes](docs/RELEASE_NOTES.md) for known differences.

## Citation

**If you use BatterySurAD or any subset of its images or annotations in research, please cite the original paper:**

> Park, J., Kim, D., Choi, B., Lee, G., & Oh, H. (2026). BatterySurAD: A Dataset for Anomaly Detection on Pouch-Type Reflective Battery Surfaces with Spatial Zone Annotations. In *Advances in Knowledge Discovery and Data Mining*, PAKDD 2026, LNCS 16598. Springer, Singapore. https://doi.org/10.1007/978-981-92-1462-4_22

```bibtex
@incollection{park2026batterysurad,
  title     = {BatterySurAD: A Dataset for Anomaly Detection on Pouch-Type Reflective Battery Surfaces with Spatial Zone Annotations},
  author    = {Park, Jiwon and Kim, Dohwan and Choi, Bongseok and Lee, Giljun and Oh, Hayoung},
  booktitle = {Advances in Knowledge Discovery and Data Mining},
  series    = {Lecture Notes in Computer Science},
  volume    = {16598},
  year      = {2026},
  publisher = {Springer},
  doi       = {10.1007/978-981-92-1462-4_22}
}
```

GitHub also provides **Cite this repository** using [CITATION.cff](CITATION.cff).

## License

**Dataset:** [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). Attribution is required by the license; formal academic paper citation is additionally requested for scholarly use. License treatment of any separately released software should be specified when that software is published.

## Questions and corrections

Please open a GitHub Issue and include the defect, view, zone, filename, and a description of the issue. Do not submit private credentials or restricted production information.
=======
Official repository for **BatterySurAD**, presented at the Pacific-Asia Conference on Knowledge Discovery and Data Mining (**PAKDD 2026**).

[![Paper](https://img.shields.io/badge/Paper-PAKDD%202026-blue)](https://doi.org/10.1007/978-981-92-1462-4_22)
![License](https://img.shields.io/badge/Dataset%20License-CC%20BY%204.0-green)

## Overview

BatterySurAD is a benchmark dataset designed to investigate anomaly detection on reflective pouch-type battery surfaces.

Unlike conventional industrial anomaly detection benchmarks focusing primarily on flat surfaces, BatterySurAD considers spatial heterogeneity, reflective material characteristics, and view-dependent anomaly detection challenges.

The dataset incorporates:

- **4 defect categories:** Scratching, Contamination, Folding, and Denting
- **2 inspection views:** Front and Back
- **15 spatial zones:** Fine-grained spatial annotations
- **Polygon annotations:** LabelMe JSON format
- **Benchmark evaluations:** Classical anomaly detection models and foundation-model baselines

The published paper reports 129,405 images, including augmented samples, and investigates zone-dependent detection difficulty, reflective surface domain shifts, and model-specific failure patterns.

## Dataset Access

**Kaggle:** [Download BatterySurAD](https://www.kaggle.com/datasets/roseannejiwonpark/batterysurad)

### Core Release

The initial release provides original battery surface images and corresponding LabelMe JSON annotation files, where available.

| Component | Core Release |
|---|---|
| Original images | 5,909 |
| Original JSON annotation files | 5,916 |
| Defect categories | 4 |
| Inspection views | 2 |
| Spatial zones | 15 |
| Format | JPG / JSON |
| Distribution | 7 ZIP archives |

**Note:** The core release differs from the full experimental dataset described in the paper. Pre-generated augmented images are not included. Image and annotation counts are based on the release archive inventory; complete one-to-one pairing has not been established.

### Download and Preparation

Download the four defect-specific archives from Kaggle:

- `Scratching.zip`
- `Contamination.zip`
- `Folding.zip`
- `Denting.zip`

Each archive contains `Front/` and `Back/` directories, preserving the original zone-level subdirectories and corresponding image and LabelMe JSON files.

Users may download individual defect categories according to their research requirements.

## Data Augmentation

A reference augmentation pipeline is provided in [`scripts/augmentation/`](scripts/augmentation/).

The implementation supports LabelMe polygon-aware augmentation, including geometric and photometric transformations. Users can specify their own input and output directories.

**Storage warning:** The original dataset contains high-resolution images, and full augmentation may generate hundreds of GiB of additional files. Run a small sample first and verify available storage before processing the entire dataset.

This implementation is a reference augmentation pipeline derived from the original research workflow. It does not guarantee exact reproduction of the pre-generated augmented images used in the published PAKDD 2026 experiments.

A demonstration notebook is also provided in [`notebooks/`](notebooks/).

## Benchmark and Reproducibility

The BatterySurAD paper evaluates the following anomaly detection methods:

**Classical anomaly detection**
- PatchCore
- FastFlow
- STPM
- CutPaste
- RD4AD
- DFR

**Foundation-model baselines**
- DINO
- CLIP

The paper investigates performance differences across defect categories, inspection views, and spatial zones.

The original benchmark results are reported in the published paper. Source notebooks and augmentation procedures are being organized for public release.

Exact reproduction of the pre-generated augmented images is not yet verified.

## Publication

**Park, J., Kim, D., Choi, B., Lee, G., & Oh, H. (2026).**

BatterySurAD: A Dataset for Anomaly Detection on Pouch-Type Reflective Battery Surfaces with Spatial Zone Annotations.

*Advances in Knowledge Discovery and Data Mining (PAKDD 2026).* Lecture Notes in Computer Science, Vol. 16598. Springer, Singapore.

**DOI:** https://doi.org/10.1007/978-981-92-1462-4_22

## Citation

If you use BatterySurAD, in whole or in part, in your research, experiments, publications, or benchmarks, **please cite the original PAKDD 2026 paper.**

```bibtex
@incollection{park2026batterysurad,
  title={BatterySurAD: A Dataset for Anomaly Detection on Pouch-Type Reflective Battery Surfaces with Spatial Zone Annotations},
  author={Park, Jiwon and Kim, Dohwan and Choi, Bongseok and Lee, Giljun and Oh, Hayoung},
  booktitle={Advances in Knowledge Discovery and Data Mining},
  series={Lecture Notes in Computer Science},
  volume={16598},
  year={2026},
  publisher={Springer},
  doi={10.1007/978-981-92-1462-4_22}
}
```

## License

The BatterySurAD dataset is released under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license.

Users must provide appropriate attribution to the dataset creators and source, retain license information, and indicate modifications where applicable.

Citation of the original research paper is strongly requested for academic use.

Code licensing, where applicable, is documented separately.

## Contact and Issues

For dataset-related questions, annotation issues, or reproducibility inquiries, please open a GitHub Issue.

---

**BatterySurAD · PAKDD 2026 · Springer LNCS 16598**
>>>>>>> 028a4fe1fe30019f33cf6675abe8834a9140755f
