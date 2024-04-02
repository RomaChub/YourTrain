import json

from sqlalchemy import LargeBinary, Column, Integer, String, Boolean, Table, MetaData, ForeignKey, JSON

metadata = MetaData()

UserOrm = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, nullable=False, unique=True),
    Column("hashed_password", LargeBinary, nullable=False),
    Column("is_active", Boolean, default=True),
)

TrainingOrm = Table(
    "training",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("description", String, nullable=True),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE")),
)

params_data = {}
params_json = json.dumps(params_data)

ExerciseOrm = Table(
    "exercises",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("description", String, nullable=True),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE")),
    Column("params", JSON, default=params_json, nullable=True),
    Column("img", String, nullable=True),
)


ConnectionExerciseWithTrainingOrm = Table(
    "connection_exercise_with_training",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("training_id", Integer, ForeignKey("training.id", ondelete="CASCADE", onupdate="CASCADE")),
    Column("exercise_id", Integer, ForeignKey("exercises.id", ondelete="CASCADE", onupdate="CASCADE")),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"))
)
