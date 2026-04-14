from fastapi import FastAPI
#import routers
from src.Users.routes import User_Router
from src.auth.routes import Auth_Router
from src.drivers.routes import Driver_Router
from src.booking.routes import Booking_Router

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
app.include_router(Driver_Router, prefix=f"/drivers", tags= ['Drivers'])
app.include_router(Booking_Router, prefix=f"/bookings", tags= ['Bookings'])
