
import os
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Point the client to Google Gemini's endpoint
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "uv + FastAPI"}

class ChatRequest(BaseModel):
    message: str
    history: list = []  # Optional: Pass previous messages for memory

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    
    for msg in request.history:
        messages.append(msg)
    messages.append({"role": "user", "content": request.message})

    # Use a Gemini model name here
    response = client.chat.completions.create(
        model="gemini-1.5-flash", 
        messages=messages
    )
    
    return {"reply": response.choices[0].message.content}