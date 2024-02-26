from typing import Annotated

from fastapi import APIRouter, Depends

from repository import ExerciseRepository
from schemas import SExersiceAdd, SExercise, SExerciseId

router = APIRouter(
    prefix="/exercises",
    tags=["Exercises"],
)


@router.post("")
async def add_exercise(
        exercise: Annotated[SExersiceAdd, Depends()],
) -> SExerciseId:
    exercise_id = await ExerciseRepository.add_one(exercise)
    return {"ok": True, "exercise_id": exercise_id}


@router.get("/{exercise_id}")
async def get_one_exercise(exercise_id: int):
    exercise_one = await ExerciseRepository.get_one(exercise_id)
    return exercise_one


@router.delete("/exercise/{exercise_id}")
async def delete_exercise(exercise_id: int):
    await ExerciseRepository.delete_exercise(exercise_id)
    return {"message": f"Exercise with id {exercise_id} has been deleted"}


@router.get("")
async def get_exercises() -> list[SExercise]:
    exercises = await ExerciseRepository.get_all()
    return exercises
