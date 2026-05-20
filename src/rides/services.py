from sqlmodel.ext.asyncio.session import AsyncSession
from src.rides.schemas import RequestRidesModel
from kafka import KafkaConsumer
from src.config import Config
class RideService():

    async def get_all_rides(self, session: AsyncSession, ride_request: RequestRidesModel):

        pass