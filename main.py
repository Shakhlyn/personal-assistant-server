import pydantic
from pydantic_settings import BaseSettings


from fastapi import FastAPI

app = FastAPI()
@app.get("/", name="home")
async def root():
    return {"message": "Hello World"}
