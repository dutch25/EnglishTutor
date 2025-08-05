import os
from dotenv import load_dotenv
import requests
from fastapi import APIRouter, Body

load_dotenv()
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

router = APIRouter()


def send_feedback_to_discord(content, user="Ẩn danh"):
    print("Gửi feedback tới Discord:", content, "user:", user)
    if not DISCORD_WEBHOOK_URL:
        print("Không tìm thấy webhook URL")
        return
    message = f"**Từ người dùng \"{user}\":** {content}"
    try:
        resp = requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
        print("Discord response:", resp.status_code, resp.text)
    except Exception as e:
        print("Lỗi gửi tới Discord:", e)


@router.post("/api/feedback_discord")
def feedback_api(
    content: str = Body(..., embed=True),
    user: str = Body("Ẩn danh", embed=True),
):
    print("Đã nhận request feedback:", content, user)
    send_feedback_to_discord(content, user)
    return {"message": "Đã gửi feedback!"}