from fastapi import APIRouter, Depends, HTTPException

from api.auth.auth_repository import AuthRepository
from api.chemas.SUser import SUser
from api.repositories.exercise_to_training import ExerciseToTraining
from api.chemas.SPairExerciseTraining import SPairExerciseTrainingId, SPairExerciseTraining

router = APIRouter(
    prefix="/your_train",
    tags=['ExerciseToTraining']
)


@router.post("/pair", response_model=SPairExerciseTrainingId)
async def add_pair(
        exercise_id: int,
        training_id: int,
        user: SUser = Depends(AuthRepository.get_current_active_auth_user),
) -> SPairExerciseTrainingId:
    try:
        pair_id = await ExerciseToTraining.add_one(exercise_id, training_id, user.id)
        return {"id": pair_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pair", response_model=list[SPairExerciseTraining])
async def get_pairs( user: SUser = Depends(AuthRepository.get_current_active_auth_user)) -> list[SPairExerciseTraining]:
    try:
        pairs = await ExerciseToTraining.get_all()
        return pairs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
