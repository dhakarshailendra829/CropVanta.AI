<p align="center">
  <b>🌱 CropVanta.AI: Advanced Agricultural Intelligence Ecosystem System</b><br/>
  <img src="images/Crop.png" width="120" alt="AI Crop Advisor Logo" /><br/>
  <b>AI‑Driven Crop Recommendation, Market Intelligence & Decision‑Support Platform</b><br/>
</p>
<p align="center">
  <img src="https://img.shields.io/badge/Artificial%20Intelligence-AI-green" />
  <img src="https://img.shields.io/badge/Machine%20Learning-Models-brightgreen" />
  <img src="https://img.shields.io/badge/Deep%20Learning-Neural%20Networks-blueviolet" />
  <img src="https://img.shields.io/badge/Smart-Agriculture-yellowgreen" />
  <img src="https://img.shields.io/badge/Precision-Farming-success" />
  <img src="https://img.shields.io/badge/Predictive-Analytics-orange" />
  <img src="https://img.shields.io/badge/Data--Driven-Decisions-blue" />
</p>
<p align="center">
  <a href="#-project-vision">Vision</a> •
  <a href="#-problem-context">Problem</a> •
  <a href="#-system-capabilities">Capabilities</a> •
  <a href="#-architecture--ml-pipeline">Architecture</a> •
  <a href="#-tech-stack">Tech Stack</a> •
  <a href="#-installation--usage">Usage</a>
</p>

## Project Vision
Modern agriculture is increasingly **data‑rich but insight‑poor**. Farmers today are surrounded by information — soil data, historical yields, weather forecasts, seasonal calendars, and market prices — yet most decisions are still made using **intuition, fragmented tools, or delayed reports**.
**AI Crop & Market Advisor** was built to bridge this gap.
The vision of this project is to create a **single intelligent dashboard** that combines **machine learning, environmental intelligence, and market analytics** to answer one critical question:
> *Which crop should I grow, when should I grow it, and how can I maximize its market value?*
This system transforms raw agricultural data into **clear, explainable, and actionable recommendations** that can be used by farmers, agri‑consultants, students, and agri‑tech platforms.

## 🌾 Problem Context
Agricultural decision‑making suffers from multiple systemic challenges:
* Crop selection often ignores **local soil suitability**
* Weather uncertainty affects yield and timing
* Market prices fluctuate and are rarely considered during planning
* Information is scattered across different sources
* Farmers lack access to **ML‑powered predictive tools**

As a result:
* Crop failures increase
* Profit margins shrink
* Resources such as water and fertilizer are misused
This project addresses these issues by providing an **end‑to‑end AI decision‑support system** instead of isolated predictions.

---

## System Capabilities 

### Intelligent Crop Recommendation Engine
At the core of the system lies a **supervised machine learning pipeline** trained on agricultural datasets containing:
* Environmental indicators
* Crop performance history
* Soil and land characteristics

The model predicts the **most suitable crop class** for given conditions using:

* Feature scaling & encoding
* Random Forest classifier
* Optional XGBoost model for enhanced accuracy
* Cross‑validation & hyperparameter tuning

Predictions are not shown as raw labels but are **contextualized inside a decision dashboard**.

---
### Sustainable Resource & Agrivoltaic Intelligence
The system now features a 2026-standard Resource Management module:
* **Real-time Solar Irradiance:** Monitors solar intensity ($W/m^2$) to calculate the feasibility of Solar Water Pumps.
* **Evapotranspiration (ET0) Analytics:** Uses FAO-56 standard logic to predict daily water loss from the soil.
* **Carbon Credit Estimator:** Automatically calculates $CO_2$ offset based on solar energy usage (1 kWh ≈ 0.85kg CO2 saved).
* **ROI Dashboard:** Converts renewable energy harvest into direct financial savings (₹).

---
### Weather‑Aware Decision Logic

Weather data plays a critical role in agriculture. This system integrates **short‑term weather intelligence** to:

* Adjust crop suitability signals
* Highlight climate risks
* Improve planning reliability
* Show weather conditions of tommorow

The dashboard surfaces weather information in a **human‑readable, actionable format** instead of raw forecasts.

---

### Market Price Intelligence

