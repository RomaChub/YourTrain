from database.database import new_session, ExerciseOrm

from sqlalchemy import select, delete

from schemas import SExersiceAdd, SExercise


class ExerciseRepository:
    @classmethod
    async def add_one(cls, data: SExersiceAdd) -> int:
        async with new_session() as session:
            exercise_dict = data.model_dump()

            exercise = ExerciseOrm(**exercise_dict)
            session.add(exercise)
            await session.flush()
            await session.commit()
            return exercise.id

    @classmethod
    async def get_all(cls) -> list[SExercise]:
        async with new_session() as session:
            quety = select(ExerciseOrm)
            result = await session.execute(quety)
            exercise_models = result.scalars().all()
            exercise_schemas = [SExercise.model_validate(exercise_model) for exercise_model in exercise_models]
            return exercise_schemas

    @classmethod
    async def get_one(cls, exercise_id: int) -> SExercise:
        async with new_session() as session:
            quety = select(ExerciseOrm).where(ExerciseOrm.id == exercise_id)
            result = await session.execute(quety)
            exercise_model = result.scalars().all()
            return exercise_model

    @classmethod
    async def delete_exercise(cls, exercise_id: int):
        async with new_session() as session:
            query = delete(ExerciseOrm).where(ExerciseOrm.id == exercise_id)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def update_exercise(cls, exercise_id: int, name: str, description: str):
        async with new_session() as session:
            exercise = await session.get(ExerciseOrm, exercise_id)
            if not exercise:
                return False

            exercise.name = name
            exercise.description = description
            session.add(exercise)
            await session.commit()
            return True

