# app/blueprints/auth/routes.py
from flask import render_template, redirect, url_for, flash, request, current_app, send_from_directory
from flask_login import current_user, login_user, logout_user
from urllib.parse import urlparse
import os

from . import bp
from .forms import LoginForm, RegisterForm
from ...models import User
from ...extensions import db


# ---------- Helpers ----------
def _is_safe_next(next_url: str) -> bool:
    """يسمح بإعادة التوجيه فقط داخل نفس الدومين (مسار نسبي)."""
    if not next_url:
        return False
    p = urlparse(next_url)
    return p.netloc == ""  # يعني /path فقط

def _agri3d_dist_dir() -> str:
    """مجلد توزيع الواجهة المبنية بـ Vite: app/static/agri3d/"""
    return os.path.join(current_app.static_folder, "agri3d")


# ---------- Auth: Login ----------
@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = LoginForm()
    if form.validate_on_submit():
        username = (form.username.data or "").strip().lower()
        user = User.query.filter_by(username=username).first()

        if not user:
            flash("اسم المستخدم غير موجود.", "danger")
            return render_template("auth/login.html", form=form)

        if not user.check_password(form.password.data):
            flash("كلمة المرور غير صحيحة.", "danger")
            return render_template("auth/login.html", form=form)

        login_user(user, remember=form.remember.data)

        next_url = request.args.get("next")
        if not _is_safe_next(next_url):
            next_url = url_for("main.home")
        return redirect(next_url)

    return render_template("auth/login.html", form=form)


# ---------- Auth: Register ----------
@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = RegisterForm()
    if form.validate_on_submit():
        username = (form.username.data or "").strip().lower()
        email = (form.email.data or "").strip().lower() if form.email.data else None

        # تحققات التكرار
        if User.query.filter_by(username=username).first():
            flash("اسم المستخدم مستخدم من قبل.", "danger")
            return render_template("auth/register.html", form=form)

        if email and User.query.filter_by(email=email).first():
            flash("البريد مستخدم من قبل.", "danger")
            return render_template("auth/register.html", form=form)

        # إنشاء المستخدم
        u = User(
            name=(form.name.data or "").strip(),
            username=username,
            email=email,
            farm_location=form.farm_location.data or "",
            contact_details=form.contact_details.data or "",
            date_of_birth=form.date_of_birth.data,
        )
        u.set_password(form.password.data)
        db.session.add(u)
        db.session.commit()

        flash("تم إنشاء الحساب بنجاح. يمكنك تسجيل الدخول الآن.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


# ---------- 3D Login (Vite build أو dev) ----------
@bp.route("/login-3d", methods=["GET"])
def login_3d():
    """
    - إنتاج: يخدم app/static/agri3d/index.html (ناتج Vite).
    - تطوير (debug=True): يحوّل تلقائياً إلى Vite dev server على 5173.
    - فولباك: يرجّع قالب Jinja بسيط لو ما فيه build ولا dev.
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    dist_dir = _agri3d_dist_dir()
    index_file = os.path.join(dist_dir, "index.html")

    # إنتاج: قدّم ملف البناء إن وجد
    if os.path.exists(index_file):
        return send_from_directory(dist_dir, "index.html")

    # تطوير: حول لـ Vite dev server
    if current_app.debug:
        return redirect("http://localhost:5173/")

    # فولباك (لو ما فيه build ولا dev)
    form = LoginForm()
    return render_template("auth/login_3d.html", form=form)


# ---------- Logout ----------
@bp.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash("تم تسجيل الخروج.", "success")
    return redirect(url_for("main.home"))
