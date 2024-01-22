from __future__ import annotations
import datetime
from contextlib import contextmanager
from sqlalchemy import String, create_engine, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    DeclarativeBase,
    sessionmaker,
    relationship,
)

from data import modules


engine = create_engine(
    url="sqlite:///db.sqlite",
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
)

Session = sessionmaker(bind=engine)


@contextmanager
def get_session() -> Session:
    """Get session"""
    new_session = Session()
    try:
        yield new_session
    finally:
        new_session.close()


class BaseTable(DeclarativeBase):
    pass


class WaUser(BaseTable):
    """Whatsapp user details"""

    __tablename__ = "wa_user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    wa_id: Mapped[str] = mapped_column(String(15), unique=True)
    admin: Mapped[bool] = mapped_column(default=False)
    name: Mapped[str] = mapped_column(String(20))
    is_pay: Mapped[bool]
    in_program: Mapped[bool]
    created_at: Mapped[datetime.datetime]
    events: Mapped[list[Event]] = relationship(back_populates="by_wa_user")


class Event(BaseTable):
    """Event info"""

    __tablename__ = "event"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[modules.EventType]
    date: Mapped[datetime.date]

    by_wa_user_id: Mapped[int | None] = mapped_column(ForeignKey("wa_user.id"))
    by_wa_user: Mapped[WaUser | None] = relationship(back_populates="events")

    added_by_admin: Mapped[str] = mapped_column(String(20))


BaseTable.metadata.create_all(engine)
