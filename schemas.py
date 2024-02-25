from typing import Optional

from pydantic import BaseModel


class SExersiceAdd(BaseModel):
    name: str
    description: Optional[str] = None


class SExercise(SExersiceAdd):
    id: int


class SExerciseId(BaseModel):
    ok: bool = True
    exercise_id: int
