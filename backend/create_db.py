from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    created_at = Column(String(50), nullable=True)
    updated_at = Column(String(50), nullable=True)
    phone = Column(String(20), nullable=True)
    description = Column(String(255), nullable=True)

class Saved(Base):
    __tablename__ = "saved"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    word = Column(String(100), nullable=False)
    meaning = Column(String(255), nullable=True)      # Thêm trường nghĩa
    phonetic = Column(String(100), nullable=True)     # Thêm trường phiên âm
    note = Column(String(255), nullable=True)
    created_at = Column(String(50), nullable=True)

    user = relationship("User", backref="saved_words")

engine = create_engine("mysql+pymysql://root@localhost/english_tutor")

print("Tạo bảng...")
Base.metadata.create_all(bind=engine)
print("Hoàn tất.")
