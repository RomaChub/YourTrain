from database.database import new_session, UserOrm

from sqlalchemy import select

from chemas.schemas import SUserAdd, SUser


class UserRepository:
    @classmethod
    async def add_user(cls, data: SUserAdd) -> int:
        async with new_session() as session:
            user_dict = data.model_dump()

            user = UserOrm(**user_dict)
            session.add(user)
            await session.flush()
            await session.commit()
            return user.id

    @classmethod
    async def get_all(cls) -> list[SUser]:
        async with new_session() as session:
            quety = select(UserOrm)
            result = await session.execute(quety)
            user_models = result.scalars().all()
            user_schemas = [SUser.model_validate(user_model) for user_model in user_models]
            return user_schemas

    @classmethod
    async def get_one(cls, user_id: int) -> SUser:
        async with new_session() as session:
            quety = select(UserOrm).where(UserOrm.id == user_id)
            result = await session.execute(quety)
            user_model = result.scalars().all()
            return user_model
