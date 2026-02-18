import csv
import os
from pathlib import Path
from modules.core.auth import hash_password, verify_password

USERS_FILE = Path("data/users.csv")

def initialize_user_file():
    if not USERS_FILE.exists():
        USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(USERS_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["full_name", "email", "hashed_password", "role"])

def create_user(full_name: str, email: str, password: str, role="user"):
    initialize_user_file()

    users = get_all_users()
    for user in users:
        if user["email"] == email:
            return False, "User already exists"

    hashed = hash_password(password)

    with open(USERS_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([full_name, email, hashed, role])

    return True, "User created successfully"

def get_all_users():
    if not USERS_FILE.exists():
        return []

    with open(USERS_FILE, mode="r") as file:
        reader = csv.DictReader(file)
        return list(reader)

def authenticate_user(email: str, password: str):
    users = get_all_users()

    for user in users:
        if user["email"] == email:
            if verify_password(password, user["hashed_password"]):
                return user

    return None
