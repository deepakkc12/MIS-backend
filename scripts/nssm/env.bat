@echo off
:: Define environment variables
set PYTHON_PATH=C:\djangoProjects\Env1\env\Scripts\python.exe
set PROJECT_PATH=C:\djangoProjects\Env1\server
set SERVICE_NAME=MISDaphne
set DAEMON_ARGS=-m daphne -b 103.12.1.191 -p 6000 config.asgi:application
set LOG_FILE=C:\djangoProjects\Env1\server\logs\daphne.log