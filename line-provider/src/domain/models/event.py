from enum import Enum
from datetime import datetime
from pydantic import BaseModel, condecimal


class EventStatus(str, Enum):
    ongoing = "незавершённое"
    team1_win = "завершено выигрышем первой команды"
    team2_win = "завершено выигрышем второй команды"


class Event(BaseModel):
    id: str
    odds: condecimal(gt=0, max_digits=4, decimal_places=2)
    deadline: datetime
    status: EventStatus = EventStatus.ongoing
