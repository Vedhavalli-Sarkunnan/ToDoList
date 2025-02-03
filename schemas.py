from pydantic import BaseModel
from typing import Optional

class TaskSchema(BaseModel):
  task: str

class UpdateUserSchema(BaseModel):
  username: Optional[str] = None
  password: Optional[str] = None

class UserSchema(BaseModel):
  username: str
  password: str

class ShowTask(BaseModel):
  task: str
  class Config():
    from_attributes=True

class ShowUser(BaseModel):
  username: str
  user_id: int
  class Config():
    from_attributes=True

class Token(BaseModel):
  access_token: str
  token_type:str
