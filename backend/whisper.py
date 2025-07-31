from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil, os, json, subprocess, requests, difflib, re
from pydub import AudioSegment, effects
from dotenv import load_dotenv

# 📥 Load API Key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("❌ Thiếu OPENAI_API_KEY trong .env")

# 🚀 Init App
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ESPEAK_PATH = r"C:\Program Files\eSpeak NG\espeak-ng.exe"

# ======== 🔤 XỬ LÝ IPA ========
def get_ipa(text: str) -> str:
    if not text.strip():
        return ""
    try:
        res = subprocess.run([ESPEAK_PATH, "-v", "en", "-q", "--ipa=3", text],
                             capture_output=True, text=True, encoding="utf-8", check=True)
        return res.stdout.strip()
    except Exception as e:
        print("❌ Lỗi IPA:", e)
        return ""

def split_ipa(ipa: str): 
    return re.findall(r"[ˈˌ]?[a-zɑɔæəɪʊeʌθðŋʃʒʔɡɾ̃ː]+|[.,!?;]", ipa.strip())

def compare_ipa_colored(target_ipa: str, user_ipa: str):
    matcher = difflib.SequenceMatcher(None, split_ipa(target_ipa), split_ipa(user_ipa))
    html = ""
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            html += ''.join(f'<span style="color:green">{p}</span>' for p in split_ipa(user_ipa)[j1:j2])
        elif tag in ("replace", "insert"):
            html += ''.join(f'<span style="color:red;text-decoration:underline">{p}</span>' for p in split_ipa(user_ipa)[j1:j2])
        elif tag == "delete":
            html += ''.join(f'<span style="background:yellow">{p}</span>' for p in split_ipa(target_ipa)[i1:i2])
    return round(matcher.ratio() * 100), html

def compare_text_colored(original, spoken):
    res = ""
    max_len = max(len(original), len(spoken))
    for i in range(max_len):
        o = original[i] if i < len(original) else " "
        s = spoken[i] if i < len(spoken) else " "
        res += f'<span style="color:{"green" if o == s else "red"}">{o}</span>'
    return res

# ======== 🔊 XỬ LÝ ÂM THANH ========
def preprocess_audio(input_path, output_path):
    audio = AudioSegment.from_file(input_path)
    audio = effects.normalize(audio).set_channels(1).set_frame_rate(16000)
    audio.export(output_path, format="wav")

def transcribe_audio(file_path):
    clean_path = file_path.replace(".webm", "_clean.wav")
    preprocess_audio(file_path, clean_path)

    url = "https://api.openai.com/v1/audio/transcriptions"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    with open(clean_path, "rb") as f:
        files = {"file": (os.path.basename(clean_path), f, "audio/wav")}
        data = {"model": "whisper-1", "language": "en"}
        res = requests.post(url, headers=headers, files=files, data=data)

    return res.json().get("text", "").strip() if res.status_code == 200 else ""

# ======== 📥 API UPLOAD ========
@app.post("/api/upload/")
async def upload_audio(file: UploadFile = File(...), original_text: str = Form(...)):
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    transcript = transcribe_audio(path)
    original_ipa = get_ipa(original_text)
    user_ipa = get_ipa(transcript)
    ipa_score, ipa_html = compare_ipa_colored(original_ipa, user_ipa)

    return {
        "transcript": transcript,
        "original_ipa": original_ipa,
        "user_ipa_raw": user_ipa,
        "user_ipa_colored": ipa_html,
        "sentence_colored": compare_text_colored(original_text, transcript),
        "ipa_score": ipa_score
    }

# ======== 📚 API LẤY CÂU TỪ JSON ========
JSON_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../frontend/src/assets/data/conversations.json")
)

def load_sentences(topic: str = None):
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    result = []
    for key, value in data.items():
        if topic and key.lower() != topic.lower():
            continue
        for s in value["sentences"]:
            result.append({
                "topic": key,
                "icon": value.get("icon", ""),
                "english": s.get("english", ""),
                "vietnamese": s.get("vietnamese", ""),
                "pronunciation": s.get("pronunciation", "")
            })
    return result

@app.get("/api/sentences")
def get_sentences(topic: str = None):
    return {"sentences": load_sentences(topic)}

# ======== 📥 API LẤY IPA ========
@app.post("/api/get_ipa")
def api_get_ipa(body: dict):
    return {"ipa": get_ipa(body.get("text", ""))}

# ======== 🧠 API NHẬN XÉT GPT ========
@app.post("/api/feedback")
def feedback(body: dict):
    transcript = body.get("transcript", "")
    target = body.get("target", "")

    prompt = f"""Bạn là giáo viên tiếng Anh cho người Việt. 
Học viên muốn nói: "{target}" 
AI nghe được: "{transcript}" 

Hãy trả lời NGẮN GỌN, dễ hiểu với cấu trúc:
🌟 Nhận xét chung
❌ Từ sai → ✅ Cách nói đúng
💡 Mẹo luyện tập
🔥 Câu khích lệ"""

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.6,
        "max_tokens": 180
    }

    try:
        res = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=15)
        if res.status_code == 200:
            data = res.json()
            return {"feedback": data.get("choices", [{}])[0].get("message", {}).get("content", "⚠️ Không có phản hồi.")}
        else:
            print("❌ GPT API lỗi:", res.text)
            return {"feedback": "⚠️ AI không trả lời, thử lại sau."}
    except Exception as e:
        print("❌ Lỗi gọi GPT API:", e)
        return {"feedback": "⚠️ Không kết nối được đến AI, thử lại sau."}