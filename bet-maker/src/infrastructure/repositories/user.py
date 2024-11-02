from typing import Optional

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.domain.models.user import User
from src.domain.DTO.user import CreateUser
from src.infrastructure.utils.utils import JWTAuthUtils


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def create(self, entity: User, data: CreateUser) -> User:
        user_query = await self.__session.execute(select(entity).filter(entity.username == data.username))
        user = user_query.scalars().all()
        if user:
            raise HTTPException(
                status_code=404, detail="Username is already taken.")
        data.password = JWTAuthUtils.get_hashed_password(data.password)
        new_user = User(**data.model_dump())
        self.__session.add(new_user)
        await self.__session.commit()
        await self.__session.refresh(new_user)
        return new_user

    async def get_user(self, entity: User, form_data: OAuth2PasswordRequestForm) -> Optional[User]:
        query = await self.__session.execute(select(entity).filter(entity.username == form_data.username))
        return query.scalars().first()

    async def get_user_by_id(self, entity: User, user_id: int) -> Optional[User]:
        query = await self.__session.execute(select(entity).filter(entity.id == user_id))
        return query.first()
