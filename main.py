from fastapi import FastAPI
from Routers import taskRouter, userRouter
from database import engine
import models

app=FastAPI()

app.include_router(taskRouter.router)
app.include_router(userRouter.router)

models.Base.metadata.create_all(bind=engine)