from fastapi import (
    Depends,
    Form,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy import select

from auth import utils as auth_utils
from database.database import UserOrm
from database.database import new_session
from chemas.SUser import SUser

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
                        return SUser(**user.__dict__)
                    else:
                        raise HTTPException(
                            status_code=status.HTTP_403_FORBIDDEN,
                            detail="user inactive",
                        )
        raise unauthed_exc

    @staticmethod
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

    @staticmethod
    async def get_current_auth_user(payload: dict = Depends(get_current_token_payload)) -> SUser:
        payload_data = await payload
        username: str | None = payload_data.get("username")
        if username is not None:
            async with new_session() as session:
                query = select(UserOrm).where(UserOrm.username == username)
                result = await session.execute(query)
                user = result.scalar()
                if user:
                    return user
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalid or user not found",
        )

    @classmethod
    async def get_current_active_auth_user(cls, user: SUser = Depends(get_current_auth_user)):
        user_object = await user
        if user_object.is_active:
            return user_object
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )
