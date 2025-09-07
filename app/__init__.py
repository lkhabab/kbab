# app/__init__.py
import os
from flask import Flask, render_template
from .config import Config
from .extensions import db, migrate, login_manager, csrf


def _ensure_sqlite_in_instance(app):
    """
    لو ما تم ضبط SQLALCHEMY_DATABASE_URI في Config، فعّل SQLite داخل مجلد instance.
    """
    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        db_path = os.path.join(app.instance_path, "app.db")
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
        app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)


def create_app(config_object: type | None = None) -> Flask:
    app = Flask(
        __name__,
        static_folder="static",
        template_folder="templates",
        instance_relative_config=True,
    )

    # تأكد من وجود مجلد instance (لقاعدة SQLite والملفات الحساسة)
    os.makedirs(app.instance_path, exist_ok=True)

    # تحميل الإعدادات
    app.config.from_object(config_object or Config)
    _ensure_sqlite_in_instance(app)

    # تهيئة الإضافات
    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)
    # تحديد صفحة تسجيل الدخول الافتراضية للـ @login_required
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    csrf.init_app(app)

    # ===== تسجيل البلوبرنتس =====
    # NOTE: الاستيراد داخل create_app لتجنّب circular imports
    from .blueprints.main import bp as main_bp
    from .blueprints.auth import bp as auth_bp
    from .blueprints.api import bp as api_bp
    from .blueprints.weather import bp as weather_bp

    app.register_blueprint(main_bp)                         # /
    app.register_blueprint(auth_bp, url_prefix="/auth")     # /auth/...
    app.register_blueprint(api_bp,  url_prefix="/api")      # /api/...
    app.register_blueprint(weather_bp)                      # /weather

    # لو API عندك تستقبل JSON POST بدون CSRF، أعفِها هنا:
    try:
        from .blueprints.api import bp as _api_bp_for_csrf
        csrf.exempt(_api_bp_for_csrf)
    except Exception:
        # لو ما تحتاج إعفاء، تجاهل
        pass

    # ===== حقن cal عالميًا (شبكة أمان) =====
    @app.context_processor
    def inject_cal():
        try:
            # نسحب CAL_DATA من بلوبرنت الطقس-الكالندر
            from .blueprints.weather import CAL_DATA
            return {"cal": CAL_DATA}
        except Exception:
            return {"cal": {}}

    # ===== صفحات الأخطاء =====
    @app.errorhandler(404)
    def not_found(e):
        # يعطي صفحة 404.html إن وجدت؛ وإلا يرجّع نص بسيط
        try:
            return render_template("errors/404.html"), 404
        except Exception:
            return "404 - الصفحة غير موجودة", 404

    @app.errorhandler(500)
    def server_error(e):
        try:
            return render_template("errors/500.html"), 500
        except Exception:
            return "500 - خطأ داخلي في الخادم", 500

    # ===== shell context (يسهّل تجربة ORM في flask shell) =====
    @app.shell_context_processor
    def make_shell_context():
        from . import models
        return {"db": db, "models": models}

    # ===== أمر CLI لتهيئة القاعدة بسرعة (اختياري) =====
    @app.cli.command("init-db")
    def init_db_command():
        """إنشاء الجداول (create_all) — مفيد أثناء التطوير."""
        with app.app_context():
            db.create_all()
            print("✓ Database initialized.")

    return app
