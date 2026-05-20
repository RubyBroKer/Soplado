from src.rides.services import RideService
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.auth.dependencies import AccessTokenBearer
from src.rides.schemas import RequestRidesModel
from src.rides.services import RideService

Ride_Router = APIRouter()
Ride_Service = RideService()
access_token_bearer = AccessTokenBearer()


@Ride_Router.get("/", response_model= list[dict])
async def get_all_rides(
    session: AsyncSession = Depends(get_session),
    ride_request: RequestRidesModel = Depends(access_token_bearer)
):
    rides = await Ride_Service.get_all_rides(session, ride_request)
    return rides