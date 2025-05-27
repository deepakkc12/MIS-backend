@echo off
call "%~dp0env.bat"

cd /d "%PROJECT_PATH%"

if "%1"=="install" (
    nssm install %SERVICE_NAME% "%PYTHON_PATH%" %DAEMON_ARGS%
    nssm set %SERVICE_NAME% AppDirectory "%PROJECT_PATH%"
    nssm set %SERVICE_NAME% AppStdout "%LOG_FILE%"
    nssm set %SERVICE_NAME% AppStderr "%LOG_FILE%"
    echo Service %SERVICE_NAME% installed.
    goto :EOF
)

if "%1"=="start" (
    nssm start %SERVICE_NAME%
    echo Service %SERVICE_NAME% started.
    goto :EOF
)

if "%1"=="stop" (
    nssm stop %SERVICE_NAME%
    echo Service %SERVICE_NAME% stopped.
    goto :EOF
)

if "%1"=="uninstall" (
    nssm remove %SERVICE_NAME% confirm
    echo Service %SERVICE_NAME% removed.
    goto :EOF
)

if "%1"=="restart" (
    nssm restart %SERVICE_NAME%
    echo Service %SERVICE_NAME% restarted.
    goto :EOF
)

if "%1"=="edit" (
    nssm edit %SERVICE_NAME%
    goto :EOF
)
echo Invalid command. Use one of: install, start, stop, uninstall, restart
