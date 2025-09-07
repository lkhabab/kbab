# app/blueprints/auth/__init__.py
from flask import Blueprint


# اسم البلوبرنت ومجلد القوالب الخاص فيه
bp = Blueprint("auth", __name__, template_folder="templates")

# تحميل المستخدم للجلسات (Flask-Login)
from ...extensions import login_manager
from ...models import User


@login_manager.user_loader
def load_user(user_id: str):
    try:
        return User.query.get(int(user_id))
    except Exception:
        return None


# مهم: استيراد الراوتس بعد تعريف bp حتى تُسجَّل المسارات
from . import routes  # noqa: F401
