from pydantic import BaseModel, field_validator
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
    booking_date: datetime
    ride : str
    started_at: datetime
    longitude_pickup: str
    latitude_pickup: str
    longitude_dropoff: str
    latitude_dropoff: str
    current_city: str

    @field_validator("booking_date", "started_at", mode="before")
    @classmethod
    def parse_dmy_dates(cls, value):
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%d-%m-%Y")
            except ValueError:
                return value
        return value

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

class VehicleDetails(BaseModel):
    distance : float
    vehicle_type: str
    total_fare: str

class RequestVehicles(BaseModel):
    longitude_pickup: str
    latitude_pickup: str
    longitude_dropoff: str
    latitude_dropoff: str
    current_city: str

