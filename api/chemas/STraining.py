from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from api.chemas.SExercise import SExercise


class STrainingAdd(BaseModel):
    name: str
    description: Optional[str] = Field('Some description about the training')
    user_id: Optional[int] = None


class STraining(STrainingAdd):
    id: int = Field('id')

    model_config = ConfigDict(from_attributes=True)


class STrainingId(BaseModel):
    id: int = Field('Training Id')


class SFullTraining(STraining):
    all_exercises_id: Optional[list[int]] = None
    all_exercises: Optional[list[SExercise]] = None
