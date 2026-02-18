from pydantic import BaseModel
import uuid
from typing import Optional

class AuthModel(BaseModel):

    id : Optional[uuid.UUID]
    username : str
    password : str

class CreateAuthModel(BaseModel):

    username : str
    password : str

class UpdateAuthModel(BaseModel):

    username : Optional[str] = None
    password : Optional[str] = None
    old_password : Optional[str] = None
    is_verified : Optional[bool] = None

class ResponseModel(BaseModel):
    username : str