from typing import Optional

from pydantic import BaseModel, ConfigDict

from chemas.SExercise import SExercise


class STrainingAdd(BaseModel):
    name: str
    description: Optional[str] = None
    user_id: Optional[int] = None


class STraining(STrainingAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class STrainingId(BaseModel):
    id: int


class SFullTraining(STraining):
    all_exercises_id: Optional[list[int]] = None
    all_exercises: Optional[list[SExercise]] = None
