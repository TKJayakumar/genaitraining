from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/hello/{name}")
def say_hello(name: str):
    if len(name) < 4:
        raise HTTPException(status_code=400, detail="Name must be at least 4 characters")
    return {"msg": f"Hello {name}"}

class User(BaseModel):
    nam: str

@app.post("/hello")
def create_greeting(user: User):
    return {"msg": f"Hello {user.nam}"}

class User(BaseModel):
    nam: str = Field(min_length=4)
 