
import os
import jwt
from functools import wraps
from pathlib import Path
from flask import request, jsonify
from dotenv import load_dotenv

load_dotenv(
    Path(__file__).resolve().parent.parent / "services" / ".env",
    override=True
)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({
                "error": "Authentication token is required"
            }), 401

        token = auth_header.split(" ", 1)[1].strip()
        secret_key = os.getenv("JWT_SECRET_KEY")

        if not secret_key:
            return jsonify({
                "error": "JWT configuration missing"
            }), 500

        try:
            payload = jwt.decode(
                token,
                secret_key,
                algorithms=["HS256"]
            )

            request.current_user = {
                "id": payload["user_id"],
                "role": payload["role"]
            }

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401

        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        except (KeyError, TypeError):
            return jsonify({"error": "Invalid token payload"}), 401

        return f(*args, **kwargs)

    return decorated


def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            current_user = getattr(request, "current_user", None)

            if not current_user:
                return jsonify({
                    "error": "Authentication is required"
                }), 401

            if current_user["role"] != required_role:
                return jsonify({
                    "error": "You do not have permission to perform this action"
                }), 403

            return f(*args, **kwargs)

        return decorated

    return decorator