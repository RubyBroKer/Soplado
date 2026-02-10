from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class User(BaseModel):
    id: Optional[uuid.UUID]  # UUID PRIMARY KEY
    name: Optional[str] = None  # Added name field
    email: str    # VARCHAR(255) UNIQUE NOT NULL
    phone_number: Optional[str] = None  # VARCHAR(20) UNIQUE, can be null
    role: str  # Enforce SQL CHECK constraint
    is_active: Optional[bool] = True  # default TRUE
    created_at: Optional[datetime] = None  # default NOW()
    updated_at: Optional[datetime] = None  # default NOW()

class CreateUserModel(BaseModel):
    name: str
    email: str
    phone_number: str
    role: str

class ResponseModel(BaseModel):
    id : uuid.UUID
    name : str
    email : str
    phone_number : str
    role : str
    is_active : bool

class UpdateModel(BaseModel):
    email : Optional[str] = None
    phone_number : Optional[str] = None
    is_active : Optional[bool] = None