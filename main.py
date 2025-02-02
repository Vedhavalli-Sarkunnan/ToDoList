from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def simple_function():
  return "Working"
