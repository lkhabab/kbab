# init_db.py
from wsgi import app
from app.extensions import db
from pathlib import Path

with app.app_context():
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    db.create_all()
    print("DB READY ->", app.config.get("SQLALCHEMY_DATABASE_URI"))
