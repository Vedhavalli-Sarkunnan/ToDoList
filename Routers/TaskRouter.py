from fastapi import APIRouter,HTTPException, Depends
from starlette import status
from schemas import TaskSchema, ShowTask
from models import Task
from database import get_db
from sqlalchemy.orm import Session
from typing import List
from auth.jwt import oauth2_scheme, decode_token

router = APIRouter(tags=["Tasks"], prefix="/task")

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ShowTask])
def get_all_tasks(db: Session = Depends(get_db), token:str = Depends(oauth2_scheme)):
  try:
    user_id = decode_token(token)
    if not user_id:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    all_tasks = db.query(Task).filter(Task.user_id==int(user_id)).all()
    return all_tasks
  except Exception as e:
    print(f"Error in updating task : {e}")

@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_particular_task(id:int, db:Session = Depends(get_db), token:str =Depends(oauth2_scheme)):
  try:
    user_id = decode_token(token)
    if not user_id:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    particular_task= db.query(Task).filter(Task.task_id==id).first()
    if not particular_task:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with ID {id} not found")
    if particular_task.user_id != user_id:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to view task with ID {id}")
    print(particular_task)
    return particular_task
  except Exception as e:
    print(f"Error in getting task : {e}")

@router.post("/",status_code=status.HTTP_201_CREATED)
def add_task(task: TaskSchema, db: Session = Depends(get_db),token:str= Depends(oauth2_scheme)):
  try:
    if task.task.strip()=="":
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can't enter a empty task")
    user_id=decode_token(token)
    if not user_id:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    new_task = Task(task=task.task.strip(),user_id=user_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return { "message" : "Task added successfully", "task" : new_task }
  except Exception as e:
    print(f"Error in adding task : {e}")

@router.put("/{id}", status_code=status.HTTP_200_OK)
def update_task(task: TaskSchema, id:int, db:Session=Depends(get_db), token:str= Depends(oauth2_scheme)):
  try:
    user_id=decode_token(token)
    if not user_id:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    task_to_be_updated=db.query(Task).filter(Task.task_id==id).first()
    if not task_to_be_updated:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with ID {id} not found")
    if task_to_be_updated.user_id !=user_id:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to update task with ID {id}")
    task_to_be_updated.task=str(task)
    db.commit()
    db.refresh(task_to_be_updated)
    return { "message" : "Task updated successfully", "task" : task_to_be_updated }
  except Exception as e:
    print(f"Error in updating task : {e}")


@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete_task(id:int, db:Session = Depends(get_db), token:str=Depends(oauth2_scheme)):
  try:
    user_id=decode_token(token)
    if not user_id:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    task_to_be_deleted = db.query(Task).filter(Task.task_id==id).first()
    if not task_to_be_deleted:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with ID {id} not found")
    if task_to_be_deleted.user_id != user_id:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to delete task with ID {id}")
    db.delete(task_to_be_deleted)
    db.commit()
    return { "message" : "Task deleted successfully", "task" : task_to_be_deleted }
  except Exception as e:
    print(f"Error in deleting task : {e}")