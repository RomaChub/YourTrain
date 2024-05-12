from typing import Optional, Dict, Any

from pydantic import BaseModel, ConfigDict


class SExerciseAdd(BaseModel):
    name: str
    description: Optional[str] = None
    user_id: Optional[int] = None
    params: Optional[Dict[str, Any]] = None


class SExercise(SExerciseAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class SExerciseId(BaseModel):
    id: int
