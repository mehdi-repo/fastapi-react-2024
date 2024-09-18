from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from model.user_model import User
from repository import user_crud
from sqlalchemy.orm import Session
from schema import user_schema
from database.connection import get_db

from datetime import datetime, timedelta
import bcrypt
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext


SECRET_KEY = "098166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")



# Password
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))



# create access Token 
def create_access_token(User:user_schema.User) -> str: 
    to_encode = {"user_id": User.id, "username": User.username}
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# verify token (First authenticate user method)
def verify_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")  
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Fetch the user using the CRUD method
    user = user_crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    
    return user



# Function to authenticate user
def authenticate_user(username: str, password: str,db: Session = Depends(get_db)):
    user = user_crud.get_user_by_username(db=db,username=username)
    if not user:
        return False
    if not verify_password(password,user.password): # type: ignore
        return False
    return user








