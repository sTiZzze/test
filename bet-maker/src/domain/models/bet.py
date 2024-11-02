import uuid
from enum import Enum

from pydantic import ConfigDict
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import ForeignKey, Integer, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from src.domain.addition.enum import ResultEnum, Result
from src.domain.models.abstract_models import AbstractModel
from src.domain.models.user import User

class EventStatus(str, Enum):
    ongoing = "незавершённое"
    team1_win = "завершено выигрышем первой команды"
    team2_win = "завершено выигрышем второй команды"

class Bet(AbstractModel):
    __tablename__ = 'bet'
    __mapper_args__ = {"concrete": True}
    __table_args__ = (
        {"postgresql_inherits": AbstractModel.__table__.name}
    )
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True)
    bet: Mapped[float] = mapped_column(
        DECIMAL(precision=10, scale=2),
        default=0,
    )
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    user: Mapped["User"] = relationship()
    event_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), default=uuid.uuid4, nullable=False
    )
    status: Mapped[EventStatus] = mapped_column(
        SQLAlchemyEnum(EventStatus),
        default=EventStatus.ongoing,
        nullable=False
    )