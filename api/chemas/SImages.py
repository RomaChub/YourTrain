from pydantic import BaseModel, ConfigDict


class SImageAdd(BaseModel):
    image_path: str
    user_id: int
    tag: str


class SImage(SImageAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)
