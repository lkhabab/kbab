# Replace /weather with Planting Calendar (Arabic)

انسخ الملفات في مشروعك حسب نفس المسارات:

- app/blueprints/weather.py        ← يستبدل صفحة الطقس
- app/templates/main/weather.html  ← واجهة التقويم
- app/static/css/calendar.css
- app/static/js/calendar_regions.js
- README.txt

## 1) تسجيل البلوبرنت
افتح `app/__init__.py` وأضف (أو بدّل القديم):
from .blueprints.weather import bp as weather_bp
app.register_blueprint(weather_bp)

## 2) افتح الصفحة
http://127.0.0.1:5000/weather

## 3) ملاحظة
الصفحة تستخدم Bootstrap 5 للمودال. لو ما عندك Bootstrap في base.html راسلني أرسل مودال Vanilla JS.
