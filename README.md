# 🇬🇧 EnglishTutor

**EnglishTutor** là ứng dụng web giúp luyện nghe, học từ vựng, ngữ pháp, câu tiếng Anh, phản xạ giao tiếp và nhiều tính năng hữu ích khác.  
Dành cho mọi đối tượng muốn nâng cao kỹ năng tiếng Anh một cách chủ động, vui vẻ và hiện đại.

---

## 🚀 Tính năng nổi bật

- **Luyện nghe từ vựng** theo chủ đề, kiểm tra và phản hồi tức thì.
- **Học câu tiếng Anh**: Luyện nghe, Luyện nói, phản xạ với các câu giao tiếp thực tế.
- **Động từ bất quy tắc**: tra cứu, nghe phát âm, luyện tập.
- **Ngữ pháp tổng hợp**: các cấu trúc câu thông dụng.
- **Từ điển mini**: tra cứu nhanh.
- **Góp ý & Phản hồi**: gửi ý kiến trực tiếp cho tác giả.
- **ChatBot AI**: trợ lý tiếng Anh, hỏi đáp mọi lúc.
- **Lưu từ vựng yêu thích**.
- **Đăng ký, đăng nhập, quản lý hồ sơ cá nhân**.

---

## 🖥️ Công nghệ sử dụng

- **Frontend:** Vue 3, Vue Router, Vite, SCSS
- **Backend:** FastAPI, SQLAlchemy, MySQL, ElevenLabs API (Text-to-Speech and Speech-to-text), Google Gemini (GenAI), ChatGPT
- **Khác:** JWT Auth, dotenv, CORS, RESTful API

---

## 📦 Cài đặt & chạy thử

### 1. Clone project
```bash
git clone https://github.com/your-username/EnglishTutor.git
cd EnglishTutor
```

### 2. Cài đặt frontend
```bash
cd frontend
npm install
npm run dev
```
Truy cập: [http://localhost:5173](http://localhost:5173)

### 3. Cài đặt backend
```bash
cd ../backend
pip install -r requirements.txt
# Tạo file .env và điền các biến môi trường cần thiết (ví dụ ELEVENLABS_API_KEY, DB_URL, ...)
uvicorn main:app --reload
```
API chạy tại: [http://localhost:8000](http://localhost:8000)

---

## 📂 Cấu trúc thư mục

```
EnglishTutor/
├── frontend/
│   ├── src/
│   │   ├── Auths/         # Đăng nhập, đăng ký, quên mật khẩu
│   │   ├── views/         # Các trang chính: Home, ListeningTest, SentenceTest, Verb, Feedback, ...
│   │   ├── assets/        # Ảnh, icon, data mẫu (json)
│   │   └── router/        # Cấu hình router Vue
│   └── package.json
├── backend/
│   ├── main.py            # FastAPI entrypoint
│   ├── whisper.py         # API Whisper (speech-to-text)
│   ├── auth_routes.py     # Đăng nhập, đăng ký, xác thực
│   ├── ...                # Các router và model khác
│   └── requirements.txt
└── README.md
```

---

## 📝 Đóng góp & phản hồi

- Mọi ý kiến đóng góp, báo lỗi hoặc đề xuất tính năng mới đều rất hoan nghênh!
- Gửi phản hồi trực tiếp tại trang "Góp ý & Phản hồi" trong app hoặc tạo issue trên GitHub.

---

## 📜 License

MIT License © 2024 [By Nhóm 7]

---

**Chúc bạn học tiếng Anh hiệu quả cùng EnglishTutor!**
