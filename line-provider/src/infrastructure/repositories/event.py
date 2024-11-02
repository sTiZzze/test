from typing import Dict, Optional
from uuid import uuid4

from src.domain.DTO.event_schema import EventCreate
from src.domain.models.event import Event, EventStatus

events: Dict[str, Event] = {}

def create_event(event_data: EventCreate) -> Event:
    event_id = str(uuid4())
    new_event = Event(id=event_id, odds=event_data.odds, deadline=event_data.deadline)
    events[event_id] = new_event
    return new_event

def get_event(event_id: str) -> Optional[Event]:
    return events.get(event_id)

def update_event_status(event_id: str, status: EventStatus) -> Optional[Event]:
    event = events.get(event_id)
    if event:
        event.status = status
    return event

def list_events() -> Dict[str, Event]:
    return events
