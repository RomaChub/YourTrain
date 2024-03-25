from typing import Optional

from pydantic import BaseModel, ConfigDict


class SExersiceAdd(BaseModel):
    name: str
    description: Optional[str] = None
    username: Optional[str] = None


class SUserAdd(BaseModel):
    username: str
    hashed_password: str
    is_active: bool = True


class STrainingAdd(BaseModel):
    name: str
    description: Optional[str] = None
    username: Optional[str] = None


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


class SPairExerciseTrainingAdd(BaseModel):
    exercise_id: int
    training_id: int


class SPairExerciseTraining(SPairExerciseTrainingAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class SPairExerciseTrainingId(BaseModel):
    pair_id: int
