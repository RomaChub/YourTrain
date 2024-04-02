from typing import Annotated

from fastapi import APIRouter, Depends

from auth.auth_repository import AuthRepository
from chemas import SUser
from repositories.exercise_repository import ExerciseRepository
from chemas.SExercise import SExersiceAdd, SExercise, SExerciseId


router = APIRouter(
    prefix="/YourTrain",
    tags=['Exersice']
)


@router.post("/exercise")
async def add_exercise(
        exercise: Annotated[SExersiceAdd, Depends()],
        user: SUser = Depends(AuthRepository.get_current_active_auth_user),
) -> SExerciseId:
    exercise_id = await ExerciseRepository.add_one(exercise, user.id)
    return {"id": exercise_id}


@router.get("/exercise/{exercise_id}")
async def get_one_exercise(exercise_id: int) -> SExercise:
    exercise_one = await ExerciseRepository.get_one(exercise_id)
    return exercise_one


@router.delete("/exercise/{exercise_id}")
async def delete_exercise(exercise_id: int) -> SExerciseId:
    await ExerciseRepository.delete_exercise(exercise_id)
    return exercise_id


@router.get("/exercise")
async def get_exercises() -> list[SExercise]:
    exercises = await ExerciseRepository.get_all()
    return exercises


@router.put("/exercise/{exercise_id}")
async def update_exercise(exercise_id: int, ex: Annotated[SExersiceAdd, Depends()]) -> SExerciseId:
    success = await ExerciseRepository.update_exercise(exercise_id, ex)
    return {"id": exercise_id}
