# app/models.py
from .extensions import db
from flask_login import UserMixin
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash

# ----- Users -----
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    farm_location = db.Column(db.String(150))
    contact_details = db.Column(db.String(100))

    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True)

    # جديد: تاريخ الميلاد (إجباري)
    date_of_birth = db.Column(db.Date, nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)

    # helper: العمر بالحساب
    @property
    def age(self) -> int:
        if not self.date_of_birth:
            return 0
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

# ----- Assessments (Crop Health) -----
class Assessment(db.Model):
    __tablename__ = "assessments"

    id = db.Column("assessment_id", db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    symptom_selected = db.Column(db.String(50))
    diagnosis = db.Column(db.String(100))
    recommendation = db.Column(db.Text)
    soil_moisture_level = db.Column(db.Float)
    confidence_score = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# ----- Weather Data -----
class WeatherData(db.Model):
    __tablename__ = "weatherdata"

    id = db.Column("weather_id", db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    date = db.Column(db.Date)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    rainfall = db.Column(db.Float)
    wind_speed = db.Column(db.Float)
    data_source = db.Column(db.String(50), default="OpenWeatherMap API")

# ----- Yield Estimates -----
class YieldEstimate(db.Model):
    __tablename__ = "yieldestimates"

    id = db.Column("estimate_id", db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    crop_type = db.Column(db.String(50))
    estimated_yield = db.Column(db.Float)
    field_area = db.Column(db.Float)  # hectares
    # النوع Date فالأفضل نخلي default = date.today بدل datetime.utcnow
    estimation_date = db.Column(db.Date, default=date.today)
    model_version = db.Column(db.String(20), default="v1.0")

# ----- Chat Sessions -----
class ChatSession(db.Model):
    __tablename__ = "chatsessions"

    id = db.Column("session_id", db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    transcript = db.Column(db.Text)
    detected_intent = db.Column(db.String(50))

# ----- Guidance Content -----
class GuidanceContent(db.Model):
    __tablename__ = "guidancecontent"

    id = db.Column("content_id", db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    content_type = db.Column(db.String(20))    # Text, Video
    content_path = db.Column(db.String(255))   # URL/path
    version = db.Column(db.String(10), default="1.0")
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

# ----- Simple seed helper (اختياري) -----
def seed_admin(db):
    # ما في داعي لإعادة الاستيراد من نفس الملف
    if not User.query.filter_by(username="admin").first():
        u = User(
            username="admin",
            name="Administrator",
            email="admin@example.com",
            is_admin=True,
            date_of_birth=date(1990, 1, 1),  # تاريخ افتراضي علشان القيود الجديدة
        )
        u.set_password("admin123")
        db.session.add(u)
        db.session.commit()
