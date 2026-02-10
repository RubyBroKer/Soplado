from sqlmodel.ext.asyncio.session import AsyncSession
from src.Users.schemas import CreateUserModel, UpdateModel
from sqlmodel import select, update, delete, desc
from src.Users.model import UserBase

class UserService():

    async def get_all_users(self, session : AsyncSession):

        statement = select(UserBase).order_by(desc(UserBase.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_user_by_id(self, user_id : str, session : AsyncSession):

        statement = select(UserBase).where(UserBase.id == user_id)
        result = await session.exec(statement)
        return result.first() if result else None

    async def create_user(self, user : CreateUserModel, session : AsyncSession):

        user_dict = user.model_dump()
        new_user = UserBase(**user_dict)
        session.add(new_user)
        await session.commit()
        return new_user

    async def update_user(self, user_id: str, user_update: UpdateModel, session : AsyncSession):
        
        user_update_dict = await self.get_user_by_id(user_id, session)
        if user_update_dict is None:
            return None
        print(user_update_dict)
        update_dict = user_update.model_dump()
        print(update_dict)
        for key, value in update_dict.items():
            if value is not None:
                setattr(user_update_dict, key, value)
        
        await session.commit()
        return user_update_dict
    
    async def delete_user(self, user_id: str, session : AsyncSession):

        user_delete = await self.get_user_by_id(user_id, session)
        if user_delete is None:
            return None
        
        await session.delete(user_delete)
        await session.commit()
        return "User deleted successfully"



    


