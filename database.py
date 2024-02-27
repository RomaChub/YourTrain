from typing import Optional

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_async_engine(
    "sqlite+aiosqlite:///exercises.db"
)
new_session = async_sessionmaker(engine, expire_on_commit=False)

engine_Training = create_async_engine(
    "sqlite+aiosqlite:///training.db"
)
new_session_training = async_sessionmaker(engine_Training, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class ExerciseOrm(Model):
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]


class TrainingOrm(Model):
    __tablename__ = "training"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    exercises: Mapped[int]


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)


async def create_tables_training():
    async with engine_Training.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables_training():
    async with engine_Training.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
