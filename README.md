# AI-Powered Agricultural Assistant (Flask)

سبعة صفحات أساسية:
- الرئيسية `/`
- تشخيص صحي `/assess` (نموذج أعراض + توصية مبدئية)
- الطقس `/weather` (تكامل OpenWeatherMap – يحتاج OWM_API_KEY)
- تقدير الإنتاجية `/yield` (نموذج مبسط قابل للتطوير)
- مساعد محادثة `/assistant` (قواعد بسيطة قابلة للاستبدال بنموذج ذكي)
- الملف الشخصي `/profile`
- تعريف `/about`

## التشغيل
```bash
cd agri_assistant_flask
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# عدّل OWM_API_KEY وقاعدة البيانات إذا رغبت
python
>>> from app import create_app
>>> from app.extensions import db
>>> from app.models import seed_admin
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
...     seed_admin(db)
... 
exit()

python run.py
# http://127.0.0.1:5000/
```

## ملاحظات
- الصفحة `/api/weather` تُستدعى من واجهة الطقس؛ عيّن متغير البيئة `OWM_API_KEY`.
- استبدل قواعد التشخيص البسيطة بنموذج ML لاحقًا (TensorFlow/PyTorch).
- طبّق التحقق وCSRF (مفعّل عبر Flask-WTF)؛ وللاستخدام العام فعّل HTTPS وتكوين الإنتاج (gunicorn/nginx).
