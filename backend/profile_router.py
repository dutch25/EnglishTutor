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
