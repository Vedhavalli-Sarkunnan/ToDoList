from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP,text,ForeignKey
from sqlalchemy.orm import relationship

class Task(Base):
  __tablename__ = "Tasks"
  task_id = Column(Integer, primary_key=True,index=True,nullable=False,autoincrement=True)
  task = Column(String,nullable=False)
  created_at = Column(TIMESTAMP(timezone=True),server_default=text('now()'))
  user_id = Column(Integer,ForeignKey("Users.user_id"))
  user=relationship("User",back_populates="tasks")

class User(Base):
  __tablename__ = "Users"
  user_id = Column(Integer, primary_key=True,index=True, nullable=False,autoincrement=True)
  username = Column(String, nullable=False)
  password = Column(String, nullable=False)
  tasks=relationship("Task",back_populates="user")
