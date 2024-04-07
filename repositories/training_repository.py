from database.database import new_session, TrainingOrm

from sqlalchemy import select, delete

from chemas.STraining import STrainingAdd, STraining


class TrainingRepository:
    @classmethod
    async def add_training(cls, data: STrainingAdd, user_id: int) -> int:
        data.user_id = user_id
        async with new_session() as session:
            training_dict = data.model_dump()

            training = TrainingOrm(**training_dict)
            session.add(training)
            await session.flush()
            await session.commit()
            return training.id

    @classmethod
    async def get_all(cls) -> list[STraining]:
        async with new_session() as session:
            quety = select(TrainingOrm)
            result = await session.execute(quety)
            training_models = result.scalars().all()
            training_schemas = [STraining.model_validate(training_model) for training_model in training_models]
            return training_schemas

    @classmethod
    async def get_one(cls, training_id: int) -> STraining:
        async with new_session() as session:
            quety = select(TrainingOrm).where(TrainingOrm.id == training_id)
            result = await session.execute(quety)
            training_model = result.scalars().all()
            return training_model

    @classmethod
    async def update_training(cls, training_id: int, name: STrainingAdd):
        async with new_session() as session:
            training = await session.get(TrainingOrm, training_id)
            if not training:
                return False

            training.name = name.name
            training.description = name.description
            session.add(training)
            await session.commit()
            return True

    @classmethod
    async def delete_training(cls, training_id: int):
        async with new_session() as session:
            query = delete(TrainingOrm).where(TrainingOrm.id == training_id)
            await session.execute(query)
            await session.commit()
