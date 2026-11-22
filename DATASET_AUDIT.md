# Dataset and model audit (19 November 2026)

The included `data/crop_recommendation.csv` contains 500 rows, seven numeric features (`N`, `P`, `K`, `temperature`, `humidity`, `ph`, `rainfall`), and 22 crop labels. The checked-in `models/model_metadata.json` says 2,200 training samples and 98.2% accuracy. Those figures do not match the dataset currently included in this ZIP.

I ran the new Random Forest + Gradient Boosting soft-voting training script on the included CSV with a stratified 80/20 split (`random_state=42`). The held-out test accuracy was 1.00% and macro-F1 was 0.0091. This is not acceptable for deployment and is not evidence of the resume's 92% claim. The script therefore did not promote or overwrite the existing model.

**Action required:** locate the original 2,200-row training dataset (or another traceable, valid dataset), verify the feature/label semantics and provenance, rerun the fixed train/test evaluation, and only then promote the ensemble. Do not manually edit metadata to claim 92%.
