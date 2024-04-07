from database.database import new_session, ConnectionExerciseWithTrainingOrm

from sqlalchemy import select

from chemas.SPairExerciseTraining import SPairExerciseTraining


class ExerciseToTraining:
    @classmethod
    async def add_one(cls, exercise_id, training_id, user_id):
        async with new_session() as session:
            exercise_pair = ConnectionExerciseWithTrainingOrm(exercise_id=exercise_id, training_id=training_id, user_id=user_id)
            session.add(exercise_pair)
            await session.flush()
            await session.commit()
            return exercise_pair.id

    @classmethod
    async def get_all(cls) -> list:
        async with new_session() as session:
            quety = select(ConnectionExerciseWithTrainingOrm)
            result = await session.execute(quety)
            pair_models = result.scalars().all()
            pair_schemas = [SPairExerciseTraining.model_validate(pair_model) for pair_model in pair_models]
            return pair_schemas
