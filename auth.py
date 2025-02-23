import jwt
import datetime
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# JWT Settings
SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
ALGORITHM = "HS256"

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def hash_password(password: str):
    """Hash a plain text password."""
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """Verify if a password matches its hashed version."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: int = 60):
    """Create a JWT access token with expiration time."""
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_delta)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    """Decode and verify a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
