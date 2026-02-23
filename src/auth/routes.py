from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.auth.schemas import CreateAuthModel, UpdateAuthModel, ResponseModel, AuthModel
from src.auth.services import AuthService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from fastapi import Depends, status, HTTPException
from src.auth.utils import create_access_token, decode_access_token
from src.auth.dependencies import JWTBearer

Auth_Router = APIRouter()
Auth_Service = AuthService()
jwt_bearer = JWTBearer()

@Auth_Router.post("/signup", response_model=ResponseModel)
async def signup(
    auth_dto : CreateAuthModel, 
    session : AsyncSession = Depends(get_session),
    user_details = Depends(jwt_bearer)
    ) -> dict:
    
    new_auth = await Auth_Service.createAuth(auth_dto, session)
    return new_auth

@Auth_Router.post("/login", response_model=ResponseModel)
async def login(auth_dto : CreateAuthModel, session : AsyncSession = Depends(get_session)):
    jwt_data = await Auth_Service.loginAuth(auth_dto, session)
    if not jwt_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials or email not verified")

    return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": jwt_data["access_token"],
                    "refresh_token": jwt_data["refresh_token"],
                }
            )
@Auth_Router.put("/update", response_model=ResponseModel)
async def update_auth(email : str, update_auth_dto : UpdateAuthModel, session : AsyncSession = Depends(get_session)):
    updated_auth = await Auth_Service.updateAuth(email, update_auth_dto, session)
    if updated_auth is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found or invalid update parameters")
    return {"username": updated_auth.username}

@Auth_Router.delete("/delete", response_model=ResponseModel)
async def delete_auth(email : str, session : AsyncSession = Depends(get_session)):
    deleted_auth = await Auth_Service.deleteAuth(email, session)
    if deleted_auth is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"username": deleted_auth.username}