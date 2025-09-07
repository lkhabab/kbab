from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, BooleanField, SubmitField,
    FloatField, IntegerField, TextAreaField, SelectField, DateField
)
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, NumberRange


# ------------------ Auth ------------------

class LoginForm(FlaskForm):
    username = StringField("اسم المستخدم", validators=[DataRequired(), Length(min=3, max=120)])
    password = PasswordField("كلمة المرور", validators=[DataRequired()])
    remember = BooleanField("تذكرني")
    submit = SubmitField("دخول")


class RegisterForm(FlaskForm):
    # ملاحظة: في التمبلت استخدم {{ form.name }} بدل full_name
    name = StringField("الاسم الكامل", validators=[DataRequired(), Length(max=100)])
    date_of_birth = DateField(
        "تاريخ الميلاد", format="%Y-%m-%d",
        validators=[DataRequired(message="تاريخ الميلاد مطلوب (YYYY-MM-DD)")]
    )
    farm_location = StringField("موقع المزرعة", validators=[Optional(), Length(max=150)])
    contact_details = StringField("وسيلة الاتصال", validators=[Optional(), Length(max=100)])
    username = StringField("اسم المستخدم", validators=[DataRequired(), Length(min=3, max=120)])
    email = StringField("البريد", validators=[Optional(), Email(), Length(max=200)])
    password = PasswordField("كلمة المرور", validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField("تأكيد كلمة المرور", validators=[DataRequired(), EqualTo("password", message="التأكيد غير مطابق")])
    submit = SubmitField("تسجيل")


# ------------------ App Forms ------------------

class AssessmentForm(FlaskForm):
    symptom_selected = SelectField(
        "العَرَض",
        choices=[
            ("leaf_yellowing", "اصفرار الأوراق"),
            ("wilting", "ذبول"),
            ("spots", "بقع على الأوراق"),
            ("stunted", "تقزم"),
            ("pests", "آفات/حشرات")
        ],
        validators=[DataRequired()]
    )
    soil_moisture_level = FloatField(
        "رطوبة التربة (%)",
        validators=[Optional(), NumberRange(min=0, max=100, message="النسبة بين 0 و 100")]
    )
    notes = TextAreaField("ملاحظات", validators=[Optional(), Length(max=500)])
    submit = SubmitField("تشخيص مبدئي")


class WeatherForm(FlaskForm):
    city = StringField("المدينة", validators=[Optional(), Length(max=80)])
    lat = FloatField("Latitude", validators=[Optional(), NumberRange(min=-90, max=90)])
    lon = FloatField("Longitude", validators=[Optional(), NumberRange(min=-180, max=180)])
    submit = SubmitField("عرض الطقس")


class YieldForm(FlaskForm):
    crop_type = StringField("المحصول", validators=[DataRequired(), Length(max=50)])
    planting_date = DateField("تاريخ الزراعة", format="%Y-%m-%d", validators=[DataRequired()])
    field_area = FloatField("المساحة (هكتار)", validators=[DataRequired(), NumberRange(min=0.01, message="أدخل قيمة أكبر من صفر")])
    variety = StringField("الصنف", validators=[Optional(), Length(max=50)])
    submit = SubmitField("احسب الإنتاجية")


class ProfileForm(FlaskForm):
    name = StringField("الاسم الكامل", validators=[DataRequired(), Length(max=100)])
    date_of_birth = DateField("تاريخ الميلاد", format="%Y-%m-%d", validators=[DataRequired()])
    farm_location = StringField("موقع المزرعة", validators=[Optional(), Length(max=150)])
    contact_details = StringField("وسيلة الاتصال", validators=[Optional(), Length(max=100)])
    email = StringField("البريد", validators=[Optional(), Email(), Length(max=200)])
    submit = SubmitField("حفظ")
