from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

class BookingBase(BaseModel):
    id: Optional[uuid.UUID]  # UUID PRIMARY KEY
    user_id: uuid.UUID  # UUID FOREIGN KEY to users.id
    booking_date: datetime
    ride : str
    started_at: datetime
    pickup_location: str
    dropoff_location: str
    status: Optional[str] = "pending"  # default 'pending'
    created_at: Optional[datetime] = None  

class RequestBookingModel(BaseModel):
    user_id: uuid.UUID
    booking_date: datetime
    ride : str
    started_at: datetime
    pickup_location: str
    dropoff_location: str

class ResponseBookingModel(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    booking_date: datetime
    ride : str
    started_at: datetime
    pickup_location: str
    dropoff_location: str
    status: str
    created_at: datetime