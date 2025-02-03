from fastapi import HTTPException
from starlette import status
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime,timedelta,timezone
from typing import Optional
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

expiration_time=int(os.getenv("EXPIRATION_TIME"))
secret_key=os.getenv("SECRET_KEY")
algorithm=os.getenv("ALGORITHM")

def create_access_token(data:dict, expires_delta: Optional[timedelta] =None):
  to_encode = data.copy()
  expires= datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=expiration_time))
  print("Expires :",expires)
  print("Time now :",datetime.now(timezone.utc))
  to_encode.update({"exp": int(expires.timestamp())})
  jwt_token = jwt.encode(to_encode,secret_key ,algorithm=algorithm)
  return jwt_token

def decode_token(token: str):
  try:
    print("Inside function")
    data = jwt.decode(token,secret_key,algorithms=[algorithm])
    print("Decoded data",data)
    return int(data.get("sub"))
  except JWTError as e:
    print("Token Decode Error :",e)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not decode token")

