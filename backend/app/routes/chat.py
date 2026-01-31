from fastapi import APIRouter
import requests

router = APIRouter()

@router.post("/chat")
async def chat_ai(payload: dict):
    prompt = payload.get("message", "")

    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "llama3",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }
    )

    data = response.json()

    return {
        "reply": data["message"]["content"]
    }
