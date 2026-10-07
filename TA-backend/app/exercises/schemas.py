from datetime import datetime

from pydantic import BaseModel

class ExerciseRead(BaseModel):
    id: int
    name: str
    description: str| None
    video_url: str| None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }