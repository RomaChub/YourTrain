from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException

from api.auth.auth_repository import AuthRepository
from api.chemas.SUser import SUser
from api.chemas.SExercise import SExercise, SExerciseAdd, SExerciseId
from api.repositories.exercise_repository import ExerciseRepository

router = APIRouter(
    prefix="/your_train",
    tags=['Exercise']
)


@router.post("/exercise", response_model=SExerciseId, status_code=201)
async def add_exercise(
        exercise: Annotated[SExerciseAdd, Depends()],
        user: SUser = Depends(AuthRepository.get_current_active_auth_user)) -> SExerciseId:
    try:
        exercise_id = await ExerciseRepository.add_one(exercise, user.id)
        return {"id": exercise_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/exercise/{exercise_id}", response_model=SExercise)
async def get_one_exercise(
        exercise_id: int,
        user: SUser = Depends(AuthRepository.get_current_active_auth_user)) -> SExercise:
    exercise_one = await ExerciseRepository.get_one(exercise_id)
    if exercise_one is None:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise_one


@router.delete("/exercise/{exercise_id}", response_model=SExerciseId)
async def delete_exercise(
        exercise_id: int,
        user: SUser = Depends(AuthRepository.get_current_active_auth_user)
                          ) -> SExerciseId:
    try:
        await ExerciseRepository.delete(exercise_id)
        return {"id": exercise_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/exercise", response_model=List[SExercise])
async def get_exercises( user: SUser = Depends(AuthRepository.get_current_active_auth_user)) -> List[SExercise]:
    exercises = await ExerciseRepository.get_all()
    return exercises


@router.put("/exercise/{exercise_id}", response_model=SExerciseId)
async def update_exercise(exercise_id: int, ex: Annotated[SExerciseAdd, Depends()],
                          user: SUser = Depends(AuthRepository.get_current_active_auth_user)
                          ) -> SExerciseId:
    try:
        success = await ExerciseRepository.update(exercise_id, ex)
        if not success:
            raise HTTPException(status_code=404, detail="Exercise not found")
        return {"id": exercise_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
