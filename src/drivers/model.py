from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import datetime

class DriverBase(SQLModel, table = True):
    __tablename__ = "drivers"

    id: int = Field(
        sa_column=Column(
            pg.BIGSERIAL,
            primary_key=True,
            nullable=False
        )
    )
    name: str
    email: str
    phone_number: str
    role: str = Field(
        sa_column=Column(pg.VARCHAR, server_default="user", nullable=False)
    )
    is_active: bool = Field(default=True)
    created_at : datetime.datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.datetime.now)
        )
    updated_at : datetime.datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.datetime.now)
    )

    def __repr__(self):
        
        return f"<Driver id={self.id!r} name={self.name!r} email={self.email!r}>"
