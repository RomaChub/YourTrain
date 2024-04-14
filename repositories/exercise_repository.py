import json

from database.database import new_session, ExerciseOrm

from sqlalchemy import select, delete

from chemas.SExercise import SExerciseAdd, SExercise


class ExerciseRepository:
    @classmethod
    async def add_one(cls, data: SExerciseAdd, user_id: int) -> int:
        data.user_id = user_id
        async with new_session() as session:
            exercise_dict = data.model_dump()

            exercise = ExerciseOrm(**exercise_dict)
            session.add(exercise)
            await session.flush()
            await session.commit()
            return exercise.id

    @classmethod
    async def get_all(cls) -> list:
        async with new_session() as session:
            query = select(ExerciseOrm)
            result = await session.execute(query)
            exercise_models = result.scalars().all()
            exercise_schemas = [SExercise.model_validate(exercise_model) for exercise_model in exercise_models]
            return exercise_schemas

    @classmethod
    async def get_one(cls, exercise_id: int) -> SExercise:
        async with new_session() as session:
            query = select(ExerciseOrm).where(ExerciseOrm.id == exercise_id)
            result = await session.execute(query)
            exercise_model = result.scalars().first()
            return exercise_model

    @classmethod
    async def delete_exercise(cls, exercise_id: int):
        async with new_session() as session:
            query = delete(ExerciseOrm).where(ExerciseOrm.id == exercise_id)
            await session.execute(query)
            await session.flush()
            await session.commit()

    @classmethod
    async def update_exercise(cls, ex_id: int, ex: SExerciseAdd):
        async with new_session() as session:
            exercise = await session.get(ExerciseOrm, ex_id)
            if not exercise:
                return False
            exercise.name = ex.name
            exercise.description = ex.description
            exercise.img = ex.img
            exercise.params = ex.params
            await session.commit()
            return True
