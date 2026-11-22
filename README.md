# 🌱 CropVanta.AI
### AI-Powered Agricultural Intelligence, Crop Recommendation & Decision Support Platform

<p align="center">
  <img src="images/Crop.png" width="120" alt="CropVanta.AI Logo" />
</p>

<p align="center">
  <strong>Turning agricultural data into intelligent, explainable and actionable decisions.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?logo=python" />
  <img src="https://img.shields.io/badge/Machine%20Learning-Scikit--learn-orange" />
  <img src="https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi" />
  <img src="https://img.shields.io/badge/Frontend-Streamlit-red?logo=streamlit" />
  <img src="https://img.shields.io/badge/Database-MySQL-blue?logo=mysql" />
  <img src="https://img.shields.io/badge/Cache-Redis-red?logo=redis" />
  <img src="https://img.shields.io/badge/License-Apache%202.0-green" />
</p>

---

## 1. Overview

**CropVanta.AI** is an agricultural intelligence and decision-support platform that combines machine learning, backend engineering, environmental information and agricultural research retrieval.

The platform is designed to help users evaluate crop suitability using soil and environmental parameters while providing supporting agricultural information through a unified application.

Its architecture combines:

- Machine-learning-based crop classification.
- A Random Forest and Gradient Boosting ensemble.
- A Streamlit-based user interface.
- FastAPI-based prediction and authentication services.
- MySQL-backed user persistence.
- Redis-based prediction caching.
- Agricultural information retrieval through web search.

The goal is to connect predictive machine learning with practical agricultural decision-support workflows.

## 2. Problem Statement

Agricultural decisions depend on multiple interacting factors:

- Soil nutrient availability.
- Temperature and humidity.
- Soil pH.
- Rainfall and environmental conditions.
- Crop-specific growing requirements.
- Agricultural information and market conditions.

These factors are often distributed across separate sources and tools.

CropVanta.AI aims to provide a unified technical platform where machine learning predictions and supporting agricultural information can be accessed through a common interface.

## 3. Core Features

### 3.1 Intelligent Crop Recommendation

The core recommendation engine uses a supervised multi-class classification approach.

**Input parameters:**

| Feature | Description |
|---|---|
| N | Nitrogen |
| P | Phosphorus |
| K | Potassium |
| Temperature | Environmental temperature |
| Humidity | Relative humidity |
| pH | Soil pH |
| Rainfall | Rainfall measurement |

The model evaluates these seven input features and predicts one of 22 crop classes.

**Ensemble architecture:**

- Random Forest Classifier.
- Gradient Boosting Classifier.
- Soft-voting prediction.
- Feature scaling.
- Label encoding.
- Model artifact validation.

### 3.2 Agricultural Research Retrieval

The agricultural research module uses DDGS-based web search to retrieve crop-related information.

It supports queries covering:

- Crop cultivation.
- Agricultural management.
- Crop-specific information from Indian agricultural sources.
- General crop-management references.

Retrieved results include titles, descriptions and source URLs.

**Important:** Retrieved web content is reference material, not automatically verified agricultural advice. Users should validate recommendations against local agricultural extension guidance.

### 3.3 FastAPI Backend

The backend provides a separate API service for application functionality.

Current integrations include:

- Crop prediction endpoint.
- Health monitoring endpoint.
- Authentication through an OAuth2 password-bearer flow with JWT access tokens.
- Request validation.
- Model and preprocessing artifact loading.
- Prediction response handling.

Interactive API documentation is available through FastAPI Swagger UI.

### 3.4 MySQL Persistence

MySQL integration supports persistent user and authentication records through SQLAlchemy.

The application supports configuration through environment variables.

### 3.5 Redis Prediction Caching

Redis is used to cache successful crop recommendation results.

Implementation details:

- SHA-256-derived cache keys.
- Model-version-aware cache identity.
- Seven-feature input identity.
- 3,600-second cache expiration.
- Cache fallback when Redis is unavailable.

The prediction service is designed to continue inference without Redis.

### 3.6 Streamlit Dashboard

The Streamlit application provides the user-facing interface.

It connects the application workflow with the underlying agricultural recommendation and information services.

### 3.7 Weather and Market Intelligence

The project also includes agricultural decision-support components for weather information and market-related insights.

