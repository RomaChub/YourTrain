from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Text, Any


class SImageAdd(BaseModel):
    image_path: str
    user_id: int
    tag: str
