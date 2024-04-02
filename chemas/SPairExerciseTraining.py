from pydantic import BaseModel, ConfigDict


class SPairExerciseTrainingAdd(BaseModel):
    exercise_id: int
    training_id: int


class SPairExerciseTraining(SPairExerciseTrainingAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class SPairExerciseTrainingId(BaseModel):
    pair_id: int
