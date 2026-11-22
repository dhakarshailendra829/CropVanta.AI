# CropVanta interview evidence notes

## Implemented in this upgrade
- Streamlit dashboard remains the frontend.
- FastAPI service is added separately at `api/main.py`.
- FastAPI exposes `/health`, OAuth2 password-bearer token issuance at `/auth/token`, and authenticated `/predict`.
- SQLAlchemy model and user store use MySQL when `DATABASE_URL` is configured; CSV fallback remains when unset.
- Redis cache-aside logic is in `modules/core/cache.py`; the crop advisor checks cache before inference and writes successful predictions with a one-hour TTL.
- `Modelcode.py` now defines Random Forest + Gradient Boosting soft voting, but the candidate must pass evaluation before promotion.

## Not yet substantiated
- The current bundled CSV has 500 rows, while model metadata says 2,200 rows.
- Current bundled CSV yields very low test accuracy in a reproducible split. Do not claim 92% until the correct dataset and evaluation are restored.
- The API benchmark script measures actual `/predict` response times only when run locally with a configured user and services. Do not claim <200 ms until it prints that result under a documented environment.
- Deployment-complexity reduction of 40% has no baseline/measurement script; omit that metric unless you conduct a before/after study.
- Gradient Boosting ensemble is implemented as candidate training logic; it becomes the deployed prediction model only after a passing candidate is promoted.
