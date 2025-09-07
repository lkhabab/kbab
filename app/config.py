import os
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_DIR   = os.path.join(BASE_DIR, "instance")
os.makedirs(DB_DIR, exist_ok=True)  # تأكد المجلد موجود
DB_PATH  = os.path.join(DB_DIR, "app.db")

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
