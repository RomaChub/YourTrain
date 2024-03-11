from sqlalchemy import Column, Integer, String, Boolean, Table, MetaData, ForeignKey, BigInteger


metadata = MetaData()

UserOrm = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("is_active", Boolean, default=True),
)

TrainingOrm = Table(
    "training",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE")),
)


ExerciseOrm = Table(
    "exercises",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("description", String, nullable=True),
    Column("training_id", Integer, ForeignKey("training.id", ondelete="CASCADE", onupdate="CASCADE")),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE")),
)