Beyond growing the right crop, profitability depends on **market timing and pricing**.

The Market Advisor module:
* Fetches crop market prices
* Associates recommendations with economic context
* Helps users align crop selection with revenue potential

This bridges the gap between **agronomic feasibility and economic viability**.

---

### Land & Soil Suitability Analysis

The system evaluates land capability and soil compatibility to ensure that recommendations are **physically realistic**, not just statistically probable.

This prevents high‑risk suggestions that could fail in real‑world conditions.

---

### Crop Calendar & Seasonal Planning

A calendar‑based advisory layer provides:

* Crop‑wise seasonal insights
* Suggested sowing and harvesting periods
* Alignment with regional agricultural cycles

This converts predictions into **actionable timelines**.

---

### AI Advisory, News & Chatbot Support

To make the system farmer‑friendly and exploratory:

* Latest agriculture‑related news is surfaced
* An AI chatbot answers contextual queries
* Insights are delivered in simple language

This transforms the dashboard from a tool into an **interactive advisor**.
## Technical Stack

| Layer | Technology | Application |
| :--- | :--- | :--- |
| **Language** | **Python 3.11+** | Core logic and backend processing. |
| **Machine Learning** | **Scikit-learn, Joblib** | Random Forest Classifier for predictive modeling. |
| **Data Science** | **Pandas, NumPy** | Feature engineering and data manipulation. |
| **Interface** | **Streamlit** | Custom CSS/HTML injection for Premium Dark-Mode UI. |
| **Geospatial** | **Folium** | Interactive mapping for land suitability analysis. |
| **APIs** | **OpenWeatherMap** | Real-time hyperlocal weather data fetching. |

---

## System Architecture & ML Pipeline
1. **Input Layer:** Captures Soil Minerals (N, P, K), pH, Temperature, and Rainfall.
2. **Transformation:** Data is passed through a scaling and encoding pipeline.
3. **Inference:** The **Random Forest Engine** performs multi-class classification to predict the best crop.
4. **Market Sync:** Real-time Mandi APIs fetch the latest prices for the recommended crop.
5. **Output:** A customized, responsive UI renders the insights via Glassmorphic cards.

---

## Tech Stack
### Machine Learning & Data Science
* Python
* NumPy, Pandas
* Scikit‑learn
* XGBoost 
* Joblib

### Visualization & Analysis

* Matplotlib
* Seaborn

### Dashboard & UI
* Streamlit
* Modular UI components
* PIL for image rendering

### External Intelligence
* Weather forecasting services
* Market price data
* Agriculture news sources

---

## Installation & Usage

### Clone Repository

