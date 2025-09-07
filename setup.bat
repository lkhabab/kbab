@echo off
cd /d %~dp0

echo === تفعيل البيئة الافتراضية ===
call venv\Scripts\activate

echo === تشغيل السيرفر ===
flask run

:: في حالة حدوث خطأ يخليك تشوف الرسالة بدل ما يقفل
pause
