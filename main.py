import os
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Point the client to the 2026 Google Gemini endpoint
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Online", "model": "Gemini 2.5 Flash"}

class ChatRequest(BaseModel):
    message: str
    history: list = []

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    # System prompt sets the behavior of the bot
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    
    # Add conversation history
    for msg in request.history:
        messages.append(msg)
    
    # Add the current user message
    messages.append({"role": "user", "content": request.message})

    # UPDATED: Use 'gemini-2.5-flash' for 2026 stability
    response = client.chat.completions.create(
        model="gemini-2.5-flash", 
        messages=messages
    )
    
    return {"reply": response.choices[0].message.content}

# 1. Define this string with your info (change this later!)
MY_DETAILS = """
I am a Python Developer specializing in Django, FastAPI, and React Native.
I am currently working on projects like 'AuthSocials' and an E-commerce backend.
I use 'uv' for package management and 'Celery/Redis' for background tasks.
I love building scalable backend architectures and clean APIs.
"""


# Add the new endpoint
@app.post("/portfolio-chat")
async def portfolio_chat_endpoint(request: ChatRequest):
    # This system prompt tells the AI to BE you
    messages = [
        {
            "role": "system", 
            "content": f"You are an AI version of me. Answer questions based on these details: {MY_DETAILS}. "
                       f"Be professional, witty, and helpful. If asked something not in the details, "
                       f"answer as a developer would."
        }
    ]
    
    # Add history
    for msg in request.history:
        messages.append(msg)
    
    # Add user message
    messages.append({"role": "user", "content": request.message})

    # Call Gemini 2.5
    response = client.chat.completions.create(
        model="gemini-2.5-flash", 
        messages=messages
    )
    
    return {"reply": response.choices[0].message.content}