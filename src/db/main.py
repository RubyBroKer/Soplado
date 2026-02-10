from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from src.config import Config
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

engine: AsyncEngine = create_async_engine(
    Config.DATABASE_URL,
    echo=True,
    future=True,
)

async def init_db():
    async with engine.begin() as conn:
            from src.Users.model import UserBase
            await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    
    Session = sessionmaker(
         bind = engine, 
         class_=AsyncSession,
         expire_on_commit=False
    )

    async with Session() as session:
         yield session
