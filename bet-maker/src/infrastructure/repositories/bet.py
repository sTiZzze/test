from typing import Iterable

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.domain.DTO.bet import BetCreate
from src.domain.models.bet import Bet
from src.domain.models.user import User


class BetRepository:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def get_all(self, entity: Bet, user: User) -> Iterable[Bet]:
        query = await self.__session.execute(select(entity).filter(entity.user_id == user.id))
        return query.scalars().all()


    async def create(self, entity: Bet, model: BetCreate, user: User) -> Bet:
        model.user_id = user.id

        new_task = entity(**model.model_dump())
        self.__session.add(new_task)
        await self.__session.commit()
        await self.__session.refresh(new_task)
        return new_task

    async def change_bet_status(self, event_id: str, status: str) -> None:
        result = await self.__session.execute(select(Bet).where(Bet.event_id == event_id))
        bets_to_update = result.scalars().all()

        for bet in bets_to_update:
            bet.status = status

        await self.__session.commit()
