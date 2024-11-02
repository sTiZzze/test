from sqlalchemy import Integer, String, Float, DECIMAL, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.models.abstract_models import AbstractModel


class User(AbstractModel):
    __tablename__ = "users"
    __mapper_args__ = {"concrete": True}
    __table_args__ = (
        {"postgresql_inherits": AbstractModel.__table__.name}
    )

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    balance: Mapped[float] = mapped_column(
        DECIMAL(precision=10, scale=2),
        default=0,
    )