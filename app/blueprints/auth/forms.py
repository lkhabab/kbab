# app/blueprints/auth/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, NumberRange


class LoginForm(FlaskForm):
    username = StringField("اسم المستخدم", validators=[DataRequired(), Length(min=3, max=120)])
    password = PasswordField("كلمة المرور", validators=[DataRequired()])
    remember = BooleanField("تذكرني")
    submit = SubmitField("دخول")


class RegisterForm(FlaskForm):
    name = StringField("الاسم الكامل", validators=[DataRequired(), Length(max=100)])
    date_of_birth = DateField("تاريخ الميلاد", format="%Y-%m-%d", validators=[DataRequired()])
    farm_location = StringField("موقع المزرعة", validators=[Optional(), Length(max=150)])
    contact_details = StringField("وسيلة الاتصال", validators=[Optional(), Length(max=100)])
    username = StringField("اسم المستخدم", validators=[DataRequired(), Length(min=3, max=120)])
    email = StringField("البريد", validators=[Optional(), Email(), Length(max=200)])
    password = PasswordField("كلمة المرور", validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField("تأكيد كلمة المرور", validators=[DataRequired(), EqualTo("password", message="التأكيد غير مطابق")])
    submit = SubmitField("تسجيل")
