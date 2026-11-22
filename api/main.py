"""FastAPI inference/authentication service for CropVanta.AI."""

from pathlib import Path

import joblib

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from modules.core.auth import create_access_token, decode_access_token
from modules.core.schemas import CropInput, TokenResponse
from modules.core.user_store import authenticate_user
from modules.crop_advisor import CropAdvisor


ROOT = Path(__file__).resolve().parents[1]

# Candidate ensemble artifacts.
ARTIFACT_DIR = ROOT / "artifacts" / "ensemble_candidate"

MODEL_PATH = ARTIFACT_DIR / "crop_ensemble_candidate.pkl"
SCALER_PATH = ARTIFACT_DIR / "scaler_candidate.pkl"
ENCODER_PATH = ARTIFACT_DIR / "label_encoder.pkl"


app = FastAPI(
    title="CropVanta.AI Inference API",
    version="1.1.0",
    description=(
        "Crop recommendation inference using a "
        "Random Forest and Gradient Boosting ensemble "
        "with JWT bearer authentication."
    ),
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

advisor: CropAdvisor | None = None


@app.on_event("startup")
def load_model() -> None:
    global advisor

    required_files = [
        MODEL_PATH,
        SCALER_PATH,
        ENCODER_PATH,
    ]

    missing_files = [
        str(path)
        for path in required_files
        if not path.exists()
    ]

    if missing_files:
        raise RuntimeError(
            f"Required model artifacts missing: {missing_files}"
        )

    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    label_encoder = joblib.load(ENCODER_PATH)

    advisor = CropAdvisor(
        model=model,
        scaler=scaler,
        label_encoder=label_encoder,
    )

    print("CropVanta ensemble model loaded successfully.")
    print(f"Crop classes: {len(label_encoder.classes_)}")


def require_user(
    token: str = Depends(oauth2_scheme),
) -> dict:

    payload = decode_access_token(token)

    if not payload or not payload.get("sub"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "model_loaded": advisor is not None,
        "model_version": (
            advisor.version if advisor is not None else None
        ),
    }


@app.post("/auth/token", response_model=TokenResponse)
def issue_token(
    form: OAuth2PasswordRequestForm = Depends(),
) -> TokenResponse:

    user = authenticate_user(
        form.username,
        form.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(
        {
            "sub": user["email"],
            "role": user.get("role", "user"),
        }
    )

    return TokenResponse(access_token=token)


@app.post("/predict")
def predict(
    payload: CropInput,
    current_user: dict = Depends(require_user),
) -> dict:

    if advisor is None:
        raise HTTPException(
            status_code=503,
            detail="Prediction model is not loaded",
        )

    result = advisor.recommend_crop(payload)

    if result.get("status") == "error":
        raise HTTPException(
            status_code=500,
            detail=result.get("message", "Prediction failed"),
        )

    return result