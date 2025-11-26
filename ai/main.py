from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# OpenAI 사용 위해 import
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import os

app = FastAPI(root_path="/ai")

# 요청 받을 데이터구조
class StoryRequest(BaseModel):
    age: int
    topic: str
    words: list[str]

# 3. LangChain 설정
llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

@app.get("/")
def read_root():
    return {"message": "Hello from AI Server!"}

@app.post("/generate-story")
async def generate_story(req: StoryRequest):
    return {"story": f"{req.age}세 아이를 위해 {req.topic} 주제로 동화를 만들 예정입니다."}