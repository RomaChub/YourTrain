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


@router.get("")
async def get_exercises() -> list[SExercise]:
    exercises = await ExerciseRepository.get_all()
    return exercises
