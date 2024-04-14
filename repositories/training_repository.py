from chemas.SExercise import SExerciseId
from database.database import new_session, TrainingOrm, ConnectionExerciseWithTrainingOrm, ExerciseOrm

from sqlalchemy import select, delete

from chemas.STraining import STrainingAdd, STraining, STrainingId, SFullTraining


class TrainingRepository:
    @classmethod
    async def add_training(cls, data: STrainingAdd, user_id: int) -> STrainingId:
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
            return training_model.pop()

    @classmethod
    async def get_training(cls, training_id: int) -> SFullTraining:
        async with new_session() as session:
            training_query = select(TrainingOrm).where(TrainingOrm.id == training_id)
            training_result = await session.execute(training_query)
            training = training_result.scalars().first()

            if not training:
                return None

            pairs_query = select(ConnectionExerciseWithTrainingOrm).where(
                ConnectionExerciseWithTrainingOrm.training_id == training_id)
            pairs_result = await session.execute(pairs_query)
            pairs_models = pairs_result.scalars().all()

            exercises_ids = [pair.exercise_id for pair in pairs_models]

            exercises_query = select(ExerciseOrm).where(ExerciseOrm.id.in_(exercises_ids))
            exercises_result = await session.execute(exercises_query)
            all_exercises = exercises_result.scalars().all()

            training_schema = SFullTraining.model_validate(training)
            training_schema.all_exercises_id = exercises_ids
            training_schema.all_exercises = all_exercises
            return training_schema

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
