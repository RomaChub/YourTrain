from fastapi import APIRouter, Depends

from auth.auth_repository import AuthRepository
from chemas.SUser import SUser
from repositories.exercise_to_training import ExerciseToTraining
from chemas.SPairExerciseTraining import SPairExerciseTrainingId, SPairExerciseTraining

router = APIRouter(
    prefix="/YourTrain",
    tags=['ExerciseToTraining']
)


@router.post("/pair")
async def add_pair(
        exercise_id: int,
        training_id: int,
        user: SUser = Depends(AuthRepository.get_current_active_auth_user),
) -> SPairExerciseTrainingId:
    pair_id = await ExerciseToTraining.add_one(exercise_id, training_id, user.id)
    return {"id": pair_id}


@router.get("/pair")
async def get_pairs() -> list:
    pairs = await ExerciseToTraining.get_all()
    return pairs
