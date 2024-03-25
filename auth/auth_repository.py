from jwt.exceptions import InvalidTokenError
from fastapi import (
    Depends,
    Form,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Mapped

from auth import utils as auth_utils
from auth.schemas import UserSchema
from database.database import new_session
from database.database import UserOrm

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/jwt/login",
)


class AuthRepository:
    @classmethod
    async def validate_auth_user(cls,
                                 username: str = Form(),
                                 password: str = Form(),
                                 ):
        async with new_session() as session:
            quety = select(UserOrm).where(UserOrm.username == username)
            result = await session.execute(quety)
            users = result.scalars().all()
        unauthed_exc = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid username or password",
        )
        for user in users:
            if user.username == username:
                if auth_utils.validate_password(password=password, hashed_password=user.hashed_password):
                    if user.is_active:
                        return UserSchema(**user.__dict__)
                    else:
                        raise HTTPException(
                            status_code=status.HTTP_403_FORBIDDEN,
                            detail="user inactive",
                        )
        raise unauthed_exc

    async def get_current_token_payload(token: str = Depends(oauth2_scheme)) -> dict:
        try:
            payload = auth_utils.decode_jwt(
                token=token,
            )
        except InvalidTokenError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid token error",

            )
        return payload

    async def get_current_auth_user(payload: dict = Depends(get_current_token_payload)) -> UserSchema:
        username: str | None = payload.get("username")
        async with new_session() as session:
            quety = select(UserOrm).where(UserOrm.username == username)
            result = await session.execute(quety)
            user = result.scalars().all()
            for u in user:
                if username == u.username:
                    return u
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="token invalid",
                )

    @classmethod
    async def get_current_active_auth_user(cls, user: UserSchema = Depends(get_current_auth_user)):
        if user.is_active != 0:
            return user
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )
