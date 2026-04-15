from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid
import datetime
from sqlalchemy import Column, BigInteger


class BookingBase(SQLModel, table = True):
    __tablename__ = "bookings"

    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            default=uuid.uuid4(),
            nullable=False
        )
    )
    user_id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False
        )
    )
    booking_date: datetime.datetime
    started_at: datetime.datetime
    ride : str
    pickup_location: str
    dropoff_location: str
    status: str = Field(
        sa_column=Column(pg.VARCHAR, server_default="pending", nullable=False)
    )
    created_at : datetime.datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.datetime.now)
        )

    def __repr__(self):
        
        return f"<Booking id={self.id!r} user_id={self.user_id!r} booking_date={self.booking_date!r}>"
    

class TravellingDetails(SQLModel, table=True):

    __tablename__ = "transport_pricing"

    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            default=uuid.uuid4(),
            nullable=False
        )
    )
    city: str
    vehicle_type: str
    base_fare_inr : float
    cost_per_km_inr : float
    surge_multiplier: float

    def __repr__(self):
        return f"<TravellingDetails city={self.city!r} vehicle_type={self.vehicle_type!r} base_fare_inr={self.base_fare_inr!r}>"
