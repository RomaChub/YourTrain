from pydantic import BaseModel, ConfigDict


class CreateUser(BaseModel):
    username: str


class UserSchema(CreateUser):
    model_config = ConfigDict(strict=True)
    hashed_password: str
    is_active: bool
