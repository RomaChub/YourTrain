from sqlalchemy import Column, Integer, String, Boolean, Table, MetaData, ForeignKey

metadata = MetaData()

UserOrm = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, nullable=False, unique=True),
    Column("hashed_password", String, nullable=False),
    Column("is_active", Boolean, default=True),
)

TrainingOrm = Table(
    "training",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("description", String, nullable=True),
    Column("username", String, ForeignKey("users.username", ondelete="CASCADE", onupdate="CASCADE")),
)


ExerciseOrm = Table(
    "exercises",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("description", String, nullable=True),
    Column("username", String, ForeignKey("users.username", ondelete="CASCADE", onupdate="CASCADE")),
)


ConnectionExerciseWithTrainingOrm = Table(
    "connection_exercise_with_training",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("training_id", Integer, ForeignKey("training.id", ondelete="CASCADE", onupdate="CASCADE")),
    Column("exercise_id", Integer, ForeignKey("exercises.id", ondelete="CASCADE", onupdate="CASCADE")),
)
