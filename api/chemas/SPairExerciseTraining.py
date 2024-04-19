from pydantic import BaseModel, ConfigDict


class SPairExerciseTrainingAdd(BaseModel):
    exercise_id: int
    training_id: int


class SPairExerciseTraining(SPairExerciseTrainingAdd):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)


class SPairExerciseTrainingId(BaseModel):
    id: int
