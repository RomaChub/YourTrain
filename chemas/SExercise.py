from typing import Optional, Dict, Text, Any

from pydantic import BaseModel, ConfigDict


class SExersiceAdd(BaseModel):
    name: str
    description: Optional[str] = None
    user_id: Optional[int] = None
    img: Optional[str] = None
    params: Optional[Dict[str, Any]] = None


class SExercise(SExersiceAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class SExerciseId(BaseModel):
    id: int
