# FastAPI service

- `GET /health`: service/model status.
- `POST /auth/token`: OAuth2 password-bearer token endpoint (form fields `username` and `password`).
- `POST /predict`: authenticated crop recommendation endpoint; send the seven CropInput fields as JSON.
- `GET /docs`: Swagger UI.

The API uses the existing user store. Configure `DATABASE_URL`, `REDIS_URL`, and `SECRET_KEY` in `.env` before testing.
