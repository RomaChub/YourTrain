from database.database import new_session, ExerciseOrm, TrainingOrm

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
    async def update_training(cls, training_id: int, name: str, exercises: int):
        async with new_session() as session:
            training = await session.get(TrainingOrm, training_id)
            if not training:
                return False

            training.name = name
            training.exercises = exercises
            training.add(training)
            await session.commit()
            return True

    @classmethod
    async def delete_training(cls, training_id: int):
        async with new_session() as session:
            query = delete(TrainingOrm).where(TrainingOrm.id == training_id)
            await session.execute(query)
            await session.commit()
