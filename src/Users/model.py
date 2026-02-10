from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid
import datetime

class UserBase(SQLModel, table = True):
    __tablename__ = "users"

    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            default=uuid.uuid4(),
            nullable=False
        )
    )
    name: str
    email: str
    phone_number: str
    role: str
    is_active: bool = Field(default=True)
    created_at : datetime.datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.datetime.now)
        )
    updated_at : datetime.datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.datetime.now)
    )

    def __repr__(self):
        
        return f"<User id={self.id!r} name={self.name!r} email={self.email!r}>"
