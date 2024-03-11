from typing import Annotated

from fastapi import APIRouter, Depends


from repositories.user_repository import UserRepository
from schemas import SUserAdd, SUserId, SUser

router = APIRouter(
    prefix="/YourTrain"
)


@router.post("/user")
async def add_user(
        user: Annotated[SUserAdd, Depends()],
) -> SUserId:
    user_id = await UserRepository.add_user(user)
    return {"user_id": user_id}

@router.get("/user")
async def get_users() -> list[SUser]:
    users = await UserRepository.get_all()
    return users
