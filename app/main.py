from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O limita a CodePen luego
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class ChatRequest(BaseModel):
    sessionId: str
    chatInput: str

@app.post("/chatbot")
def proxy_chat(req: ChatRequest):
    username = os.getenv("N8N_USER")
    password = os.getenv("N8N_PASS")
    webhook = os.getenv("N8N_WEBHOOK")
    print(f"📨 Recibido mensaje: sessionId={req.sessionId}, chatInput={req.chatInput}")
    if not username or not password or not webhook:
        raise HTTPException(status_code=500, detail="Missing credentials")

    try:
        response = requests.post(
            webhook,
            json={"sessionId": req.sessionId, "chatInput": req.chatInput},
            auth=requests.auth.HTTPBasicAuth(username, password),
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))