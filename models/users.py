import datetime
from enum import Enum

from sqlalchemy import Boolean, Integer, select, desc, func, DateTime
from sqlalchemy import ForeignKey, BIGINT, BOOLEAN, Enum as SqlEnum
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy_file import ImageField

from models.database import BaseModel, db


class BotUser(BaseModel):
    class TypeUser(str, Enum):
        OPTOM = 'optom'
        RESTORATOR = 'restorator'
        ONE = "one"

    first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    username: Mapped[str] = mapped_column(String(255), nullable=True)

    def __str__(self):
        return super().__str__() + f" - {self.username}"


class District(BaseModel):
    name: Mapped[str]


class Check(BaseModel):
    text: Mapped[str]
    group_id: Mapped[int] = mapped_column(BIGINT)
    district: Mapped[str]
    district_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("districts.id", ondelete='CASCADE'))
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), server_onupdate=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class Tickets(BaseModel):
    text: Mapped[str]
    check: Mapped[str]
    district: Mapped[str]
    district_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("districts.id", ondelete='CASCADE'))
    check_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("ticketss.id", ondelete='CASCADE'))
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), server_onupdate=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
