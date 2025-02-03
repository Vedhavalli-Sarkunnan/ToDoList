from fastapi import HTTPException, Depends, APIRouter
from starlette import status
from schemas import UserSchema,Token
from auth.hashing import hash_password,verify_password
from models import User
from sqlalchemy.orm import Session
from database import get_db
from auth.jwt import create_access_token

router = APIRouter(tags=["Auth"],prefix="/auth")

@router.post("/register",status_code=status.HTTP_201_CREATED)
def register(user:UserSchema, db:Session = Depends(get_db)):
  if " " in user.username:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username cannot have space-separated words")
  existing_user=db.query(User).filter(User.username==user.username).first()
  if existing_user:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
  new_user= User(username=user.username, password=hash_password(user.password))
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return { "message": "User added successfully", "user": new_user }

@router.post("/login", status_code=status.HTTP_200_OK)
def login(data:UserSchema, db:Session = Depends(get_db)):
  user=db.query(User).filter(User.username==data.username).first()
  if not user or not verify_password(data.password,user.password): 
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid Credentials")
  token=create_access_token(data={"sub":str(user.user_id)})
  return Token(access_token=token,token_type="Bearer")




  