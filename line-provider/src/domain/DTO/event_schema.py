from pydantic import BaseModel, condecimal
from datetime import datetime
from src.domain.models.event import EventStatus


class EventCreate(BaseModel):
    odds: condecimal(gt=0, max_digits=4, decimal_places=2)
    deadline: datetime


class EventUpdateStatus(BaseModel):
    status: EventStatus