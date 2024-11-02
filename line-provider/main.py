from fastapi import FastAPI

from src.interfaces.event import router_event

app = FastAPI()

app.include_router(router_event, prefix="/api/v1", tags=["events"])