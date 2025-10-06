import os
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split, RandomizedSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, top_k_accuracy_score
import joblib
import json
try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except Exception:
    XGBOOST_AVAILABLE = False

CROP_CSV = os.path.join(DATA_DIR, "crop_recommendation.csv")
WEATHER_CSV = os.path.join(DATA_DIR, "weather_data.csv")
MANDI_CSV = os.path.join(DATA_DIR, "mandi_prices.csv")

OUTPUT_MODEL = "crop_model.pkl"
OUTPUT_SCALER = "scaler.pkl"

print("Loading datasets...")
crop_df = pd.read_csv(CROP_CSV)
print(f"crop_recommendation.csv: {crop_df.shape}")

weather_df = pd.read_csv(WEATHER_CSV) if os.path.exists(WEATHER_CSV) else None
mandi_df = pd.read_csv(MANDI_CSV) if os.path.exists(MANDI_CSV) else None

crop_descriptions = {
    "Wheat": "Wheat is a cereal grain grown worldwide. Requires well-drained soil and moderate rainfall. Harvest in 3-4 months. Ideal for temperate climates.",
    "Rice": "Rice is a staple crop grown in waterlogged fields. Needs high rainfall and warm temperatures. Rich in carbohydrates and calories.",
    "Maize": "Maize is a versatile crop for food and fodder. Grows in fertile, well-drained soil. Requires moderate temperature and rainfall.",
    "Sugarcane": "Sugarcane is a tropical crop for sugar production. Needs long sunlight and abundant water. Harvested after 10-12 months.",
    "Cotton": "Cotton is grown in warm climates with moderate rainfall. Used for textile industry. Requires fertile, well-drained soil.",
    "Tomato": "Tomato is a widely cultivated vegetable. Requires warm climate, fertile soil, and regular watering. Harvest in 2-3 months.",
    "Potato": "Potato is a tuber crop grown in cool climates. Needs well-drained soil and moderate rainfall. Harvest in 3-4 months.",
    "Onion": "Onion is a bulb vegetable grown in well-drained soil. Requires moderate temperature and sunlight. Harvest in 3-4 months.",
    "Chili": "Chili is a spicy vegetable grown in warm climates. Requires fertile soil, regular watering, and sunlight. Harvest in 3-4 months.",
    "Brinjal": "Brinjal (Eggplant) grows in warm regions. Needs fertile soil and regular irrigation. Harvest in 3-5 months for best yield.",
    "Carrot": "Carrot is a root vegetable grown in cool climates. Requires loose, sandy soil and moderate rainfall. Harvest in 2-3 months.",
    "Cabbage": "Cabbage is a leafy vegetable requiring cool weather. Needs fertile soil and regular watering. Harvest in 3-4 months.",
    "Cauliflower": "Cauliflower is a cool-season vegetable. Requires well-drained soil and moderate rainfall. Harvest in 3-4 months.",
    "Peas": "Peas are grown in cool climates and require well-drained soil. Rich in protein and nutrients. Harvest in 2-3 months.",
    "Soybean": "Soybean is a legume crop grown in warm climates. Requires fertile soil and moderate rainfall. Harvest in 4-5 months.",
    "Millet": "Millet is a drought-resistant cereal grown in dry regions. Requires minimal water and grows fast. Harvest in 3-4 months."
}

print("Preparing features and labels...")

expected_features = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
X = crop_df[expected_features].copy()
y = crop_df['label'].astype(str).copy()

X = X.fillna(X.median())

le = LabelEncoder()
y_enc = le.fit_transform(y)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
joblib.dump(scaler, OUTPUT_SCALER)
print(f"Scaler saved to {OUTPUT_SCALER}")

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y_enc, test_size=0.2, random_state=42, stratify=y_enc)

print("Training Random Forest...")
rf = RandomForestClassifier(random_state=42, n_jobs=-1)
param_dist = {
    "n_estimators": [100, 200, 300, 500],
    "max_depth": [None, 6, 10, 20, 30],
    "min_samples_split": [2, 5, 10],
    "min_samples_leaf": [1, 2, 4],
    "bootstrap": [True, False]
}

rs = RandomizedSearchCV(rf, param_distributions=param_dist, n_iter=30,
                        scoring='accuracy', cv=4, verbose=1, random_state=42, n_jobs=-1)
rs.fit(X_train, y_train)

best_rf = rs.best_estimator_
joblib.dump(best_rf, OUTPUT_MODEL)
print(f"Random Forest model saved to {OUTPUT_MODEL}")

y_pred = best_rf.predict(X_test)
print("Test Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred, target_names=le.classes_))

cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(10,8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=le.classes_, yticklabels=le.classes_)
plt.title("Confusion Matrix")
plt.tight_layout()
plt.savefig("confusion_matrix.png")
plt.close()

def predict_crop(input_dict):
    """
    input_dict keys: N,P,K,temperature,humidity,ph,rainfall
    returns: recommended crop + description + top3
    """
    x = np.array([input_dict[f] for f in expected_features]).reshape(1, -1)
    x_scaled = scaler.transform(x)
    pred_idx = best_rf.predict(x_scaled)[0]
    pred_label = le.inverse_transform([pred_idx])[0]
    
    top3 = []
    if hasattr(best_rf, "predict_proba"):
        probs = best_rf.predict_proba(x_scaled)[0]
        top_idx = np.argsort(probs)[::-1][:3]
        top3 = [(le.inverse_transform([i])[0], float(probs[i])) for i in top_idx]
        
    desc = crop_descriptions.get(pred_label, "No description available.")
    return {"crop": pred_label, "description": desc, "top3": top3}

median_input = X.median().to_dict()
demo = predict_crop(median_input)
print("\nDemo prediction with median values:")
print(demo)