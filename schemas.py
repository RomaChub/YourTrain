from typing import Optional

from pydantic import BaseModel, ConfigDict


class SExersiceAdd(BaseModel):
    name: str
    description: Optional[str] = None
    user_id: int
    training_id: int


class SUserAdd(BaseModel):
    username: str
    hashed_password: str


class STrainingAdd(BaseModel):
    name: str
    user_id: int


class SExercise(SExersiceAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class SUser(SUserAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class STraining(STrainingAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class SExerciseId(BaseModel):
    exercise_id: int


class STrainingId(BaseModel):
    training_id: int


class SUserId(BaseModel):
    user_id: int
