from fastapi import APIRouter,HTTPException, Depends
from starlette import status
from schemas import TaskSchema, ShowTask
from models import Task
from database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(tags=["Tasks"], prefix="/task")

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ShowTask])
def get_all_tasks(db: Session = Depends(get_db)):
  all_tasks = db.query(Task).all()
  return all_tasks

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ShowTask)
def get_particular_task(id:int, db:Session = Depends(get_db)):
  particular_task= db.query(Task).filter(Task.task_id==id).first()
  if not particular_task:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with ID {id} not found")
  return particular_task

@router.post("/",status_code=status.HTTP_201_CREATED)
def add_task(task: TaskSchema, db: Session = Depends(get_db)):
  if task.task.strip()=="":
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can't enter a empty task")
  user_id=4
  new_task = Task(task=task.task.strip(),user_id=user_id)
  db.add(new_task)
  db.commit()
  db.refresh(new_task)
  return { "message" : "Task added successfully", "task" : new_task }

@router.put("/{id}", status_code=status.HTTP_200_OK)
def update_task(task: str, id:int, db:Session=Depends(get_db)):
  task_to_be_updated=db.query(Task).filter(Task.task_id==id).first()
  if not task_to_be_updated:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with ID {id} not found")
  task_to_be_updated.task=task
  db.commit()
  db.refresh(task_to_be_updated)
  return { "message" : "Task updated successfully", "task" : task_to_be_updated }


@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete_task(id:int, db:Session = Depends(get_db)):
  task_to_be_deleted = db.query(Task).filter(Task.task_id==id).first()
  if not task_to_be_deleted:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with ID {id} not found")
  db.delete(task_to_be_deleted)
  db.commit()
  return { "message" : "Task deleted successfully", "task" : task_to_be_deleted }
