# BatterySurAD initial release notes

## Scope

The initial public dataset package includes original images and original JSON annotations selected from eight local source archives by filename convention (`aug` absent). Augmented experimental images are excluded from this package.

## Known inventory inconsistencies

- Archive inventory: 5,909 original image filenames; 5,916 original JSON filenames.
- `긁힘_앞.zip` has 729 original image filenames versus 736 JSON filenames.
- The archive inventory found 9 original images without a same-path `.json` counterpart (this may be due to naming/extensions); these are not confirmed missing annotations.
- Paper totals and release inventory have different coverage/counting and must not be equated until reconciled.

## Reproducibility disclosure

Augmentation notebooks exist in several revisions, but an exact-generation recipe (per-image parameters/seeds/environment) has not been confirmed. Do not claim that new augmentation runs reproduce the original augmented image bytes or the original paper evaluations.

## TODO before publishing publicly

- [ ] Confirm redistribution permissions for images and labels.
- [ ] Verify that released shards have uploaded successfully and are downloadable.
- [ ] Add verified Kaggle URL.
- [ ] Add confirmed DOI/citation.
- [ ] Add curated generation scripts and baseline result tables if available.
