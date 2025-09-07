from datetime import date
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..extensions import db
from ..forms import AssessmentForm, WeatherForm, YieldForm, ProfileForm
from ..models import Assessment, WeatherData, YieldEstimate, User

bp = Blueprint("main", __name__)

@bp.get("/")
def home():
    return render_template("main/home.html")

# i. Home (already above) -> login/register links through navbar

# ii. Crop Health Assessment
@bp.route("/assess", methods=["GET", "POST"])
@login_required
def assess():
    form = AssessmentForm()
    result = None
    if form.validate_on_submit():
        # naive rule-based mapping as placeholder for AI
        mapping = {
            "leaf_yellowing": ("نقص نيتروجين محتمل", "أضف تسميد N متوازن وتحقق من الري."),
            "wilting": ("إجهاد مائي", "افحص الرطوبة؛ ري منتظم وتغطية التربة بالملش."),
            "spots": ("بقعة فطرية محتملة", "أزل الأوراق المصابة وحسّن التهوية."),
            "stunted": ("نقص عناصر/تربة فقيرة", "اختبار تربة وتسميد عضوي تدريجي."),
            "pests": ("نشاط آفات", "مصائد لاصقة، مراقبة صباحية، واستشارة قبل رش مبيد.")
        }
        diag, rec = mapping.get(form.symptom_selected.data, ("غير محدد", "أرسل صورة أوراق للمزيد من الدقة."))
        # trivial confidence estimate
        conf = 0.6 if form.symptom_selected.data in mapping else 0.3
        assess = Assessment(
            user_id=current_user.id,
            symptom_selected=form.symptom_selected.data,
            diagnosis=diag,
            recommendation=rec,
            soil_moisture_level=form.soil_moisture_level.data or 0.0,
            confidence_score=conf
        )
        db.session.add(assess)
        db.session.commit()
        result = assess
        flash("تم إنشاء تقرير تشخيص مبدئي.", "success")
    return render_template("main/assess.html", form=form, result=result)

# iii. Weather & Seasonality
@bp.route("/weather", methods=["GET", "POST"])
@login_required
def weather():
    form = WeatherForm()
    return render_template("main/weather.html", form=form)

# iv. Yield Estimation
@bp.route("/yield", methods=["GET", "POST"])
@login_required
def yield_page():
    form = YieldForm()
    result = None
    if form.validate_on_submit():
        # simple baseline model
        # base_yield per hectare (rough placeholder), adjust by planting month proximity to July (rainfed example)
        base = 1.0  # ton/ha baseline
        month = form.planting_date.data.month
        seasonal_bonus = 1.2 if month in (6,7,8) else 0.9
        est = round(base * seasonal_bonus * (form.field_area.data or 1.0), 2)
        y = YieldEstimate(
            user_id=current_user.id,
            crop_type=form.crop_type.data,
            estimated_yield=est,
            field_area=form.field_area.data
        )
        db.session.add(y)
        db.session.commit()
        result = y
        flash("تم حساب إنتاجية مبدئية.", "success")
    return render_template("main/yield.html", form=form, result=result)

# v. Chat Assistance
@bp.get("/assistant")
@login_required
def assistant():
    return render_template("main/assistant.html")

# vi. User Profile
@bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    u = current_user
    form = ProfileForm(obj=u)
    if form.validate_on_submit():
        u.name = form.name.data
        u.farm_location = form.farm_location.data
        u.contact_details = form.contact_details.data
        u.email = form.email.data
        db.session.commit()
        flash("تم حفظ الملف الشخصي.", "success")
        return redirect(url_for("main.profile"))
    return render_template("main/profile.html", form=form)

# vii. About Us
@bp.get("/about")
def about():
    return render_template("main/about.html")
