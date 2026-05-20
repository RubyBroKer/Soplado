from pydantic import BaseModel, Field
from typing import Optional
import uuid
from datetime import datetime

class RidesBase(BaseModel):
    id: Optional[uuid.UUID]  # UUID PRIMARY KEY
    current_longitude: str
    current_latitude: str
    vehicle_type: str


class RequestRidesModel(BaseModel):
    current_longitude: str
    current_latitude: str
    vehicle_type: str