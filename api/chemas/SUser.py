from pydantic import BaseModel, ConfigDict, Field


class SUserAdd(BaseModel):
    username: str
    hashed_password: str = Field('your_password')


class SUser(SUserAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class SUserW(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)


class SUserId(BaseModel):
    user_id: int
