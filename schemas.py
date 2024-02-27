from typing import Optional

from pydantic import BaseModel, ConfigDict


class SExersiceAdd(BaseModel):
    name: str
    description: Optional[str] = None


class STrainingAdd(BaseModel):
    name: str
    exercises: int


class SExercise(SExersiceAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class STraining(STrainingAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class SExerciseId(BaseModel):
    exercise_id: int


class STrainingId(BaseModel):
    training_id:int