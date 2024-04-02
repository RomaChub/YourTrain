from pydantic import BaseModel, ConfigDict


class SUserAdd(BaseModel):
    username: str
    hashed_password: str
    is_active: bool


class SUser(SUserAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class SUserW(BaseModel):
    id: int
    username: str
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


class SUserId(BaseModel):
    user_id: int
