from datetime import datetime
from sqlalchemy import update, select
from sqlalchemy.orm import Session

from api.chemas.SCompleteTraining import SCompleteTraining
from api.database.database import new_session, CompleteTrainingOrm, UserOrm


class CompleteTrainingsRepository:

    @classmethod
    async def add_start_time(cls, start_time: datetime, training_id: int, user_id: int):
        async with new_session() as session:
            completed_training = CompleteTrainingOrm(time_start=start_time, time_end=None, user_id=user_id,
                                                     training_id=training_id)
            session.add(completed_training)
            await session.commit()

            await cls._update_user_training_start_flag(session, user_id, True)

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

            await cls._update_user_training_start_flag(session, user_id, False)

    @classmethod
    async def get_all_completed_trainings(cls) -> list[SCompleteTraining]:
        async with new_session() as session:
            query = select(CompleteTrainingOrm)
            result = await session.execute(query)
            models = result.scalars().all()
            return models

    @classmethod
    async def _update_user_training_start_flag(cls, session: Session, user_id: int, flag_value: bool):
        user_model = select(UserOrm).where(UserOrm.id == user_id)
        result = await session.execute(user_model)
        user = result.scalars().first()
        if user:
            user.training_start_flag = flag_value
            session.add(user)
            await session.commit()
