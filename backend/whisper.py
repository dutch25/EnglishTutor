from fastapi import APIRouter, File, UploadFile, Form
import shutil, os, json, subprocess, re, difflib, wave, json as js, requests
from pydub import AudioSegment, effects
from vosk import Model, KaldiRecognizer
from dotenv import load_dotenv

# ====== 🔧 Cấu hình ======
router = APIRouter()
UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
MODEL_PATH = "./models/vosk-en"
ESPEAK_PATH = r"C:\Program Files\eSpeak NG\espeak-ng.exe"

# ====== 🔑 Load API Key GPT ======
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ====== 🚀 Load model Vosk ======
if not os.path.exists(MODEL_PATH):
    raise RuntimeError("❌ Không tìm thấy model Vosk! Giải nén model vào ./models/vosk-en")
vosk_model = Model(MODEL_PATH)

# ====== 🔤 Xử lý IPA ======
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

# ====== 🎧 Xử lý âm thanh ======
def preprocess_audio(input_path, output_path):
    try:
        audio = AudioSegment.from_file(input_path)
        audio = effects.normalize(audio).set_channels(1).set_frame_rate(16000)
        audio.export(output_path, format="wav", codec="pcm_s16le")
        print(f"✅ Đã convert {input_path} → {output_path}, size={os.path.getsize(output_path)} bytes")
    except Exception as e:
        print("❌ Lỗi khi xử lý audio:", e)

def transcribe_audio(file_path):
    clean_path = file_path.replace(".webm", "_clean.wav")
    preprocess_audio(file_path, clean_path)

    if not os.path.exists(clean_path) or os.path.getsize(clean_path) < 1000:
        print("⚠️ File WAV trống hoặc quá nhỏ!")
        return ""

    print(f"🎧 Bắt đầu nhận dạng với Vosk: {clean_path}")
    wf = wave.open(clean_path, "rb")
    rec = KaldiRecognizer(vosk_model, wf.getframerate())
    rec.SetWords(True)

    text = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = js.loads(rec.Result())
            print("👉 Partial:", res.get("text", ""))
            text += " " + res.get("text", "")
    res = js.loads(rec.FinalResult())
    print("👉 Final:", res.get("text", ""))
    text += " " + res.get("text", "")
    wf.close()

    text = text.strip()
    if not text:
        print("⚠️ Không nhận dạng được giọng nói!")
    return text

# ====== 📥 API Upload ======
@router.post("/api/upload/")
async def upload_audio(file: UploadFile = File(...), original_text: str = Form(...)):
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    transcript = transcribe_audio(path)
    if not transcript:
        return {"error": "⚠️ Không nhận dạng được giọng nói!", "transcript": ""}

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

# ====== 📚 API Lấy câu từ JSON ======
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

@router.get("/api/sentences")
def get_sentences(topic: str = None):
    return {"sentences": load_sentences(topic)}

# ====== 📥 API Lấy IPA ======
@router.post("/api/get_ipa")
def api_get_ipa(body: dict):
    return {"ipa": get_ipa(body.get("text", ""))}

# ====== 🤖 API Feedback GPT (phân tích điểm mạnh/điểm yếu) ======
@router.post("/api/feedback")
def feedback(body: dict):
    transcript = body.get("transcript", "")
    target = body.get("target", "")

    if not OPENAI_API_KEY:
        return {"feedback": "⚠️ Không tìm thấy OpenAI API Key."}

    prompt = f"""
Bạn là giáo viên phát âm tiếng Anh cho người Việt. 
Học viên muốn nói: "{target}"
AI nghe được: "{transcript}"

Hãy:
1. ✅ Nêu Điểm mạnh trong phát âm.
2. ❌ Chỉ ra Điểm yếu cụ thể (âm sai, thiếu nhấn, ngữ điệu).
3. 💡 Đưa ra mẹo cải thiện chi tiết.


Phải có 3 mục rõ ràng điểm mạnh, điểm yếu và mẹo cải thiện
Trả lời ngắn gọn, rõ ràng, dễ hiểu và không thêm các dấu ** ở đầu câu.
"""

    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.6,
        "max_tokens": 220
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
        return {"feedback": "⚠️ Không kết nối được AI."}
