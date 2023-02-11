# app/auth/auth_handler.py

import time
from typing import Dict

import jwt
from decouple import config


JWT_SECRET = config("AUTH_SECRET")
JWT_ALGORITHM = "HS256"


def token_response(token: str):
    return {
        "access_token": token
    }


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}

