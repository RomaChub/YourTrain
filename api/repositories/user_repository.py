from api.auth.utils import hash_password
from api.database.database import new_session, UserOrm
from sqlalchemy import select
from api.chemas.SUser import SUserAdd, SUser, SUserW

class UserRepository:
    @classmethod
    async def add_user(cls, data: SUserAdd) -> int:
        data.hashed_password = await hash_password(data.hashed_password)
        async with new_session() as session:
            user_dict = data.model_dump()
            user = UserOrm(**user_dict)
            session.add(user)
            await session.flush()
            await session.commit()
            return user.id

    @classmethod
    async def get_all(cls) -> list[SUserW]:
        async with new_session() as session:
            query = select(UserOrm)
            result = await session.execute(query)
            user_models = result.scalars().all()
            user_schemas = [SUserW.model_validate(user_model) for user_model in user_models]
            return user_schemas

    @classmethod
    async def get_one(cls, user_id: int) -> SUser:
        async with new_session() as session:
            query = select(UserOrm).where(UserOrm.id == user_id)
            result = await session.execute(query)
            user_model = result.scalars().first()
            return user_model
