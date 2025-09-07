from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from ..extensions import db, login_manager
from ..forms import LoginForm, RegisterForm, ProfileForm
from ..models import User

bp = Blueprint("auth", __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash("تم تسجيل الدخول.", "success")
            return redirect(request.args.get("next") or url_for("main.home"))
        flash("بيانات الدخول غير صحيحة", "danger")
    return render_template("auth/login.html", form=form)

@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash("اسم المستخدم موجود", "warning")
        else:
            u = User(
                name=form.name.data,
                farm_location=form.farm_location.data,
                contact_details=form.contact_details.data,
                username=form.username.data,
                email=form.email.data or None,
            )
            u.set_password(form.password.data)
            db.session.add(u)
            db.session.commit()
            flash("تم إنشاء الحساب. سجّل دخولك.", "success")
            return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)

@bp.get("/logout")
@login_required
def logout():
    logout_user()
    flash("تم تسجيل الخروج.", "info")
    return redirect(url_for("main.home"))
