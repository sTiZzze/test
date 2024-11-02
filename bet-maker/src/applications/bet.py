from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_db
from src.infrastructure.repositories.bet import BetRepository


class BetService:
    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.__session = BetRepository(session)

    async def get_bet(self, entity, user):
        return await self.__session.get_all(entity, user)

    async def create_bet(self, entity, model, user):
        return await self.__session.create(entity, model, user)

    async def change_bet_status(self, event_id, status):
        return await self.__session.change_bet_status(event_id, status)
