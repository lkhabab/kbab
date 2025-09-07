from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user
from urllib.parse import urlparse

from . import bp
from .forms import LoginForm, RegisterForm
from ...models import User
from ...extensions import db


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = LoginForm()
    if form.validate_on_submit():
        username = (form.username.data or "").strip().lower()
        user = User.query.filter_by(username=username).first()

        if user is None:
            flash("اسم المستخدم غير موجود.", "danger")
            return render_template("auth/login.html", form=form)

        if not user.check_password(form.password.data):
            flash("كلمة المرور غير صحيحة.", "danger")
            return render_template("auth/login.html", form=form)

        login_user(user, remember=form.remember.data)

        # next آمن فقط داخل نفس الدومين
        next_page = request.args.get("next")
        parsed = urlparse(next_page) if next_page else None
        if not parsed or parsed.netloc:
            next_page = url_for("main.home")

        return redirect(next_page)

    return render_template("auth/login.html", form=form)


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = RegisterForm()
    if form.validate_on_submit():
        username = (form.username.data or "").strip().lower()
        email = (form.email.data or "").strip().lower() if form.email.data else None

        # تحقق من التكرار
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


# ===== صفحات العرض 3D (GET فقط) =====
@bp.route("/login-3d", methods=["GET"])
def login_3d():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    return render_template("auth/login_3d.html", form=form)


@bp.route("/register-3d", methods=["GET"])
def register_3d():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegisterForm()
    return render_template("auth/register_3d.html", form=form)


# تسجيل الخروج
@bp.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash("تم تسجيل الخروج.", "success")
    return redirect(url_for("main.home"))
