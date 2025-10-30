import base64
import hashlib
import os
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from app.core.settings import settings


def _pbkdf2(password: str, salt: bytes, iterations: int = 390000) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = _pbkdf2(password, salt)
    return base64.b64encode(salt + digest).decode("utf-8")


def verify_password(password: str, encoded: str) -> bool:
    try:
        decoded = base64.b64decode(encoded.encode("utf-8"))
    except Exception:
        return False
    salt, digest = decoded[:16], decoded[16:]
    candidate = _pbkdf2(password, salt)
    return hashlib.compare_digest(candidate, digest)


def create_access_token(
    subject: str,
    *,
    additional_claims: dict[str, Any] | None = None,
    expires_delta: timedelta | None = None,
) -> str:
    now = datetime.now(tz=timezone.utc)
    expire = now + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    payload: dict[str, Any] = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }
    if additional_claims:
        payload.update(additional_claims)
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token


def decode_access_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
