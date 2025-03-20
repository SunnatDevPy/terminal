import datetime
from enum import Enum

from sqlalchemy import ForeignKey, BIGINT
from sqlalchemy import String
from sqlalchemy import func, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from models.database import BaseModel


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


class BankName(BaseModel):
    name: Mapped[str]


class GroupFromBank(BaseModel):
    bank_name: Mapped[str]
    group_id: Mapped[int] = mapped_column(BIGINT)
    bank_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("bank_names.id", ondelete='CASCADE'))


class Check(BaseModel):
    device: Mapped[str]
    district: Mapped[str]
    district_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("districts.id", ondelete='CASCADE'))
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), server_onupdate=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class Tickets(BaseModel):
    text: Mapped[str]
    check: Mapped[str]
    district: Mapped[str]
    district_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("districts.id", ondelete='CASCADE'))
    check_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("checks.id", ondelete='CASCADE'))
    group_id: Mapped[int] = mapped_column(BIGINT)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), server_onupdate=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
