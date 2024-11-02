from fastapi import HTTPException, status

from src.infrastructure.repositories.user import UserRepository
from src.infrastructure.utils.utils import JWTAuthUtils


class UserService:
    def __init__(self, session):
        self.__session = UserRepository(session)

    async def create_user(self, entity, data):
        return await self.__session.create(entity, data)

    async def login_user(self, entity, form_data):
        user = await self.__session.get_user(entity, form_data)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect username or password"
            )
        hashed_pass = user.password

        if not JWTAuthUtils.verify_password(form_data.password, hashed_pass):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect password"
            )
        return {
            "access_token": JWTAuthUtils.create_access_token(user.id),
            "refresh_token": JWTAuthUtils.create_refresh_token(user.id),
        }

    async def get_user(self, entity, user_id):
        return await self.__session.get_user_by_id(entity, user_id)