from fastapi import FastAPI
from Routers import TaskRouter

app=FastAPI()

app.include_router(TaskRouter.router)
