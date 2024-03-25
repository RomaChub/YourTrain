from fastapi import APIRouter

from repositories.exercise_to_training import ExerciseToTraining
from chemas.schemas import SPairExerciseTrainingId, SPairExerciseTraining

router = APIRouter(
    prefix="/YourTrain",
    tags=['ExerciseToTraining']
)


@router.post("/pair")
async def add_pair(
        exercise_id: int,
        training_id: int
) -> SPairExerciseTrainingId:
    pair_id = await ExerciseToTraining.add_one(exercise_id, training_id)
    return {"pair_id": pair_id}

@router.get("/pair")
async def get_pairs() -> list[SPairExerciseTraining]:
    pairs = await ExerciseToTraining.get_all()
    return pairs

