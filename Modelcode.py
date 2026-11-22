"""Train and evaluate a Random Forest + Gradient Boosting soft-voting ensemble.

IMPORTANT: The supplied repository CSV contains only 500 rows. The training
script evaluates on a held-out stratified test split and will NOT overwrite
production model files unless the measured accuracy reaches MIN_ACCURACY.
Set PROMOTE_MODEL=1 only after verifying the dataset and metrics.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier, VotingClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "crop_recommendation.csv"
MODEL_DIR = ROOT / "models"
EXPERIMENT_DIR = ROOT / "artifacts" / "ensemble_candidate"
FEATURES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
MIN_ACCURACY = float(os.getenv("MIN_ACCURACY", "0.70"))


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)
    required = FEATURES + ["label"]
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"Dataset is missing required columns: {missing}")
    if len(df) < 100:
        raise ValueError("At least 100 labelled rows are required for this evaluation.")

    X = df[FEATURES].apply(pd.to_numeric, errors="coerce")
    y_text = df["label"].astype(str).str.strip().str.lower()
    medians = X.median()
    X = X.fillna(medians)
    if X.isna().any().any():
        raise ValueError("One or more feature columns contain no usable numeric values.")

    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y_text)
    counts = pd.Series(y_text).value_counts()
    if counts.min() < 2:
        raise ValueError("Every crop class must have at least two rows for stratified splitting.")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    # Fit preprocessing ONLY on training data to avoid test-set leakage.
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    rf = RandomForestClassifier(
        n_estimators=300, max_features="sqrt", min_samples_leaf=1,
        class_weight="balanced", random_state=42, n_jobs=-1
    )
    gb = GradientBoostingClassifier(
        n_estimators=150, learning_rate=0.05, max_depth=2,
        min_samples_leaf=2, random_state=42
    )
    ensemble = VotingClassifier(
        estimators=[("random_forest", rf), ("gradient_boosting", gb)],
        voting="soft", weights=[2, 1]
    )
    print("Training Random Forest + Gradient Boosting soft-voting ensemble...")
    ensemble.fit(X_train_scaled, y_train)
    predictions = ensemble.predict(X_test_scaled)
    accuracy = float(accuracy_score(y_test, predictions))
    macro_f1 = float(f1_score(y_test, predictions, average="macro", zero_division=0))

    print(f"Rows: {len(df)} | Features: {len(FEATURES)} | Crop classes: {len(label_encoder.classes_)}")
    print(f"Held-out test accuracy: {accuracy:.4f} ({accuracy * 100:.2f}%)")
    print(f"Held-out macro F1: {macro_f1:.4f}")
    print("Classification report:")
    print(classification_report(
        y_test, predictions, labels=np.arange(len(label_encoder.classes_)),
        target_names=label_encoder.classes_, zero_division=0
    ))

    EXPERIMENT_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(ensemble, EXPERIMENT_DIR / "crop_ensemble_candidate.pkl")
    joblib.dump(scaler, EXPERIMENT_DIR / "scaler_candidate.pkl")
    joblib.dump(label_encoder, EXPERIMENT_DIR / "label_encoder.pkl")
    metadata = {
        "algorithm": "Soft Voting: RandomForestClassifier + GradientBoostingClassifier",
        "features": FEATURES,
        "classes": label_encoder.classes_.tolist(),
        "rows": int(len(df)),
        "test_size": 0.2,
        "random_state": 42,
        "accuracy": accuracy,
        "macro_f1": macro_f1,
        "confusion_matrix": confusion_matrix(y_test, predictions).tolist(),
        "trained_at_utc": datetime.now(timezone.utc).isoformat(),
        "scaler_fit_on_training_split_only": True,
    }
    (EXPERIMENT_DIR / "metrics.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(f"Candidate artifacts saved to: {EXPERIMENT_DIR}")

    promote = os.getenv("PROMOTE_MODEL", "0").strip() == "1"
    if promote and accuracy >= MIN_ACCURACY:
        MODEL_DIR.mkdir(parents=True, exist_ok=True)
        joblib.dump(ensemble, MODEL_DIR / "crop_model.pkl")
        joblib.dump(scaler, MODEL_DIR / "scaler.pkl")
        (MODEL_DIR / "model_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
        print("PROMOTED: ensemble model and scaler written to models/.")
    else:
        print("NOT PROMOTED: production model files were left unchanged.")
        if accuracy < MIN_ACCURACY:
            print(f"Accuracy {accuracy:.2%} is below MIN_ACCURACY={MIN_ACCURACY:.0%}.")
        if not promote:
            print("To promote after reviewing metrics: set PROMOTE_MODEL=1 and rerun.")


if __name__ == "__main__":
    main()
