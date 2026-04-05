from sqlmodel.ext.asyncio.session import AsyncSession
from src.Users.schemas import CreateUserModel, UpdateModel
from sqlmodel import select, update, delete, desc
from src.Users.model import DriverBase

class DriverService():

    async def get_all_drivers(self, session : AsyncSession):
        statement = select(DriverBase).order_by(desc(DriverBase.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_driver_by_id(self, driver_id : str, session : AsyncSession):

        statement = select(DriverBase).where(DriverBase.id == driver_id)
        result = await session.exec(statement)
        return result.first() if result else None

    async def create_driver(self, driver : CreateUserModel, session : AsyncSession):
        driver_dict = driver.model_dump()
        new_driver = DriverBase(**driver_dict)
        session.add(new_driver)
        await session.commit()
        return new_driver

    async def update_driver(self, driver_id: str, driver_update: UpdateModel, session : AsyncSession):
        
        driver_update_dict = await self.get_driver_by_id(driver_id, session)
        if driver_update_dict is None:
            return None
        update_dict = driver_update.model_dump()
        for key, value in update_dict.items():
            if value is not None:
                setattr(driver_update_dict, key, value)
        
        await session.commit()
        return driver_update_dict
    
    async def delete_driver(self, driver_id: str, session : AsyncSession):

        driver_delete = await self.get_driver_by_id(driver_id, session)
        if driver_delete is None:
            return None
        
        await session.delete(driver_delete)
        await session.commit()
        return "Driver deleted successfully"



    


