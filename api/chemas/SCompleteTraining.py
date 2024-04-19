from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SCompleteTraining(BaseModel):
    id: int
    training_id: int
    time_start: datetime
    time_end: datetime
    user_id: int

    model_config = ConfigDict(from_attributes=True)
