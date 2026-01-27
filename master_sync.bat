@echo off
setlocal EnableDelayedExpansion
title AutoSync Master - USB Monitor

REM ==== INITIALIZE ====
set SCRIPT_DIR=%~dp0
set SCRIPT_DIR=%SCRIPT_DIR:~0,-1%
set CONFIG_FILE=%SCRIPT_DIR%\sync_config.ini
set MODULE_DIR=%SCRIPT_DIR%\modules

REM Read config
call :READ_CONFIG

REM Create log directory
set LOG_DIR=%SCRIPT_DIR%\%LOG_DIR_CONFIG%
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

REM Set log file with date
for /f "tokens=1-3 delims=/ " %%a in ('date /t') do set LOG_DATE=%%a_%%b_%%c
set LOGFILE=%LOG_DIR%\sync_%LOG_DATE%.log

echo ========================================= >> "%LOGFILE%"
echo AutoSync Master Started: %date% %time% >> "%LOGFILE%"
echo ========================================= >> "%LOGFILE%"
echo Config loaded from: %CONFIG_FILE% >> "%LOGFILE%"
echo.

cls
echo ╔════════════════════════════════════════╗
echo ║        AutoSync Master v2.0            ║
echo ╚════════════════════════════════════════╝
echo.
echo [*] Monitoring for USB drive: %USB_DRIVE%
echo [*] Log: %LOGFILE%
echo [*] Press Ctrl+C to exit
echo.

:MAIN_LOOP
timeout /t %CHECK_INTERVAL% >nul

if not exist %USB_DRIVE%\ (
    echo [%time%] Waiting for USB... >> "%LOGFILE%"
    goto MAIN_LOOP
)

echo ========================================= >> "%LOGFILE%"
echo [%time%] USB DETECTED: %USB_DRIVE% >> "%LOGFILE%"
echo ========================================= >> "%LOGFILE%"
echo.
echo [√] USB detected! Starting sync...

REM ==== RUN ALL MODULES ====
call :RUN_MODULE "usb_sync.bat" "USB Sync (E: ↔ USB)"
call :RUN_MODULE "git_sync.bat" "Git Auto-Commit/Push"
call :RUN_MODULE "db_deploy.bat" "Database Deployment"
call :RUN_MODULE "web_deploy.bat" "Web Files Deployment"

echo [%time%] All modules completed >> "%LOGFILE%"
echo.
echo [√] Sync complete! Monitoring for USB removal...

:USB_MONITOR
timeout /t %CHECK_INTERVAL% >nul

if not exist %USB_DRIVE%\ (
    echo ========================================= >> "%LOGFILE%"
    echo [%time%] USB REMOVED >> "%LOGFILE%"
    echo ========================================= >> "%LOGFILE%"
    echo.
    echo [!] USB removed. Waiting for next insertion...
    goto MAIN_LOOP
)

goto USB_MONITOR

REM ==== SUBROUTINES ====

:RUN_MODULE
set MODULE_NAME=%~1
set MODULE_DESC=%~2
set MODULE_PATH=%MODULE_DIR%\%MODULE_NAME%

if not exist "%MODULE_PATH%" (
    echo [%time%] ERROR: Module not found: %MODULE_PATH% >> "%LOGFILE%"
    echo [X] Module not found: %MODULE_NAME%
    goto :EOF
)

echo [%time%] Running: %MODULE_DESC% >> "%LOGFILE%"
echo [→] %MODULE_DESC%...
call "%MODULE_PATH%" "%CONFIG_FILE%" "%LOGFILE%"
if errorlevel 1 (
    echo [%time%] WARNING: %MODULE_NAME% returned error code %errorlevel% >> "%LOGFILE%"
    echo [!] Warning: %MODULE_NAME% had errors
) else (
    echo [%time%] SUCCESS: %MODULE_DESC% completed >> "%LOGFILE%"
    echo [√] %MODULE_DESC% done
)
goto :EOF

:READ_CONFIG
REM Read USB drive
for /f "usebackq tokens=1,2 delims==" %%a in ("%CONFIG_FILE%") do (
    set LINE=%%a
    set VALUE=%%b
    
    REM Remove leading/trailing spaces
    for /f "tokens=* delims= " %%x in ("!LINE!") do set LINE=%%x
    for /f "tokens=* delims= " %%x in ("!VALUE!") do set VALUE=%%x
    
    REM Skip comments and empty lines
    if not "!LINE!"=="" (
        if not "!LINE:~0,1!"==";" (
            if "!LINE!"=="drive" set USB_DRIVE=!VALUE!
            if "!LINE!"=="check_interval" set CHECK_INTERVAL=!VALUE!
            if "!LINE!"=="dir" set LOG_DIR_CONFIG=!VALUE!
        )
    )
)

REM Set defaults if not found
if not defined USB_DRIVE set USB_DRIVE=G:
if not defined CHECK_INTERVAL set CHECK_INTERVAL=5
if not defined LOG_DIR_CONFIG set LOG_DIR_CONFIG=logs

goto :EOF

endlocal
