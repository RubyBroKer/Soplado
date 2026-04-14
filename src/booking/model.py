from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid
import datetime

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