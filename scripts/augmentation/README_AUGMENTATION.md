# BatterySurAD — augmentation example

This directory provides a **safe, reproducible example** for users of the BatterySurAD Core Release. It is based on transformation ideas appearing in the author's supplied working notebooks, especially `augment_with labels(json).ipynb`, `폴더 내 순회하며 증강_언제끝나.ipynb`, and `배터리 이미지 증강.ipynb`.

**Important scientific distinction:** These historical notebooks contain different implementations and experimental iterations. Some saved images were generated with *unchanged* LabelMe JSON coordinates even when geometrical transforms were applied, while an earlier notebook used keypoint-aware transforms. The exact historical per-image parameters and random seeds have not been established. **This code must not be described as an exact recreation of the 129,405-image PAKDD 2026 experimental dataset.** It is an illustrative new augmentation pipeline, not the published benchmark's original augmentation outputs.

## Requirements

Python 3.10+; install packages:

```bash
python -m pip install -r requirements-augmentation.txt
```

## Choose your paths

First extract the relevant Kaggle defect archive (`Scratching.zip`, `Contamination.zip`, `Folding.zip`, or `Denting.zip`) to a directory you control. Choose an **output directory that does not exist** and is on a disk with plenty of free space.

Windows PowerShell example (replace `D:\YOUR_DATASET_FOLDER` and `E:\YOUR_OUTPUT_FOLDER`):

```powershell
py augment_batterysurad.py --input "D:\YOUR_DATASET_FOLDER\Scratching\Front" --output "E:\YOUR_OUTPUT_FOLDER\demo"
```

This is a **dry run**: no files will be saved. For a tiny example with two images and two variants each:

```powershell
py augment_batterysurad.py --input "D:\YOUR_DATASET_FOLDER\Scratching\Front" --output "E:\YOUR_OUTPUT_FOLDER\demo" --max-samples 2 --num-aug 2 --run
```

To intentionally process *all* matching originals under the input directory:

```powershell
py augment_batterysurad.py --input "D:\YOUR_DATASET_FOLDER\Scratching\Front" --output "E:\YOUR_OUTPUT_FOLDER\full_front" --max-samples 0 --num-aug 10 --allow-large-run --run
```

**Do not run all images until the output disk can accommodate the generated data.** Original images are high resolution and outputs can reach hundreds of GB. The printed size estimate is a rough warning, not a guarantee. Start with `--max-samples 1` or `2`; ideally use an external SSD.

## Safety and behavior

- Default **dry run**, capped at **2 originals** and **2 variants**; full generation needs `--max-samples 0 --allow-large-run --run`.
- Input is read-only; output must be a *different*, not previously existing directory.
- JPG/PNG inputs and LabelMe JSON must have exactly matching basenames within the same zone directory. Unpaired files are skipped and counted. Some Core Release original JSONs are unmatched, so all images should **not** be assumed annotated.
- Uses deterministic per-file RNG seeds, writes an `augmentation_log.csv`, processes one image at a time, and supports Korean path names.
- Polygon coordinates are rotated with the image for rotation variants. Photometric variants keep coordinates unchanged. This corrects a potential label-misalignment issue in historical experimental notebooks; it does **not** retrospectively validate original augmented annotations.
- LabelMe `imageData` is set to `null` for outputs to avoid embedding another full image into every JSON. `imagePath`, `imageWidth`, and `imageHeight` are updated.
- There is no automatic normal-vs-defective train/test split. Avoid leakage: split by **original image identity** before generating train/test augmentations.
- The transform list is illustrative: brightness/contrast, rotation, Gaussian noise, blur, gamma. The paper reports broader augmentation parameters. Do not claim bitwise or benchmark-score reproducibility.
- Huge input ZIPs should not be extracted just to run this demo. Download a single defect/archive or start with a small sample. A Kaggle Notebook with constrained ephemeral disk space should not run full-dataset augmentation.

## Recommended publication approach

- Host **Core Release data** on Kaggle and cite the paper.
- Host this script and its documentation on GitHub; a separate Kaggle Notebook may demonstrate a single annotated image.
- If publishing novel model results based on newly generated augmentations, state the transform implementation/version/seed and distinguish those results from the historical paper benchmark.

**Paper:** Park et al., BatterySurAD, PAKDD 2026, DOI: https://doi.org/10.1007/978-981-92-1462-4_22
