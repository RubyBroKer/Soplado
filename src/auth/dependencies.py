from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi import Request, status, dependencies
from src.auth.utils import decode_access_token
from src.db.redis import token_blocklist, token_in_blocklist
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.services import AuthService

auth_service = AuthService()

class JWTBearer(HTTPBearer):
    
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request : Request) -> HTTPAuthorizationCredentials:

        credentials = await super().__call__(request)
        token = credentials.credentials if credentials else None
        token_data = decode_access_token(token) if token else None
        if await token_in_blocklist(token_data["jti"]):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has been revoked")
        self.verify_token_data(token_data)

        return token_data
    async def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decode_access_token(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid
    
    def verify_token_data(self, token_data):
        raise NotImplementedError("Please Override this method in child classes")
    

class AccessTokenBearer(JWTBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data["refresh"]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please provide a refresh token, not an access token")


class RefreshTokenBearer(JWTBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data["refresh"]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please provide an access token, not a refresh token")
        
async def get_current_user(
        token_data: dict = Depends(AccessTokenBearer())
        , session : AsyncSession = Depends(get_session)
        ) -> dict:
    email = token_data["user"]["email"]
    user = await auth_service.get_user_by_email(email, session)
    return user
