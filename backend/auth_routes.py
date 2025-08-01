from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserRegister, UserLogin
from datetime import datetime
import bcrypt, re, dns.resolver

router = APIRouter()

# ✅ Check email hợp lệ
def is_valid_email(email: str) -> bool:
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)

# ✅ Check domain email có MX record
def check_email_exists(email: str) -> bool:
    domain = email.split('@')[-1]
    try:
        dns.resolver.resolve(domain, 'MX')
        return True
    except:
        return False

# ✅ API Đăng ký
@router.post("/register")
async def register(user: UserRegister, db: Session = Depends(get_db)):
    if not is_valid_email(user.email):
        raise HTTPException(status_code=400, detail="Email không hợp lệ.")
    if not check_email_exists(user.email):
        raise HTTPException(status_code=400, detail="Email không tồn tại.")
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email đã được sử dụng.")
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Tên đăng nhập đã tồn tại.")
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match.")

    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()
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

# ✅ API Đăng nhập
@router.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        (User.username == user.login_input) | (User.email == user.login_input)
    ).first()

    if not existing_user:
        raise HTTPException(status_code=401, detail="Tên đăng nhập hoặc email không tồn tại")
    if not bcrypt.checkpw(user.password.encode(), existing_user.password.encode()):
        raise HTTPException(status_code=401, detail="Mật khẩu không chính xác")

    return {"message": "Đăng nhập thành công", "username": existing_user.username}
