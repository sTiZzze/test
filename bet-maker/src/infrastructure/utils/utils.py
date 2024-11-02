from datetime import datetime, timedelta
from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext

from config.config import settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JWTAuthUtils:
    @staticmethod
    def get_hashed_password(password: str) -> str:
        return password_context.hash(password)

    @staticmethod
    def verify_password(password: str, hashed_pass: str) -> bool:
        return password_context.verify(password, hashed_pass)

    @staticmethod
    def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow(
            ) + timedelta(minutes=settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(
            to_encode, settings.jwt.JWT_PRIVATE_KEY, settings.jwt.JWT_ALGORITHM)
        return encoded_jwt

    @staticmethod
    def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow(
            ) + timedelta(minutes=settings.jwt.REFRESH_TOKEN_EXPIRES_IN)

        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(
            to_encode, settings.jwt.JWT_PUBLIC_KEY, settings.jwt.JWT_ALGORITHM)
        return encoded_jwt