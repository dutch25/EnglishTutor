from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
import requests
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from whisper import router as whisper_router   # ✅ router của whisper
from auth_routes import router as auth_router  # ✅ router login/register

# ✅ Khởi tạo FastAPI
app = FastAPI()

# ✅ Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Load biến môi trường
load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = "tnSpp4vdxKPjI9w0GnoV"  # Replace with your voice ID

# ✅ Import router whisper & auth
app.include_router(whisper_router)  # API liên quan đến Whisper
app.include_router(auth_router)     # API đăng nhập & đăng ký

# ✅ API Root
@app.get("/")
def read_root():
    return {"message": "Welcome to the English Tutor API"}

# ✅ API lấy audio từ ElevenLabs
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

# ✅ API Chat với Gemini
# ✅ API Chat với Gemini
@app.post("/chat")
async def chat(data: dict):
    user_message = data.get("message", "")

    # ✅ Prompt hướng dẫn thêm
    system_prompt = (
        "Bạn là một gia sư tiếng Anh chuyên giúp người Việt luyện nghe và nói. "
        "Hãy trả lời ngắn gọn, dễ hiểu, và phù hợp cho mọi trình độ."
    )

    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{system_prompt}\nNgười học: {user_message}",
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0)
        ),
    )
    return {"reply": response.text}

# ✅ Kết nối MySQL (nếu cần dùng trực tiếp ngoài ORM)
db = mysql.connector.connect(
    host="localhost",
    user="root",
    port=3306,
    password="",
    database="english_tutor",
)
cursor = db.cursor()
