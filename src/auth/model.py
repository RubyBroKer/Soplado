from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid

class AuthBase(SQLModel, table = True):
    __tablename__ = "auth"

    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            default=uuid.uuid4(),
            nullable=False
        )
    )

    username : str
    password : str
    is_verified : bool = Field(default=False)

    def __repr__(self):
        return "Id is {} and username is {}".format(self.id, self.username)