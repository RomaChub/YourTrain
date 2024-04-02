from fastapi import (
    APIRouter,
    Depends,
)
from pydantic import BaseModel

from auth import utils as auth_utils
from auth.auth_repository import AuthRepository
from chemas import SUser


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


router = APIRouter(prefix="/jwt", tags=["JWT"])


@router.post("/login", response_model=TokenInfo)
def auth_user_issue_jwt(
        user: SUser = Depends(AuthRepository.validate_auth_user),
):
    jwt_payload = {
        # subject
        "sub": user.username,
        "username": user.username,
    }
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )


@router.get("/user/me")
async def auth_user_check_self_info(
        payload: dict = Depends(AuthRepository.get_current_token_payload),
        user: SUser = Depends(AuthRepository.get_current_active_auth_user),
):
    iat = payload.get("iat")
    return {
        "username": user.username,
        "logged_in_at": iat,
    }
