
import os
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "uv + FastAPI"}

class ChatRequest(BaseModel):
    message: str
    history: list = []  # Optional: Pass previous messages for memory

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    # Format messages for the API
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    
    # Add history + new message
    for msg in request.history:
        messages.append(msg)
    messages.append({"role": "user", "content": request.message})

    response = client.chat.completions.create(
        model="gpt-4o-mini", # Fast and cheap for 2026
        messages=messages
    )
    
    return {"reply": response.choices[0].message.content}