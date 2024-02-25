from database import new_session, ExerciseOrm

from sqlalchemy import select

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
            exercise_schemas =[SExercise.model_validate(exercise_models) for exercise_model in exercise_models]
            return exercise_models
