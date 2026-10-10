import os
import jwt
from datetime import datetime, timedelta, timezone
from werkzeug.security import check_password_hash
from models.auth_model import register_user, get_user_by_email
from dotenv import load_dotenv
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env", override=True)

load_dotenv()


def register_service(data):
    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name or not email or not password:
        return {"error": "Name, email and password are required"}, 400

    if len(password) < 8:
        return {"error": "Password must contain at least 8 characters"}, 400

    hashed_password = generate_password_hash(password)

    try:
        user = register_user(name, email, hashed_password)
        return {"message": "Registration successful", "user": user}, 201

    except Exception as e:
        if getattr(e, "pgcode", None) == "23505":
            return {"error": "Email already registered"}, 409

        return {"error": "Registration failed"}, 500

def login_service(data):
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return {"error": "Email and password are required"}, 400

    user = get_user_by_email(email)

    if not user or not check_password_hash(user[3], password):
        return {"error": "Invalid email or password"}, 401

    secret_key = os.getenv("JWT_SECRET_KEY")

    if not secret_key:
        return {"error": "JWT configuration missing"}, 500

    token = jwt.encode(
        {
            "user_id": user[0],
            "role": user[4],
            "exp": datetime.now(timezone.utc) + timedelta(hours=1)
        },
        secret_key,
        algorithm="HS256"
    )

    return {
        "message": "Login successful",
        "token": token,
        "user": {
            "id": user[0],
            "name": user[1],
            "email": user[2],
            "role": user[4]
        }
    }, 200