from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
import mysql.connector
import bcrypt
import re


router = APIRouter()

class UserUpdate(BaseModel):
    old_username: str  # Thêm old_username để biết người dùng gốc là ai
    username: str
    email: str
    phone: str
    description: str    

class PasswordUpdate(BaseModel):
    username: str
    old_password: str
    new_password: str

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="english_tutor",
        port=3306,
    )

@router.get("/api/user/{username}")
async def get_user(username: str):
    connection = get_db_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT username, email, phone, description FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except mysql.connector.Error as e:
        print(f"Error fetching user: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        cursor.close()
        connection.close()

@router.put("/api/user/update-profile")
async def update_profile(data: UserUpdate):
    connection = get_db_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (data.old_username,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not re.match(r"[^@]+@[^@]+\.[^@]+", data.email):
            raise HTTPException(status_code=400, detail="Invalid email format")

        cursor.execute("SELECT username FROM users WHERE email = %s AND username != %s", (data.email, data.old_username))
        email_conflict = cursor.fetchone()
        if email_conflict:
            raise HTTPException(status_code=400, detail="Email is already in use by another account")

        # Nếu username muốn đổi khác với old_username, kiểm tra trùng
        if data.username != data.old_username:
            cursor.execute("SELECT username FROM users WHERE username = %s", (data.username,))
            username_conflict = cursor.fetchone()
            if username_conflict:
                raise HTTPException(status_code=400, detail="Username already exists")

        # Kiểm tra dữ liệu có gì thay đổi không (so sánh với DB)
        if (data.username == user['username'] and
            data.email == user['email'] and
            data.phone == user['phone'] and
            data.description == (user['description'] or "")):  # tránh None
            return {"message": "No changes were made, data remains the same"}

        # Thực hiện update
        cursor.execute("""
            UPDATE users 
            SET username = %s, email = %s, phone = %s, description = %s 
            WHERE username = %s
        """, (data.username, data.email, data.phone, data.description, data.old_username))
        connection.commit()
        print("Rows affected:", cursor.rowcount)


        return {"message": "Profile updated successfully"}

    except mysql.connector.Error as e:
        print(f"Error updating profile: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        cursor.close()
        connection.close()

@router.put("/api/user/change-password")
async def change_password(data: PasswordUpdate):
    connection = get_db_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT password FROM users WHERE username = %s", (data.username,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Kiểm tra mật khẩu cũ
        stored_password = user['password'].encode()
        if not bcrypt.checkpw(data.old_password.encode(), stored_password):
            raise HTTPException(status_code=400, detail="Mật khẩu cũ không chính xác.")

        # Kiểm tra độ mạnh mật khẩu mới (tùy chọn, giống đăng ký)
        if len(data.new_password) < 8 or not re.search(r"[A-Z]", data.new_password) or not re.search(r"[!@#$%^&*(),.?\":{}|<>]", data.new_password):
            raise HTTPException(status_code=400, detail="Mật khẩu mới phải có ít nhất 8 ký tự, 1 chữ in hoa và 1 ký tự đặc biệt.")

        # Hash mật khẩu mới và cập nhật
        hashed_new_password = bcrypt.hashpw(data.new_password.encode(), bcrypt.gensalt()).decode()
        cursor.execute("UPDATE users SET password = %s WHERE username = %s", (hashed_new_password, data.username))
        connection.commit()
        print("Password updated for:", data.username)

        return {"message": "Đổi mật khẩu thành công"}

    except mysql.connector.Error as e:
        print(f"Error changing password: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        cursor.close()
        connection.close()
