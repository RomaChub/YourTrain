from database import new_session, ExerciseOrm, new_session_training,TrainingOrm

from sqlalchemy import select, delete

from schemas import SExersiceAdd, SExercise, STrainingAdd, STraining


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


class TrainingRepository:
    @classmethod
    async def add_training(cls, data: STrainingAdd) -> int:
        async with new_session_training() as session:
            training_dict = data.model_dump()

            training = TrainingOrm(**training_dict)
            session.add(training)
            await session.flush()
            await session.commit()
            return training.id

    @classmethod
    async def get_all(cls) -> list[STraining]:
        async with new_session_training() as session:
            quety = select(TrainingOrm)
            result = await session.execute(quety)
            training_models = result.scalars().all()
            training_schemas = [STraining.model_validate(training_model) for training_model in training_models]
            return training_schemas

    @classmethod
    async def delete_training(cls, training_id: int):
        async with new_session_training() as session:
            query = delete(TrainingOrm).where(TrainingOrm.id == training_id)
            await session.execute(query)
            await session.commit()
