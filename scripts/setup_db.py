"""Create local folders and initialize MySQL tables when configured."""
import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]

def main() -> None:
    load_dotenv(ROOT / ".env")
    for folder in ("models", "data", "logs", "uploaded_papers"):
        (ROOT / folder).mkdir(parents=True, exist_ok=True)
    if os.getenv("DATABASE_URL", "").strip():
        from modules.core.database import initialize_database
        initialize_database()
        print("MySQL connection successful; users table created/verified.")
    else:
        print("DATABASE_URL not set. MySQL skipped; CSV fallback remains active.")

if __name__ == "__main__":
    main()
