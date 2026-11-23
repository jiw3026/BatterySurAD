# BatterySurAD

**BatterySurAD: A Dataset for Anomaly Detection on Pouch-Type Reflective Battery Surfaces with Spatial Zone Annotations**

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

**Kaggle:** [BatterySurAD Dataset — link to be activated after upload]

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

Download the `batterysurad_originals_*.zip` archives from Kaggle and extract the required archives.

The archives preserve the original source directory structure, with a source archive prefix to distinguish files.

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
