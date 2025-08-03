from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from create_db import Saved, Base, engine
from pydantic import BaseModel
from datetime import datetime

# ====== 🔧 Cấu hình ======
router = APIRouter()

class SaveWordRequest(BaseModel):
    user_id: int
    word: str
    meaning: str = ""
    phonetic: str = ""
    note: str = ""

# ====== 📥 API Lưu từ ======
@router.post("/api/save_word")
async def save_word(data: SaveWordRequest, db: Session = Depends(get_db)):
    saved = Saved(
        user_id=data.user_id,
        word=data.word,
        meaning=data.meaning,
        phonetic=data.phonetic,
        note=data.note,
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
    db.add(saved)
    db.commit()
    db.refresh(saved)
    return {"message": "Đã lưu từ", "id": saved.id}

# ====== 📚 API Lấy danh sách từ đã lưu ======
@router.get("/api/saved_words")
def get_saved_words(user_id: int = Query(...), db: Session = Depends(get_db)):
    words = db.query(Saved).filter_by(user_id=user_id).order_by(Saved.id.desc()).all()
    return [
        {
            "id": w.id,
            "word": w.word,
            "meaning": w.meaning,
            "phonetic": w.phonetic,
            "note": w.note,
            "created_at": w.created_at
        }
        for w in words
    ]

# ====== 🗑️ API Xoá từ đã lưu ======
@router.delete("/api/saved_word/{id}")
def delete_saved_word(id: int, db: Session = Depends(get_db)):
    word = db.query(Saved).filter_by(id=id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Không tìm thấy")
    db.delete(word)
    db.commit()
    return {"message": "Đã xoá"}