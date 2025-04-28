from sqlalchemy import Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from datetime import datetime
import pytz

import config as cfg

moscow_tz = pytz.timezone("Europe/Moscow")
engine = create_async_engine(url=cfg.SQLALCHEMY_DATABASE_URI, echo=True)
async_session = async_sessionmaker(engine)

def now_moscow():
    return datetime.now(moscow_tz).strftime("%d.%m.%Y %H:%M:%S")

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String)
    created_at: Mapped[str] = mapped_column(String, default=now_moscow)
    last_active: Mapped[str] = mapped_column(String, default=now_moscow, onupdate=now_moscow)
    notif_time: Mapped[str] = mapped_column(String, default="00:00")
    role: Mapped[str] = mapped_column(String, default="user")

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    assigned_to: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"), nullable=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, default="pending")
    priority: Mapped[str] = mapped_column(String, default="medium")
    due_date: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[str] = mapped_column(String, default=now_moscow)
    updated_at: Mapped[str] = mapped_column(String, default=now_moscow, onupdate=now_moscow)

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String, unique=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[str] = mapped_column(String, default=now_moscow)

class Log(Base):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    action: Mapped[str] = mapped_column(String)
    created_at: Mapped[str] = mapped_column(String, default=now_moscow)

class Reminder(Base):
    __tablename__ = "reminders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String)
    text: Mapped[str] = mapped_column(String)
    date: Mapped[str] = mapped_column(String)
    time: Mapped[str] = mapped_column(String)
    rules: Mapped[str] = mapped_column(String)
    sending_time: Mapped[str] = mapped_column(String, nullable=True, default=None)
    created_at: Mapped[str] = mapped_column(String, default=now_moscow)
    updated_at: Mapped[str] = mapped_column(String, default=now_moscow, onupdate=now_moscow)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        