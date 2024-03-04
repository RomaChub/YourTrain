from typing import Annotated

from fastapi import APIRouter, Depends

from repository import ExerciseRepository, TrainingRepository
from schemas import SExersiceAdd, SExercise, SExerciseId, STrainingAdd, STraining, STrainingId

router = APIRouter(
    prefix="/YourTrain"
)


@router.post("/exercise")
async def add_exercise(
        exercise: Annotated[SExersiceAdd, Depends()],
) -> SExerciseId:
    exercise_id = await ExerciseRepository.add_one(exercise)
    return {"exercise_id": exercise_id}


@router.post("/training")
async def add_training(
        training: Annotated[STrainingAdd, Depends()],
) -> STrainingId:
    training_id = await TrainingRepository.add_training(training)
    return {"training_id": training_id}


@router.get("/exercise/{exercise_id}")
async def get_one_exercise(exercise_id: int):
    exercise_one = await ExerciseRepository.get_one(exercise_id)
    return exercise_one


@router.get("/training/{training_id}")
async def get_one_training(training_id: int):
    training_one = await TrainingRepository.get_one(training_id)
    return training_one


@router.delete("/exercise/{exercise_id}")
async def delete_exercise(exercise_id: int):
    await ExerciseRepository.delete_exercise(exercise_id)
    return {"message": f"Exercise with id {exercise_id} has been deleted"}


@router.delete("/training/{training_id}")
async def delete_training(training_id: int):
    await TrainingRepository.delete_training(training_id)
    return {"message": f"Training with id {training_id} has been deleted"}


@router.get("/exercise")
async def get_exercises() -> list[SExercise]:
    exercises = await ExerciseRepository.get_all()
    return exercises


@router.get("/training")
async def get_training() -> list[STraining]:
    training = await TrainingRepository.get_all()
    return training


@router.put("/exercise/{exercise_id}")
async def update_exercise(exercise_id: int, name: str, description: str):
    success = await ExerciseRepository.update_exercise(exercise_id, name, description)
    return {"message": f"Exercise {exercise_id} updated successfully"}


@router.put("/training/{training_id}")
async def update_training(training_id: int, name: str, exercises: int):
    success = await TrainingRepository.update_training(training_id, name, exercises)
    return {"message": f"Training {training_id} updated successfully"}
