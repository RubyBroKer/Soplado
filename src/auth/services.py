from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.schemas import CreateAuthModel, UpdateAuthModel, AuthModel
from src.auth.models import AuthBase
from sqlmodel import select, update, delete, desc
from src.auth.utils import hash_password, verify_password

class AuthService():


    async def get_auth_email(self, auth_email:str, session : AsyncSession) -> AuthBase:

        statement = select(AuthBase).where(AuthBase.username == auth_email)
        result = await session.exec(statement)
        return result.first() if result else None

    async def createAuth(self, auth : CreateAuthModel, session : AsyncSession) -> AuthBase:
        user = await self.get_auth_email(auth.username, session)
        if user is not None:
            return None
        
        auth_dict = auth.model_dump()
        auth_dict["password"] = hash_password(auth_dict["password"])
        new_auth = AuthBase(**auth_dict)
        session.add(new_auth)
        await session.commit()

        return new_auth
    
    async def loginAuth(self, auth : AuthModel, session : AsyncSession) -> bool:

        auth_dict = await self.get_auth_email(auth.username, session)

        if auth_dict is None:
            return False
        
        if not auth_dict.is_verified:
            return False
        
        if not verify_password(auth.password, auth_dict.password):
            return False
        
        return True
    
    async def updateAuth(self, auth_email : str, update_auth : UpdateAuthModel, session : AsyncSession) -> AuthBase:

        auth_dict = await self.get_auth_email(auth_email, session)
        if auth_dict is None:
            return None
        
        update_dict = update_auth.model_dump()
        if update_dict["is_verified"] is True:
            setattr(auth_dict, "is_verified", True)
        
        if update_dict["password"] is not None:
            if update_dict["old_password"] is None:
                return None
            
            if not verify_password(update_dict["old_password"], auth_dict.password):
                return None
            
            setattr(auth_dict, "password", hash_password(update_dict["password"]))
        
        await session.commit()
        return auth_dict
    
    async def deleteAuth(self, auth_email : str, session : AsyncSession):

        auth_dict = await self.get_auth_email(auth_email, session)

        if auth_dict is None:
            return None
        
        if not verify_password(auth_dict.password, auth_dict.password):
            return None
        await session.delete(auth_dict)

        await session.commit()

        return "Authentication Removed"


