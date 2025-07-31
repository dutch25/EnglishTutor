from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import whisper

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


load_dotenv()


ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = "tnSpp4vdxKPjI9w0GnoV"  # Replace this with your voice ID , jerry voice id: 1t1EeRixsJrKbiF1zwM6 / adam voice s3TPKV1kjDlVtZbl4Ksh

@app.get("/audio/{word}")
def get_audio(word: str, speed: float = 0.75):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": word,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.75,
            "speed": speed,
            "similarity_boost": 0.75
            
        }
    }

    response = requests.post(url, headers=headers, json=payload, stream=True)

    if response.status_code != 200:
        print("❌ ElevenLabs error:", response.status_code)
        print("🔍 Response:", response.text)
        return {"error": "Failed to generate audio"}

    return StreamingResponse(response.raw, media_type="audio/mpeg")

@app.post("/chat")
async def chat(data: dict):
    user_message = data.get("message", "")
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_message,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0)
        ),
    )
    return {"reply": response.text}
