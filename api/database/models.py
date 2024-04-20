import json

from sqlalchemy import LargeBinary, Column, Integer, String, Boolean, Table, MetaData, ForeignKey, JSON, TIMESTAMP

metadata = MetaData()

UserOrm = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, nullable=False, unique=True),
    Column("hashed_password", LargeBinary, nullable=False),
    Column("is_active", Boolean, default=True),
    Column("training_start_flag", Boolean, default=False),
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
)


ConnectionExerciseWithTrainingOrm = Table(
    "connection_exercise_with_training",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("training_id", Integer, ForeignKey("training.id", ondelete="CASCADE", onupdate="CASCADE")),
    Column("exercise_id", Integer, ForeignKey("exercises.id", ondelete="CASCADE", onupdate="CASCADE")),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"))
)

CompleteTrainingOrm = Table(
    "complete_trainings",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("training_id", Integer, ForeignKey("training.id", ondelete="CASCADE", onupdate="CASCADE")),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE")),
    Column("time_start", TIMESTAMP, default=False),
    Column("time_end", TIMESTAMP, default=False)
)

ImageOrm = Table(
    "images",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("image_path", String, nullable=False),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE")),
    Column("tag", String, nullable=True)
)
