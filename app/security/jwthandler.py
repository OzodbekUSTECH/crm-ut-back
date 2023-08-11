from datetime import datetime, timedelta

from jose import ExpiredSignatureError, JWTError, jwt




class JWTHandler:
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM = "HS256"

    @staticmethod
    async def encode(payload: dict, expires_delta: timedelta = None) -> str:
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=JWTHandler.ACCESS_TOKEN_EXPIRE_MINUTES)
        payload.update({"exp": expire})
        return jwt.encode(payload, JWTHandler.SECRET_KEY, algorithm=JWTHandler.ALGORITHM)

    @staticmethod
    async def decode(token: str) -> dict:
        return jwt.decode(token, JWTHandler.SECRET_KEY, algorithms=[JWTHandler.ALGORITHM])

        
    