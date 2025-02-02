from fastapi import FastAPI
from Routers import taskRouter
from database import engine
import models

app=FastAPI()

app.include_router(taskRouter.router)

models.Base.metadata.create_all(bind=engine)