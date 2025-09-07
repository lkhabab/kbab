@echo off
cd /d %~dp0
call venv\Scripts\activate
py -m flask --app wsgi run --debug --host=127.0.0.1 --port=5000
