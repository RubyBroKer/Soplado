from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.schemas import CreateAuthModel, UpdateAuthModel
from src.auth.models import AuthBase
from sqlmodel import select, update, delete, desc


class AuthService():


    async def get_auth_id(self, auth_id:str, session : AsyncSession) -> AuthBase:

        statement = select(AuthBase).where(AuthBase.id == auth_id)
        result = await session.exec(statement)
        return result.first() if result else None

    async def createAuth(self, auth : CreateAuthModel, session : AsyncSession) -> AuthBase:

        auth_dict = auth.model_dump()
        new_auth = AuthBase(**auth_dict)
        session.add(new_auth)
        await session.commit()

        return new_auth
    
    async def updateAuth(self, auth_id : str, update_auth : UpdateAuthModel, session : AsyncSession) -> AuthBase:

        auth_dict = await self.get_auth_id(auth_id)
        if auth_dict is None:
            return None
        
        update_dict = auth_dict.model_dump()

        for key, value in update_dict.items():
            if value is not None:
                setattr(auth_dict, key, value)
        
        await session.commit()
        return auth_dict
    
    async def deleteAuth(self, auth_id : str, session : AsyncSession):

        auth_dict = await self.get_auth_id(auth_id)

        if auth_dict is None:
            return None
        
        await session.delete(auth_dict)

        await session.commit()

        return "Authentication Removed"