```bash
git clone https://github.com/dhakarshailendra829/CropVanta.AI.git
cd CropVanta.AI
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Launch Dashboard

```bash
streamlit run app.py
```

---


## MySQL Persistence and Redis Caching

CropVanta supports optional infrastructure integrations:

- **MySQL + SQLAlchemy:** when `DATABASE_URL` is configured, user registration and authentication records are stored in the `users` table. The CSV user store remains a local fallback when `DATABASE_URL` is unset.
- **Redis:** when `REDIS_URL` is configured and reachable, successful crop recommendations are cached for 3,600 seconds. Cache keys include the model version and all seven input features. If Redis is unavailable, prediction continues without the cache.

### Configure locally

1. Copy `.env.example` to `.env` and fill in credentials.
2. Create a MySQL database named `cropvanta` (or update the database name in `DATABASE_URL`).
3. Install dependencies with `pip install -r requirements.txt`.
4. Start Redis and MySQL.
5. Run `python scripts/setup_db.py` to create the `users` table.
6. Start the application with `streamlit run app.py`.

The application does not bundle or automatically host MySQL or Redis; these services must be provided separately.

## Who This Project Is For

### Farmers & Agricultural Decision-Makers

This platform helps farmers move from intuition-based decisions to **data-driven crop planning** by combining crop suitability, weather intelligence, seasonal calendars, and market awareness in one place.

It supports:

* Smarter crop selection based on soil, climate, and land conditions
* Reduced risk from unpredictable weather patterns
* Better timing of sowing and harvesting

---

### Agri-Tech Startups & Product Teams

For agri-tech entrepreneurs and product builders, this project serves as a **reference architecture** for building intelligent agriculture platforms.

It demonstrates:

* How machine learning models can power real user decisions
* How to integrate ML outputs into a usable dashboard
* How multiple data sources (weather, market, land) can be unified into a single product

This makes it suitable as a prototype or foundation for scalable agri-AI solutions.

---

### Students, Researchers & Practitioners

This project can be used as a learning reference for:
* Applied machine learning in agriculture
* End-to-end ML system design 
* Translating predictions into actionable insights

---

### Farmers & Agricultural Decision-Makers

* Data-driven crop selection
* Seasonal and land-aware planning

### Students & Learners

* Applied machine learning in real-world agriculture
* End-to-end ML + UI integration

### Agri-Tech Startups & Prototypes

* Rapid experimentation platform
* Foundation for scalable smart-farming solutions

---

## Future Roadmap

* Crop yield prediction models
* Satellite & remote sensing integration
* Multi‑language dashboard support
* User Friendly Interface
* Real‑time commodity exchange feeds
* Added helpline to support farmers
---
## License

Apache License 2.0
© 2026 Shailendra Dhakad
---

## 👤Author

**Shailendra Dhakad**
Artificial Intelligence • Machine Learning • Backend Developer • Software Engineering 

---

<p align="center">
  <b>CropVanta.AI</b> 🌾 <br/>
  Advanced AI & Deep Learning based Agricultural Intelligence System <br/><br/>
  Version 2.0.1 <br/>
  Architected & Developed by Shailendra Dhakad <br/>
  AI Researcher & Machine Learning Engineer & Software Engineer <br/>
  Licensed under Apache License 2.0
</p>

---
# Note:- This Project is under improvements and upgraded soon.

## Interview-ready backend extensions (local development)

This branch adds an optional FastAPI inference/authentication service, SQLAlchemy-backed MySQL user persistence, and Redis cache-aside caching for crop recommendations. The Streamlit dashboard remains the user interface. These services are real code integrations, but they are only active when the corresponding services and environment variables are configured.

### Windows PowerShell setup

```powershell
# 1. Create and activate a Python environment
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# 3. Create local environment configuration
Copy-Item .env.example .env
# Edit .env and set unique MYSQL_ROOT_PASSWORD, MYSQL_PASSWORD and SECRET_KEY values

# 4. Start MySQL and Redis (Docker Desktop must be running)
docker compose up -d mysql redis

# 5. Create MySQL tables
python scripts/setup_db.py

# 6. Start the FastAPI service (Terminal 1)
uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload

# 7. Start the Streamlit dashboard (Terminal 2)
streamlit run app.py
```

FastAPI interactive docs: http://127.0.0.1:8000/docs
Health check: http://127.0.0.1:8000/health

### Model training and evaluation

```powershell
python Modelcode.py
```

The training script compares a Random Forest + Gradient Boosting soft-voting ensemble on a stratified held-out test split. It fits the scaler only on the training split, reports accuracy and macro-F1, and writes candidate files under `artifacts/ensemble_candidate/`. It does not overwrite the app's current model unless `PROMOTE_MODEL=1` is set and measured accuracy reaches `MIN_ACCURACY` (default 70%).

**Dataset validation warning:** the repository's included `data/crop_recommendation.csv` currently has 500 rows across 22 classes, while the checked-in model metadata describes 2,200 training rows. A test run on the included CSV produced very low held-out accuracy (about 4%) for the new ensemble. Do not claim 92% or promote this candidate using this CSV. Restore the original verified training dataset, check its provenance and label quality, then rerun evaluation before making an accuracy claim.

### Verify integrations

```powershell
# MySQL/Redis containers
docker compose ps

# Redis responds with PONG
docker exec cropvanta-redis redis-cli ping

# MySQL container health
docker exec cropvanta-mysql mysqladmin ping -h 127.0.0.1 -p

# API health
Invoke-RestMethod http://127.0.0.1:8000/health
```

For a real end-to-end latency claim, benchmark the `/predict` API over repeated requests with Redis both cold and warm, and report p50/p95 including network, authentication, cache and inference overhead. Model-only inference time is not end-to-end API latency.
