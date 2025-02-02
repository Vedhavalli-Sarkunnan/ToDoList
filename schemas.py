from pydantic import BaseModel

class TaskSchema(BaseModel):
  task: str

class UserSchema(BaseModel):
  username: str
  password: str

class ShowTask(BaseModel):
  task: str
  class Config():
    from_attributes=True

class ShowUser(BaseModel):
  username: str
  class Config():
    from_attributes=True

class Token(BaseModel):
  access_token: str
  token_type:str
