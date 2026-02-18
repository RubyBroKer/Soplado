from fastapi import APIRouter
from src.auth.schemas import CreateAuthModel, UpdateAuthModel, ResponseModel, AuthModel
from src.auth.services import AuthService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from fastapi import Depends, status, HTTPException

Auth_Router = APIRouter()
AuthService = AuthService()

@Auth_Router.post("/signup", response_model=ResponseModel)
async def signup(auth_dto : CreateAuthModel, session : AsyncSession = Depends(get_session)) -> dict:
    
    new_auth = await AuthService.signup(auth_dto, session)
    return new_auth

@Auth_Router.post("/login", response_model=ResponseModel)
async def login(auth_dto : AuthModel, session : AsyncSession = Depends(get_session)):
    is_valid = await AuthService.loginAuth(auth_dto, session)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials or email not verified")
    return {"username": auth_dto.username}

@Auth_Router.put("/update", response_model=ResponseModel)
async def update_auth(auth_email : str, update_auth_dto : UpdateAuthModel, session : AsyncSession = Depends(get_session)):
    updated_auth = await AuthService.updateAuth(auth_email, update_auth_dto, session)
    if updated_auth is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found or invalid update parameters")
    return {"username": updated_auth.username}

@Auth_Router.delete("/delete", response_model=ResponseModel)
async def delete_auth(auth_email : str, session : AsyncSession = Depends(get_session)):
    deleted_auth = await AuthService.deleteAuth(auth_email, session)
    if deleted_auth is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"username": deleted_auth.username}