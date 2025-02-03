from fastapi import APIRouter,HTTPException, Depends
from schemas import ShowUser, UpdateUserSchema
from models import User
from starlette import status
from database import get_db
from sqlalchemy.orm import Session
from typing import List
from auth.hashing import hash_password

router = APIRouter(tags=['Users'],prefix="/user")

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ShowUser])
def get_all_users(db:Session = Depends(get_db)):
  try:
    all_users = db.query(User).all()
    return all_users
  except Exception as e:
    print("Error in getting users :", e)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ShowUser)
def get_particular_user(id: int,db:Session = Depends(get_db)):
  try:
    particular_user = db.query(User).filter(User.user_id==id).first() 
    if not particular_user:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")
    return particular_user 
  except Exception as e:
    print("Error in getting user :", e)

@router.put("/{id}",status_code=status.HTTP_200_OK)
def update_user(id:int, user: UpdateUserSchema, db:Session = Depends(get_db)):
  try:
    if not user.username and not user.password:
      return {"message" : "No updates to be made"}
    user_to_be_updated = db.query(User).filter(User.user_id==id).first()
    if not user_to_be_updated:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")
    if user.username:
      user_to_be_updated.username = user.username
    if user.password: 
      user_to_be_updated.password = hash_password(user.password)
    db.commit()
    db.refresh(user_to_be_updated)
    return { "message" : "User updated successfully", "user" : user_to_be_updated }
  except Exception as e:
    print("Error in updating user :", e)

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_user(id: int, db:Session = Depends(get_db)):
  try:
    user_to_be_deleted = db.query(User).filter(User.user_id==id).first()
    if not user_to_be_deleted:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")
    db.delete(user_to_be_deleted)
    db.commit()
    return { "message" : "User deleted successfully", "user" : user_to_be_deleted }
  except Exception as e:
    print("Error in deleting user :", e)