Availability and accuracy of external information depend on the configured providers, data sources and API credentials.

---

## 4. Machine Learning Evaluation

### Dataset Summary

| Property | Value |
|---|---:|
| Total samples | 2,200 |
| Crop classes | 22 |
| Features | 7 |
| Samples per class | 100 |
| Missing values | 0 |
| Duplicate rows | 0 |

The dataset contains soil and environmental measurements associated with crop labels.

### Model Architecture

The recommendation engine uses a soft-voting ensemble:

1. Random Forest Classifier.
2. Gradient Boosting Classifier.
3. Probability aggregation through soft voting.
4. Final class prediction using the ensemble output.

The preprocessing workflow uses a fitted scaler and label encoder.

### Cross-Validation Results

**Evaluation method:** Stratified 5-fold cross-validation.

| Metric | Mean result |
|---|---:|
| Accuracy | 99.50% |
| Macro Precision | Approximately 99.50% |
| Macro Recall | Approximately 99.50% |
| Macro F1-score | Approximately 99.50% |

**Additional evaluation:**

- Holdout test accuracy: 99.545%.
- Holdout macro-F1: 99.545%.
- Cross-validation out-of-fold accuracy: 99.50%.

These results describe evaluation on the available dataset. They should not be interpreted as guaranteed prediction accuracy on unseen farms or real-world agricultural conditions.

Dataset provenance and independent external validation remain important considerations before production agricultural deployment.

---

## 5. System Architecture

```text
                  USER
                   |
                   v
          Streamlit Dashboard
                   |
          +--------+--------+
          |                 |
          v                 v
     FastAPI Service   Agricultural Research
          |             DDGS Search
          |
          v
     Input Validation
          |
          v
     Redis Cache Check
          |
      +---+---+
      |       |
     Hit     Miss
      |       |
      |       v
      |   Feature Preparation
      |       |
      |       v
      |   Fitted Scaler
      |       |
      |       v
      |   ML Ensemble
      |       |
      |       v
      |   Label Decoder
      |       |
      +-------+
          |
          v
     Prediction Response
          |
          v
     Streamlit Dashboard

     MySQL: User Persistence
     Redis: Prediction Cache
```

### Prediction Pipeline

1. Receive the seven agricultural input features.
2. Validate the request.
3. Generate a cache identity.
4. Check Redis for an existing prediction.
5. If there is a cache miss, prepare the input features.
6. Apply the fitted scaler.
7. Run the Random Forest and Gradient Boosting ensemble.
8. Decode the predicted crop class.
9. Store the successful result in Redis when available.
10. Return the prediction response.

---

## 6. Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python 3.11+ |
| Machine Learning | Scikit-learn |
| Data Processing | NumPy, Pandas |
| Model Persistence | Joblib |
| Backend | FastAPI |
| API Validation | Pydantic |
| Authentication | JWT, OAuth2 |
| Database | MySQL, SQLAlchemy |
| Caching | Redis |
| Frontend | Streamlit, JavaScript |
| Research Retrieval | DDGS |
| Containerization | Docker, Docker Compose |
| Visualization | Matplotlib, Seaborn |

---

## 7. Installation and Setup

### Prerequisites

- Python 3.11 or later.
- Git.
- Docker Desktop.
- MySQL and Redis services, either through Docker Compose or separately.

### Step 1: Clone the repository

```powershell
git clone --branch AdvanceWork https://github.com/dhakarshailendra829/CropVanta.AI.git

cd CropVanta.AI
```

### Step 2: Create a virtual environment

```powershell
py -3.11 -m venv .venv

.\.venv\Scripts\Activate.ps1
```

### Step 3: Install dependencies

```powershell
python -m pip install --upgrade pip

pip install -r requirements.txt
```

### Step 4: Configure environment variables

```powershell
Copy-Item .env.example .env
```

Configure the required database connection, Redis URL and authentication secret in `.env`.

Never commit `.env` or expose passwords, access tokens or secret keys.

### Step 5: Start MySQL and Redis

```powershell
docker compose up -d mysql redis
```

Verify the containers:

```powershell
docker compose ps
```

### Step 6: Initialize the database

```powershell
python -m scripts.setup_db
```

### Step 7: Start the FastAPI service

Open a separate PowerShell terminal:

