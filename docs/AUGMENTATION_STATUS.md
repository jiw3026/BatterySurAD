# Augmentation code — publication status

BatterySurAD's manuscript describes augmentation using limited rotation, brightness/contrast changes, Gaussian noise, and blur. Historical user-supplied notebooks include multiple approaches (including OpenCV and Albumentations) and annotation-transform experiments.

**No single notebook has yet been verified to be the exact final pipeline used for all published augmented images.** Different image and polygon-transform code paths are present. For that reason, this kit does not release an unverified notebook as the official reproduction script or state that it regenerates the 129,405-image published corpus.

For a future code release: identify the final generation entrypoint, remove absolute local paths and notebook outputs, fix library versions and random seeds, save per-image transforms, verify polygon alignment on samples, and test on a tiny separate fixture. Then publish under a declared software license with the scope of reproduction explicitly stated.
