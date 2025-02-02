from pydantic import BaseModel

class TaskSchema(BaseModel):
  task: str

class UserSchema(BaseModel):
  username: str
  password: str