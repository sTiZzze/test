import asyncio
import json

from fastapi import APIRouter, Depends
from fastapi_cache import FastAPICache
from starlette import status

from config.database import get_db
from consumer import consume_messages
from src.applications.bet import BetService
from src.domain.DTO.bet import BetCreate
from src.domain.models.bet import Bet
from src.domain.models.user import User
from src.infrastructure.utils.deps import get_current_user

router_bet = APIRouter()

@router_bet.on_event("startup")
async def startup_event():
    asyncio.create_task(consume_messages())


@router_bet.get("/get_events/")
async def get_events():
    redis = FastAPICache.get_backend().redis

    keys = await redis.keys("cache:message_*")
    cached_messages = []

    for key in keys:
        message = await redis.get(key)
        if message:
            message_data = json.loads(message)

            if message_data.get("status") == "незавершённое":
                cached_messages.append(message_data)

    return {"cached_messages": cached_messages}

@router_bet.get('/bets')
async def get_bets(user: User = Depends(get_current_user)):
    async with get_db() as session:
        service = BetService(session)
    return await service.get_bet(Bet, user)


@router_bet.post('/bet', status_code=status.HTTP_201_CREATED)
async def create_bet(task: BetCreate, user: dict = Depends(get_current_user)):
    async with get_db() as session:
        service = BetService(session)
    return await service.create_bet(Bet, task, user)
