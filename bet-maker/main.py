import asyncio

import httpx
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis.asyncio import Redis

from config.config import settings
from consumer import consume_messages
from src.interfaces.auth import router_auth
from src.interfaces.bet import router_bet

app = FastAPI()

@app.on_event("startup")
async def startup():
    redis = await Redis.from_url(settings.redis.REDIS_URL)
    FastAPICache.init(RedisBackend(redis), prefix="cache")


# async def fetch_data():
#     async with httpx.AsyncClient() as client:
#         response = await client.get("http://line-provider:8001/api/v1/events")
#         if response.status_code == 200:
#             return response.json()
#         else:
#             return {"error": "Failed to fetch data", "status_code": response.status_code}
#
# @app.get("/get-events/")
# async def get_events():
#     data = await fetch_data()  # Вызов функции для получения данных
#     return data

app.include_router(router_auth, prefix="/api/v1", tags=["users"])
app.include_router(router_bet, prefix="/api/v1", tags=["bet"])

