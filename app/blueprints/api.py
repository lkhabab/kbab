# app/blueprints/api.py
import os, requests, re, time
from flask import Blueprint, jsonify, request, current_app
from ..models import GuidanceContent  # لو ما تحتاجه تقدر تشيله
from ..extensions import csrf         # لعمل إعفاء على مسارات الـAJAX

bp = Blueprint("api", __name__)

# ---------- Utilities ----------
AR_DIAC    = re.compile(r'[\u0617-\u061A\u064B-\u0652]')
AR_TATWEEL = re.compile(r'[\u0640]')
AR_PUNC    = re.compile(r'[^\w\s\u0600-\u06FF]')

def norm_ar(t: str) -> str:
    if not t:
        return ""
    t = t.strip().lower()
    t = AR_DIAC.sub('', t)
    t = AR_TATWEEL.sub('', t)
    t = t.replace('أ','ا').replace('إ','ا').replace('آ','ا')
    t = t.replace('ى','ي').replace('ئ','ي').replace('ؤ','و')
    t = AR_PUNC.sub(' ', t)
    return re.sub(r'\s+',' ', t)

# ---------- Weather ----------
@bp.get("/weather")
@csrf.exempt  # GET عادةً ما يحتاج CSRF، بس نخليها معفاة احتياطاً
def weather():
    key = current_app.config.get("OWM_API_KEY") or os.getenv("OWM_API_KEY", "")
    city = (request.args.get("city") or "").strip()
    lat  = (request.args.get("lat")  or "").strip()
    lon  = (request.args.get("lon")  or "").strip()

    if not key:
        return jsonify(ok=False, error="Missing OWM_API_KEY"), 400

    if city:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={key}&units=metric&lang=ar"
    elif lat and lon:
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={key}&units=metric&lang=ar"
    else:
        return jsonify(ok=False, error="Provide ?city=Khartoum أو ?lat=..&lon=.."), 400

    try:
        r = requests.get(url, timeout=12)
        r.raise_for_status()
        data = r.json()
        if "list" not in data:
            return jsonify(ok=False, error=data), 400

        # أول 8 قيود ≈ 24 ساعة
        out = [{
            "dt": it.get("dt"),
            "time": it.get("dt_txt"),
            "temp": it.get("main", {}).get("temp"),
            "feels": it.get("main", {}).get("feels_like"),
            "hum": it.get("main", {}).get("humidity"),
            "wind": it.get("wind", {}).get("speed"),
            "desc": (it.get("weather") or [{}])[0].get("description")
        } for it in data["list"][:8]]

        return jsonify(ok=True, city=data.get("city", {}), forecast=out)
    except requests.RequestException as e:
        return jsonify(ok=False, error=f"network: {e}"), 502
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500

# ---------- Chat (rule-based) ----------
@bp.post("/chat")
@csrf.exempt  # مهم لو مفعّل CSRF-WTF — الواجهة ترسل JSON مش فورم
def chat():
    try:
        payload = request.get_json(silent=True) or {}
        text_raw = (payload.get("text") or "").strip()
        if not text_raw:
            return jsonify(ok=False, reply="اكتب سؤالك"), 400

        # تأخير صناعي لمحاكاة الكتابة (بين 5 و 10 ثواني)
        time.sleep(7)

        text = norm_ar(text_raw)

        rules = [
            # ري
            (["ري","ارو","سقاية","moyah","water","irrig"], 
             "الري: اسقِ صباحًا/مساءً، وراقب رطوبة التربة (عمق 5–7 سم). الدُفعات الخفيفة أفضل من الغمر الثقيل."),
            # تسميد
            (["تسميد","سماد","npk","fert"], 
             "قسّم التسميد إلى دفعات صغيرة متوازنة (NPK) بعد الري وليس قبله. أرسل المساحة والعمر لنحسب جرعة تقريبية."),
            # آفات/أمراض
            (["افة","حشرة","thrips","aphid","من","فطر","عفن","صدأ","لفحة"], 
             "اعزل المصاب وحسّن التهوية ونظّف البقايا. حدّد النوع بدقة قبل أي مبيد (صورة واضحة تفيد)."),
            # طقس
            (["طقس","مطر","weather"], 
             "تفاصيل الطقس المحلي متاحة في صفحة الطقس (24 ساعة القادمة).")
        ]

        for keys, ans in rules:
            if any(k in text for k in keys):
                return jsonify(ok=True, reply=ans)

        # (اختياري) جلب إرشادات من DB
        # rec = GuidanceContent.query.filter(GuidanceContent.content.ilike(f"%{text_raw[:20]}%")).first()
        # if rec:
        #     return jsonify(ok=True, reply=rec.content)

        fallback = "أرسل وصفًا مختصرًا للمشكلة: المحصول + العَرَض + آخر ري/تسميد، وسأقترح خطوات أولية."
        return jsonify(ok=True, reply=fallback)

    except Exception as e:
        return jsonify(ok=False, reply=f"خطأ غير متوقع: {e}"), 500
