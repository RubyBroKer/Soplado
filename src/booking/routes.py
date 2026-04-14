from src.booking.schemas import RequestBookingModel, ResponseBookingModel
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

