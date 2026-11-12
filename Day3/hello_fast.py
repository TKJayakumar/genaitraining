
from fastapi import FastAPI
from pydantic import BaseModel, Field
from hello_llm import ask_question

app = FastAPI()

class User(BaseModel):
    nam: str = Field(min_length=3)
    quest: str = Field(min_length=5)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/ask")
def create_greeting(user: User):

    answer = ask_question(user.quest)

    return {
        "msg": f"{user.nam} answer: {answer.msg}",
        "reference": answer.reference,
        "confidence": answer.confidence
    }
