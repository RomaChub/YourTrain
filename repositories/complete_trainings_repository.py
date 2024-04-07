from datetime import datetime
from sqlite3 import Timestamp
from sqlalchemy import update
from sqlalchemy import select

from chemas.SCompleteTraining import SCompleteTraining
from database.database import new_session, CompleteTrainingOrm, UserOrm


class CompleteTrainingsRepository:

    @classmethod
    async def add_start_time(cls, start_time: datetime, training_id: int, user_id: int):
        async with new_session() as session:
            completed_training = CompleteTrainingOrm(time_start=start_time, time_end=None, user_id=user_id,
                                                     training_id=training_id)
            session.add(completed_training)
            await session.commit()
            user_model = select(UserOrm).where(UserOrm.id == user_id)
            result = await session.execute(user_model)
            user = result.scalars().all()
            user = user.pop(0)
            user.training_start_flag = True
            session.add(user)
            await session.flush()
            await session.commit()
            return completed_training.id

    @classmethod
    async def add_end_time(cls, end_time: datetime, user_id: int):
        async with new_session() as session:
            await session.execute(
                update(CompleteTrainingOrm)
                .where((CompleteTrainingOrm.time_end.is_(None)) & (CompleteTrainingOrm.user_id == user_id))
                .values(time_end=end_time)
            )
            await session.commit()
            user_model = select(UserOrm).where(UserOrm.id == user_id)
            result = await session.execute(user_model)
            user = result.scalars().all()
            user = user.pop(0)
            user.training_start_flag = False
            session.add(user)
            await session.flush()
            await session.commit()

    @classmethod
    async def get_all_completed_trainings(cls) -> list:
        async with new_session() as session:
            query = select(CompleteTrainingOrm)
            result = await session.execute(query)
            models = result.scalars().all()
            return models
