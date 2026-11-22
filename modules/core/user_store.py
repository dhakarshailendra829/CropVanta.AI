"""User persistence: MySQL via SQLAlchemy when configured, CSV for local fallback."""
import csv
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from modules.core.auth import hash_password, verify_password
from modules.core.database import User, database_is_configured, get_session_factory, initialize_database

load_dotenv()
USERS_FILE = Path("data/users.csv")


def _use_database() -> bool:
    return database_is_configured()


def initialize_user_file():
    if _use_database():
        initialize_database()
        return
    if not USERS_FILE.exists():
        USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(USERS_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["full_name", "email", "hashed_password", "role"])


def create_user(full_name: str, email: str, password: str, role="user"):
    initialize_user_file()
    normalized_email = email.strip().lower()
    hashed = hash_password(password)

    if _use_database():
        SessionLocal = get_session_factory()
        try:
            with SessionLocal() as session:
                existing = session.scalar(select(User).where(User.email == normalized_email))
                if existing:
                    return False, "User already exists"
                session.add(User(full_name=full_name.strip(), email=normalized_email,
                                 hashed_password=hashed, role=role))
                session.commit()
            return True, "User created successfully"
        except IntegrityError:
            return False, "User already exists"
        except SQLAlchemyError:
            return False, "Database operation failed. Check database configuration."

    users = get_all_users()
    if any(user["email"].strip().lower() == normalized_email for user in users):
        return False, "User already exists"
    with open(USERS_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([full_name.strip(), normalized_email, hashed, role])
    return True, "User created successfully"


def get_all_users():
    if _use_database():
        initialize_database()
        SessionLocal = get_session_factory()
        with SessionLocal() as session:
            records = session.scalars(select(User).order_by(User.id)).all()
            return [{"full_name": u.full_name, "email": u.email,
                     "hashed_password": u.hashed_password, "role": u.role}
                    for u in records]

    if not USERS_FILE.exists():
        return []
    with open(USERS_FILE, mode="r", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def authenticate_user(email: str, password: str):
    normalized_email = email.strip().lower()
    if _use_database():
        initialize_database()
        SessionLocal = get_session_factory()
        try:
            with SessionLocal() as session:
                user = session.scalar(select(User).where(User.email == normalized_email))
                if user and verify_password(password, user.hashed_password):
                    return {"full_name": user.full_name, "email": user.email, "role": user.role}
        except SQLAlchemyError:
            return None
        return None

    for user in get_all_users():
        if user["email"].strip().lower() == normalized_email:
            if verify_password(password, user["hashed_password"]):
                return user
    return None
