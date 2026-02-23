from src.Users.schemas import User, UpdateModel, ResponseModel, CreateUserModel
from typing import Optional, List
from fastapi import Header, status,APIRouter, Depends
from fastapi.exceptions import HTTPException
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.Users.services import UserService
from src.auth.dependencies import JWTBearer


User_Router = APIRouter()
User_Service = UserService()
jwt_bearer = JWTBearer()

@User_Router.get('/get_headers',status_code=500)
async def get_headers(
    accept:str = Header(None),
    content_type:str = Header(None),
    user_agent:str = Header(None),
    host:str = Header(None)
):
    request_headers = {}
    request_headers["Accept"] = accept
    request_headers["Content-Type"] = content_type
    request_headers["User-Agent"] = user_agent
    request_headers["Host"] = host
    return request_headers

@User_Router.get("/", response_model= List[ResponseModel])
async def get_users(
    session : AsyncSession = Depends(get_session),
    user_details = Depends(jwt_bearer)) -> list:
    
    Users = await User_Service.get_all_users(session)
    return Users

@User_Router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseModel)
async def create_user(user_dto : CreateUserModel, 
                      session : AsyncSession = Depends(get_session),
                      user_details = Depends(jwt_bearer)) -> dict:
    
    new_user = await User_Service.create_user(user_dto, session)
    return new_user

@User_Router.get("/{user_id}", response_model=ResponseModel)
async def get_by_userId(user_id:str, 
                        session : AsyncSession = Depends(get_session),
                        user_details = Depends(jwt_bearer)) -> dict:

    user = await User_Service.get_user_by_id(user_id, session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
            )
    
    return user

@User_Router.patch("/{user_id}", response_model= ResponseModel)
async def update_user(user_id:str, 
                      user_data : UpdateModel, 
                      session : AsyncSession = Depends(get_session),
                      user_details = Depends(jwt_bearer)) -> dict:

    user_update = await User_Service.update_user(user_id, user_data, session)

    if user_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
            )
    
    return user_update

@User_Router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id:str,
                    session : AsyncSession = Depends(get_session),
                    user_details = Depends(jwt_bearer)) -> None:
    user_delete = await User_Service.delete_user(user_id, session)
        
    if user_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="User does not exist")
    return user_delete
