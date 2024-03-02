from typing import Optional

from sqlalchemy import Column, Integer, String, Table, MetaData


metadata = MetaData()

ExerciseOrm = Table(
    "exercises",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("description", String),
)

TrainingOrm = Table(
    "training",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("exercises", String),
)


