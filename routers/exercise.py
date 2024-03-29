from typing import Annotated

from fastapi import APIRouter, Depends

from auth.auth_repository import AuthRepository
from auth.schemas import UserSchema
from repositories.exercise_repository import ExerciseRepository
from chemas.schemas import SExersiceAdd, SExercise, SExerciseId


router = APIRouter(
    prefix="/YourTrain",
    tags=['Exersice']
)


@router.post("/exercise")
async def add_exercise(
        exercise: Annotated[SExersiceAdd, Depends()],
        user: UserSchema = Depends(AuthRepository.get_current_active_auth_user),
) -> SExerciseId:
    exercise_id = await ExerciseRepository.add_one(exercise,user.username)
    return {"exercise_id": exercise_id}


@router.get("/exercise/{exercise_id}")
async def get_one_exercise(exercise_id: int):
    exercise_one = await ExerciseRepository.get_one(exercise_id)
    return exercise_one


@router.delete("/exercise/{exercise_id}")
async def delete_exercise(exercise_id: int):
    await ExerciseRepository.delete_exercise(exercise_id)
    return {"message": f"Exercise with id {exercise_id} has been deleted"}


@router.get("/exercise")
async def get_exercises() -> list[SExercise]:
    exercises = await ExerciseRepository.get_all()
    return exercises


@router.put("/exercise/{exercise_id}")
async def update_exercise(exercise_id: int, name: str, description: str):
    success = await ExerciseRepository.update_exercise(exercise_id, name, description)
    return {"message": f"Exercise {exercise_id} updated successfully"}
