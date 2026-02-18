from fastapi import FastAPI
from src.Users.routes import User_Router
from src.auth.routes import Auth_Router
from contextlib import asynccontextmanager
from src.db.main import init_db
version = "v1"

@asynccontextmanager
async def lifespan(app : FastAPI):
    print("server is starting")
    await init_db()
    yield
    print("server is stopped")

app = FastAPI(
    title= "Titan",
    description= " A REST Api for customers of titan watch",
    version= version,
    lifespan=lifespan
)

app.include_router(User_Router, prefix=f"/users", tags= ['Users'])
app.include_router(Auth_Router, prefix=f"/auth", tags= ['Auth'])