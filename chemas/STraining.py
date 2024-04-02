from typing import Optional

from pydantic import BaseModel, ConfigDict


class STrainingAdd(BaseModel):
    name: str
    description: Optional[str] = None
    user_id: Optional[int] = None


class STraining(STrainingAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class STrainingId(BaseModel):
    id: int
