"""SQLAlchemy persistence layer for CropVanta.AI.

Set DATABASE_URL to a MySQL SQLAlchemy URL, for example:
mysql+pymysql://user:password@localhost:3306/cropvanta
"""
from __future__ import annotations

import os
from functools import lru_cache
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import create_engine, String, DateTime, Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

load_dotenv()


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(30), nullable=False, default="user")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())


@lru_cache(maxsize=1)
def get_engine():
    database_url = os.getenv("DATABASE_URL", "").strip()
    if not database_url:
        raise RuntimeError("DATABASE_URL is not configured; CSV storage remains active.")
    return create_engine(
        database_url,
        pool_pre_ping=True,
        pool_recycle=1800,
        pool_size=5,
        max_overflow=10,
        future=True,
    )


@lru_cache(maxsize=1)
def get_session_factory():
    return sessionmaker(bind=get_engine(), autoflush=False, expire_on_commit=False)


def initialize_database() -> None:
    """Create application tables if they do not already exist."""
    Base.metadata.create_all(bind=get_engine())


def database_is_configured() -> bool:
    return bool(os.getenv("DATABASE_URL", "").strip())