```powershell
cd "C:\Users\Shailendra\Desktop\CropVanta.AI"

.\.venv\Scripts\Activate.ps1

uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload
```

### Step 8: Start the Streamlit dashboard

Open another terminal:

```powershell
cd "C:\Users\Shailendra\Desktop\CropVanta.AI"

.\.venv\Scripts\Activate.ps1

streamlit run app.py
```

---

## 8. API Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/health` | GET | API and model health |
| `/docs` | GET | Interactive API documentation |
| `/auth/token` | POST | JWT access-token authentication |
| `/predict` | POST | Crop recommendation |

### Health Check

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

Expected healthy response:

```json
{
  "status": "ok",
  "model_loaded": true,
  "model_version": "3.2.0-Ensemble"
}
```

For request schemas and response examples, use:

```text
http://127.0.0.1:8000/docs
```

---

## 9. Model Artifacts

The current ensemble integration uses three artifacts:

| Artifact | Purpose |
|---|---|
| `crop_ensemble_candidate.pkl` | Trained ensemble classifier |
| `scaler_candidate.pkl` | Fitted feature scaler |
| `label_encoder.pkl` | Crop class decoding |

The model expects the following feature order:

```python
[
    "N",
    "P",
    "K",
    "temperature",
    "humidity",
    "ph",
    "rainfall"
]
```

The artifacts must remain compatible with the installed Scikit-learn version and the application code.

**Repository note:** The candidate artifacts are excluded by the current `artifacts/` entry in `.gitignore`. If the API requires these files after cloning, include the three required model artifacts in the repository or provide a documented artifact installation process. Never commit credentials or unrelated runtime outputs.

---

## 10. Testing and Verification

Useful local verification commands:

### Python compilation

```powershell
python -m py_compile .\modules\crop_advisor.py .\api\main.py
```

### Redis health

```powershell
docker exec cropvanta-redis redis-cli ping
```

### MySQL health

```powershell
docker compose ps
```

### API health

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

For full application validation, test authentication, prediction requests, database persistence, Redis cache hits and Redis-unavailable fallback.

---

## 11. Security and Reliability

The project incorporates several backend reliability practices:

- Environment-based configuration.
- JWT access-token authentication.
- Password-protected database configuration.
- Request validation.
- Redis cache fallback.
- Separation of model inference and API services.
- Exclusion of local secrets and runtime files through `.gitignore`.

Do not publish real credentials, `.env` files, user databases, access tokens or private data.

---

## 12. Current Limitations

CropVanta.AI is an evolving agricultural decision-support project.

Important limitations include:

- Model evaluation is based on the available dataset.
- Independent real-world agricultural validation is not established.
- Per-feature input ranges do not guarantee that a combination is agronomically realistic.
- Prediction probabilities are not automatically calibrated confidence estimates.
- External weather and market data depend on provider availability.
- Retrieved web information requires independent verification.
- Local MySQL and Redis services must be configured separately.

The system should support agricultural decision-making, not replace qualified agronomic advice.

---

## 13. Future Development Roadmap

- Independent validation with geographically diverse agricultural datasets.
- Regional soil and climate suitability analysis.
- Crop yield estimation.
- Satellite and remote-sensing integration.
- Multilingual agricultural assistance.
- Improved uncertainty and out-of-distribution detection.
- More comprehensive market intelligence.
- Farmer-oriented advisory workflows.
- Monitoring and evaluation of model performance over time.

---

## 14. License

This project is licensed under the **Apache License 2.0**.

See [LICENSE](LICENSE) for details.

## 15. Author

**Shailendra Dhakad**

Artificial Intelligence · Machine Learning · Backend Development · Software Engineering

- GitHub: [dhakarshailendra829](https://github.com/dhakarshailendra829)
- Portfolio: [Personal Portfolio](https://dhakarshailendra829.github.io/)
- LinkedIn: [Professional Profile](https://www.linkedin.com/in/shailendra-dhakad-063a98292/)
- ORCID: [0009-0000-7365-3852](https://orcid.org/0009-0000-7365-3852)

---

<p align="center">
  <strong>CropVanta.AI 🌱</strong><br/>
  Intelligent Agricultural Decision Support<br/>
  Built with Python, Machine Learning and Backend Engineering.
</p>