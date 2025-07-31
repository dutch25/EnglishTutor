from fastapi import FastAPI
from fastapi import Header
from fastapi.responses import StreamingResponse
from fastapi import FastAPI, HTTPException, Form
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
import requests
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import dns.resolver
import re
from sqlalchemy.orm import Session
from fastapi import Depends 
from database import get_db
from models import User
from datetime import datetime
from schemas import UserRegister
from schemas import UserLogin
import bcrypt
from whisper import router  # Import router từ whisper.py


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)



load_dotenv()



ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = "tnSpp4vdxKPjI9w0GnoV"  # Replace this with your voice ID , jerry voice id: 1t1EeRixsJrKbiF1zwM6 / adam voice s3TPKV1kjDlVtZbl4Ksh
SECRET_KEY = "b7e2c3a4e8f9d1c2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6"  # Đổi thành chuỗi bí mật của bạn
ALGORITHM = "HS256"

# Tạo token truy cập
def create_access_token(data: dict):
    from datetime import timedelta
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

@app.get("/")
def read_root():
    return {"message": "Welcome to the English Tutor API"}

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

db = mysql.connector.connect(
    host="localhost",
    user="root",
    port=3306,
    password="",
    database="english_tutor",
)
cursor = db.cursor()

def is_valid_email(email: str) -> bool:
    # Regex kiểm tra định dạng email hợp lệ
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

def check_email_exists(email: str) -> bool:
    # Kiểm tra domain có tồn tại mail server không (DNS MX record)
    domain = email.split('@')[-1]
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        return True if answers else False
    except Exception:
        return False
    
@app.post("/register")
async def register(user: UserRegister, db: Session = Depends(get_db)):
    if not is_valid_email(user.email):
        raise HTTPException(status_code=400, detail="Email không hợp lệ.")

    if not check_email_exists(user.email):
        raise HTTPException(status_code=400, detail="Email không tồn tại trên hệ thống toàn cầu.")

    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email đã được sử dụng.")
    
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Tên đăng nhập đã tồn tại.")

    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match.")

    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        updated_at=None
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Đăng ký thành công"}

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        (User.username == user.login_input) | (User.email == user.login_input)
    ).first()

    if not existing_user:
        raise HTTPException(status_code=401, detail="Tên đăng nhập hoặc email không tồn tại")

    if not bcrypt.checkpw(user.password.encode('utf-8'), existing_user.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Mật khẩu không chính xác")

    return {
        "message": "Đăng nhập thành công",
        "username": existing_user.username
    }

