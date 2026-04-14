from sqlalchemy.ext.asyncio import AsyncSession
from src.booking.schemas import RequestBookingModel, ResponseBookingModel
from sqlmodel import select, update, delete, desc
from src.booking.model import BookingBase

class BookingService():
    pass