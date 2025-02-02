from fastapi import FastAPI
from Routers import taskRouter, userRouter,authRouter
from database import engine
import models

app=FastAPI()

app.include_router(taskRouter.router)
app.include_router(userRouter.router)
app.include_router(authRouter.router)

models.Base.metadata.create_all(bind=engine)