from typing import Optional

from pydantic import BaseModel, ConfigDict


class SExersiceAdd(BaseModel):
    name: str
    description: Optional[str] = None


class SExercise(SExersiceAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class SExerciseId(BaseModel):
    ok: bool = True
    exercise_id: int
