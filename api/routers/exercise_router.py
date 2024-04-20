from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from api.auth.auth_repository import AuthRepository
from api.chemas import SUser
from api.repositories.exercise_repository import ExerciseRepository
from api.chemas.SExercise import SExerciseAdd, SExercise, SExerciseId


router = APIRouter(
    prefix="/your_train",
    tags=['Exercise']
)


@router.post("/exercise", response_model=SExerciseId)
async def add_exercise(
        exercise: Annotated[SExerciseAdd, Depends()],
        user: SUser = Depends(AuthRepository.get_current_active_auth_user),
) -> SExerciseId:
    try:
        exercise_id = await ExerciseRepository.add_one(exercise, user.id)
        return {"id": exercise_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/exercise/{exercise_id}", response_model=SExercise)
async def get_one_exercise(exercise_id: int) -> SExercise:
    exercise_one = await ExerciseRepository.get_one(exercise_id)
    if exercise_one is None:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise_one


@router.delete("/exercise/{exercise_id}", response_model=SExerciseId)
async def delete_exercise(exercise_id: int) -> SExerciseId:
    try:
        await ExerciseRepository.delete(exercise_id)
        return {"id": exercise_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/exercise", response_model=list[SExercise])
async def get_exercises() -> list[SExercise]:
    exercises = await ExerciseRepository.get_all()
    return exercises


@router.put("/exercise/{exercise_id}", response_model=SExerciseId)
async def update_exercise(exercise_id: int, ex: Annotated[SExerciseAdd, Depends()]) -> SExerciseId:
    try:
        success = await ExerciseRepository.update(exercise_id, ex)
        return {"id": exercise_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
