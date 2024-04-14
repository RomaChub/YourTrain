from typing import Annotated

from fastapi import APIRouter, Depends

from repositories.user_repository import UserRepository
from chemas.SUser import SUserAdd, SUserId, SUser, SUserW

router = APIRouter(
    prefix="/your_train",
    tags=['User']
)


@router.post("/user")
async def add_user(
        user: Annotated[SUserAdd, Depends()],
) -> SUserId:
    user_id = await UserRepository.add_user(user)
    return {"user_id": user_id}


@router.get("/user")
async def get_users() -> list[SUserW]:
    users = await UserRepository.get_all()
    return users
