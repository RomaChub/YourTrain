from database.database import new_session, ConnectionExerciseWithTrainingOrm
from sqlalchemy import select
from typing import List
from chemas.SPairExerciseTraining import SPairExerciseTraining


class ExerciseToTraining:
    @classmethod
    async def add_one(cls, exercise_id: int, training_id: int, user_id: int) -> int:
        async with new_session() as session:
            exercise_pair = ConnectionExerciseWithTrainingOrm(exercise_id=exercise_id, training_id=training_id,
                                                              user_id=user_id)
            session.add(exercise_pair)
            await session.flush()
            await session.commit()
            return exercise_pair.id

    @classmethod
    async def get_all(cls) -> List[SPairExerciseTraining]:
        async with new_session() as session:
            query = select(ConnectionExerciseWithTrainingOrm)
            result = await session.execute(query)
            pair_models = result.fetchall()
            pair_schemas = [SPairExerciseTraining.model_validate(pair_model) for pair_model in pair_models]
            return pair_schemas
