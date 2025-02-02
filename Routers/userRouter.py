from fastapi import APIRouter,HTTPException, Depends
from schemas import UserSchema
from models import User
from starlette import status
from database import get_db
from sqlalchemy.orm import Session
from auth.hashing import hash_password

router = APIRouter(tags=['Users'],prefix="/user")

@router.get("/", status_code=status.HTTP_200_OK)
def get_all_users(db:Session = Depends(get_db)):
  all_users = db.query(User).all()
  return all_users

@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_particular_user(id: int,db:Session = Depends(get_db)):
  particular_user = db.query(User).filter(User.user_id==id).first()
  if not particular_user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")
  return particular_user

@router.post("/",status_code=status.HTTP_201_CREATED)
def add_user(user:UserSchema, db:Session = Depends(get_db)):
  existing_user=db.query(User).filter(User.username==user.username).first()
  if existing_user:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
  new_user= User(username=user.username, password=hash_password(user.password))
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return { "message": "User added successfully", "user": new_user } 

@router.put("/{id}",status_code=status.HTTP_200_OK)
def update_user(id:int, username: str =None, password: str=None, db:Session = Depends(get_db)):
  if not username and not password:
    return {"message" : "No updates to be made"}
  user_to_be_updated = db.query(User).filter(User.user_id==id).first()
  if not user_to_be_updated:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")
  if username:
    user_to_be_updated.username = username
  if password: 
    user_to_be_updated.password = hash_password(password)
  db.commit()
  db.refresh(user_to_be_updated)
  return { "message" : "User updated successfully", "user" : user_to_be_updated }

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_user(id: int, db:Session = Depends(get_db)):
  user_to_be_deleted = db.query(User).filter(User.user_id==id).first()
  if not user_to_be_deleted:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")
  db.delete(user_to_be_deleted)
  db.commit()
  return { "message" : "User deleted successfully", "user" : user_to_be_deleted }