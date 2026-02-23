from passlib.context import CryptContext
from src.config import Config
from datetime import timedelta, datetime
import jwt
import uuid
import logging

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

ACCESS_TOKEN_EXPIRY = 3600

def hash_password(password : str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password : str, hashed_password : str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(auth_data: dict, expiry : timedelta = None, refresh : bool = False) -> str:

    payload = {}
    payload['auth_data'] = auth_data
    payload['exp'] =  datetime.now() + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload['jit'] = str(uuid.uuid4())
    payload['refresh'] = refresh
    token = jwt.encode(
        payload = payload,
        key = Config.JWT_SECRET_KEY,
        algorithm = Config.JWT_ALGORITHM
    )

    return token

def decode_access_token(token : str) -> dict:

    try:

        token_data = jwt.decode(
            jwt = token,
            key = Config.JWT_SECRET_KEY,
            algorithms = [Config.JWT_ALGORITHM]
        )

        return token_data
    
    except jwt.PyJWTError as e:
        logging.error(f"Token decoding error: {str(e)}")
        return None