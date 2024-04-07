from typing import Optional

from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSON
from config import DB_PORT, DB_USER, DB_PASS, DB_HOST, DB_NAME

engine = create_async_engine(
    f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class ExerciseOrm(Model):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String, nullable=True)
    user_id = Column(Integer)
    params = Column(JSON)
    img = Column(String)


class CompleteTrainingOrm(Model):
    __tablename__ = "complete_trainings"
    
    id = Column(Integer, primary_key=True)
    training_id = Column(Integer)
    user_id = Column(Integer)
    time_start = Column(TIMESTAMP, nullable=True)
    time_end = Column(TIMESTAMP, nullable=True)


class TrainingOrm(Model):
    __tablename__ = "training"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    user_id: Mapped[int]


class UserOrm(Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    username: Mapped[str]
    hashed_password: Mapped[bytes]
    is_active: Mapped[bool]
    training_start_flag: Mapped[Optional[bool]]


class ConnectionExerciseWithTrainingOrm(Model):
    __tablename__ = "connection_exercise_with_training"

    id: Mapped[int] = mapped_column(primary_key=True)
    training_id: Mapped[int]
    exercise_id: Mapped[int]
    user_id: Mapped[int]


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
