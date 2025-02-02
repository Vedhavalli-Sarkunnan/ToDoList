from fastapi import APIRouter,HTTPException
from starlette import status

router = APIRouter(tags=["Tasks"], prefix="/task")

tasks= []
id=0

@router.get("/", status_code=status.HTTP_200_OK)
def get_all_tasks():
  return tasks

@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_particular_task(id:int):
  if(len(tasks)<id):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with ID {id} not found")
  return tasks[id-1]

@router.post("/",status_code=status.HTTP_201_CREATED)
def add_task(task: str):
  tasks.append(task)
  return task

@router.put("/{id}", status_code=status.HTTP_201_CREATED)
def update_task(task:str, id:int):
  if(len(tasks)<id):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with ID {id} not found")
  tasks[id-1]=task
  return task

@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete_task(id:int):
  if(len(tasks)<id):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with ID {id} not found")
  del tasks[id-1]
  return "Deleted successfully"
