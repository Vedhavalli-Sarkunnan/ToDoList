from pydantic import BaseModel

class TaskSchema(BaseModel):
  task: str

class UserSchema(BaseModel):
  username: str
  password: str

class ShowTask(BaseModel):
  task: str
  class Config():
    orm_mode=True

class ShowUser(BaseModel):
  username: str
  class Config():
    orm_mode=True
    