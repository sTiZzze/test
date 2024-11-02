from datetime import datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

from config.config import settings
from config.database import get_db
from src.domain.models.user import User
from src.domain.DTO.user import TokenPayload
from src.applications.user import UserService

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="api/v1/login",
    scheme_name="JWT"
)


async def get_current_user(token: str = Depends(reuseable_oauth)):
    async with get_db() as session:
        service = UserService(session)
    try:
        payload = jwt.decode(
            token, settings.jwt.JWT_PRIVATE_KEY, algorithms=[
                settings.jwt.JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await service.get_user(User, int(token_data.sub))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    return user[0]