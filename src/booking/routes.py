from src.booking.schemas import RequestBookingModel, ResponseBookingModel, RequestVehicles
from typing import List, Optional
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.booking.services import BookingService
from src.auth.dependencies import AccessTokenBearer
Booking_Router = APIRouter()
Booking_Service = BookingService()
access_token_bearer = AccessTokenBearer()

@Booking_Router.get("/request",  status_code=status.HTTP_200_OK)
async def check_vehicles(requestDTO : RequestVehicles,
                                 session: AsyncSession = Depends(get_session)):
    
    available_vehicles = await Booking_Service.calculate_fare(requestDTO, session)

    if not available_vehicles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No available vehicles found in the current city.")
    return available_vehicles

@Booking_Router.post("/book", status_code=status.HTTP_200_OK)
async def book_vehicle(requestDTO : RequestBookingModel,
                                 session: AsyncSession = Depends(get_session),
                                 token: str = Depends(access_token_bearer)):
    

    user_id = token["auth_data"]["id"]
    booking_status = await Booking_Service.book_vehicle(user_id, requestDTO, session)
    return booking_status
    




