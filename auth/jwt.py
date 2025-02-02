from fastapi import HTTPException
from starlette import status
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime,timedelta
from typing import Optional
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

expiration_time=os.getenv("EXPIRATION_TIME")
secret_key=os.getenv("SECRET_KEY")
algorithm=os.getenv("ALGORITHM")

def create_access_token(data:dict, expires_delta: Optional[timedelta] =None):
  to_encode = data.copy()
  if expires_delta:
    expires= datetime.utcnow() + expires_delta
  else:
    expires = datetime.utcnow() + timedelta(minutes=int(expiration_time))
  to_encode.update({"exp": expires})
  jwt_token = jwt.encode(to_encode,secret_key ,algorithm=algorithm)
  return jwt_token

def decode_token(token: str):
  try:
    data = jwt.decode(token,secret_key,algorithms=[algorithm])
    return data.get("sub")
  except JWTError:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not decode token")

