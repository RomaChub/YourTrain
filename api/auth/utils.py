from datetime import datetime, timedelta
import bcrypt
import jwt
from api.auth.core.config import settings


def encode_jwt(payload: dict, expire_timedelta: timedelta | None = None) -> str:
    """
    Encode JWT token with payload
    """
    private_key = settings.auth_jwt.private_key_path.read_text()
    algorithm = settings.auth_jwt.algorithm
    expire_minutes = settings.auth_jwt.access_token_expire_minutes

    to_encode = payload.copy()
    now = datetime.utcnow()
    expire = now + (expire_timedelta or timedelta(minutes=expire_minutes))
    to_encode.update(exp=expire, iat=now)

    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(token: str | bytes) -> dict:
    """
    Decode JWT token
    """
    public_key = settings.auth_jwt.public_key_path.read_text()
    algorithm = settings.auth_jwt.algorithm

    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def hash_password(password: str) -> bytes:
    """
    Hash password
    """
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    """
    Validate password
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
