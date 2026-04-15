from sqlalchemy.ext.asyncio import AsyncSession
from src.booking.schemas import RequestBookingModel, ResponseBookingModel
from sqlmodel import select, update, delete, desc
from src.booking.model import BookingBase, TravellingDetails
from src.config import Config
import requests

class BookingService():

    async def get_available_vehicles(self, requestDTO : RequestBookingModel, session : AsyncSession):

        current_city = requestDTO.current_city
        try:
            statement = select(TravellingDetails).where(
                TravellingDetails.city == current_city)
        except Exception as e:
            print(f"Error fetching available vehicles: {e}")
            return []

        available_vehicles = await session.exec(statement)

        return available_vehicles.all()
    
    async def calculate_fare(self, requestDTO : RequestBookingModel, session : AsyncSession):

        # Fetch the distance between pickup and dropoff locations using OpenCage API
        api_key = Config.OPENCAGE_API_KEY
        print(f"Calculating fare for request: {requestDTO}")
        url = f"https://api.bigdatacloud.net/data/reverse-geocode-client?q={requestDTO.latitude_dropoff}+{requestDTO.longitude_dropoff}"
        response = requests.get(url)
        data = response.json()
        city = data.get("city")
        print(f"Current city from OpenCage API: {city}")

        if city!= requestDTO.current_city:
            return None
        
        available_vehicles = await self.get_available_vehicles(requestDTO, session)
        if not available_vehicles:
            return None
        
        url = f"http://router.project-osrm.org/route/v1/driving/{requestDTO.latitude_pickup},{requestDTO.longitude_pickup};{requestDTO.latitude_dropoff},{requestDTO.longitude_dropoff}?overview=false"
    
        response = requests.get(url)
        data = response.json()
        distance = data["routes"][0]["distance"] / 1000
        print(f"Distance between pickup and dropoff: {distance} km")
        vehicle_options = []
        for vehicle in available_vehicles:
            total_fare = vehicle.base_fare_inr + (vehicle.cost_per_km_inr * distance)
            vehicle_options.append({
                "vehicle_type": vehicle.vehicle_type,
                "total_fare": round(total_fare, 2)
            })
        return vehicle_options