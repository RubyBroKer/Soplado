from src.Users.schemas import User, UpdateModel, ResponseModel, CreateUserModel
from typing import Optional, List
from fastapi import Header, status,APIRouter, Depends
from fastapi.exceptions import HTTPException
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.dependencies import JWTBearer, AccessTokenBearer, RefreshTokenBearer
from src.drivers.services import DriverService

Driver_Router = APIRouter()
Driver_Service = DriverService()
jwt_bearer = JWTBearer()
access_token_bearer = AccessTokenBearer()


@Driver_Router.get("/", response_model= List[ResponseModel])
async def get_drivers(
    session : AsyncSession = Depends(get_session),
    driver_details = Depends(access_token_bearer)) -> list:
    
    Drivers = await Driver_Service.get_all_drivers(session)
    return Drivers

@Driver_Router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseModel)
async def create_driver(driver_dto : CreateUserModel, 
                        session : AsyncSession = Depends(get_session),
                      driver_details = Depends(access_token_bearer)) -> dict:
    
    new_driver = await Driver_Service.create_driver(driver_dto, session)
    return new_driver
@Driver_Router.get("/{driver_id}", response_model=ResponseModel)
async def get_by_driverId(driver_id:str, 
                        session : AsyncSession = Depends(get_session),
                        driver_details = Depends(access_token_bearer)) -> dict:
    driver = await Driver_Service.get_driver_by_id(driver_id, session)
    if driver is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver not found"
            )
    
    return driver

@Driver_Router.patch("/{driver_id}", response_model= ResponseModel)
async def update_driver(driver_id:str, 
                        driver_data : UpdateModel, 
                        session : AsyncSession = Depends(get_session),
                        driver_details = Depends(access_token_bearer)) -> dict:
    driver_update = await Driver_Service.update_driver(driver_id, driver_data, session)

    if driver_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver not found"
            )
    
    return driver_update

@Driver_Router.delete("/{driver_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_driver(driver_id:str,
                    session : AsyncSession = Depends(get_session),
                    driver_details = Depends(access_token_bearer)) -> None:
    driver_delete = await Driver_Service.delete_driver(driver_id, session)
        
    if driver_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Driver does not exist")
    return driver_delete
