@echo off
setlocal EnableDelayedExpansion

REM ═══════════════════════════════════════════════════
REM AutoSync Master Orchestrator v2.1
REM Runs all sync modules when USB is detected
REM ═══════════════════════════════════════════════════

REM Get script directory
set SCRIPT_DIR=%~dp0
set SCRIPT_DIR=%SCRIPT_DIR:~0,-1%

REM Paths
set CONFIG=%SCRIPT_DIR%\sync_config.ini
set LOG_DIR=%SCRIPT_DIR%\logs
set MODULE_DIR=%SCRIPT_DIR%\modules

REM Create logs directory if it doesn't exist
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

REM Set log file with date
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (
    set LOG_DATE=%%c_%%a_%%b
)
set LOGFILE=%LOG_DIR%\sync_%LOG_DATE%.log

REM Check if config exists
if not exist "%CONFIG%" (
    echo ERROR: Configuration file not found: %CONFIG%
    echo Please run setup.bat first!
    pause
    exit /b 1
)

REM Start logging
echo ========================================= >> "%LOGFILE%"
echo AutoSync Master Started: %date% %time% >> "%LOGFILE%"
echo ========================================= >> "%LOGFILE%"
echo Config loaded from: %CONFIG% >> "%LOGFILE%"
echo ========================================= >> "%LOGFILE%"

REM Read USB drive letter from config
set USB_DRIVE=
for /f "usebackq tokens=1,2 delims==" %%a in ("%CONFIG%") do (
    set LINE=%%a
    set VALUE=%%b
    for /f "tokens=* delims= " %%x in ("!LINE!") do set LINE=%%x
    for /f "tokens=* delims= " %%x in ("!VALUE!") do set VALUE=%%x
    if "!LINE!"=="drive" set USB_DRIVE=!VALUE!
)

if not defined USB_DRIVE (
    echo ERROR: USB drive not configured in sync_config.ini
    pause
    exit /b 1
)

REM Read check interval
set CHECK_INTERVAL=5
for /f "usebackq tokens=1,2 delims==" %%a in ("%CONFIG%") do (
    set LINE=%%a
    set VALUE=%%b
    for /f "tokens=* delims= " %%x in ("!LINE!") do set LINE=%%x
    for /f "tokens=* delims= " %%x in ("!VALUE!") do set VALUE=%%x
    if "!LINE!"=="check_interval" set CHECK_INTERVAL=!VALUE!
)

REM Main loop - runs forever
:MAIN_LOOP

REM Wait for USB drive
:WAIT_FOR_USB
if not exist "%USB_DRIVE%\" (
    timeout /t %CHECK_INTERVAL% /nobreak >nul
    goto WAIT_FOR_USB
)

echo [%time%] USB DETECTED: %USB_DRIVE% >> "%LOGFILE%"
echo ========================================= >> "%LOGFILE%"

REM ════════════════════════════════════════
REM MODULE 1: USB Sync (E: ↔ USB)
REM ════════════════════════════════════════
echo [%time%] Running: USB Sync (E: ^<-^> USB) >> "%LOGFILE%"
if exist "%MODULE_DIR%\usb_sync.bat" (
    call "%MODULE_DIR%\usb_sync.bat" "%CONFIG%" "%LOGFILE%"
) else (
    echo [%time%] WARNING: usb_sync.bat not found! >> "%LOGFILE%"
)

REM ════════════════════════════════════════
REM MODULE 2: Git Auto-Commit/Push
REM ════════════════════════════════════════
echo [%time%] Running: Git Sync (auto-commit/push) >> "%LOGFILE%"
if exist "%MODULE_DIR%\git_sync.bat" (
    call "%MODULE_DIR%\git_sync.bat" "%CONFIG%" "%LOGFILE%"
) else (
    echo [%time%] WARNING: git_sync.bat not found! >> "%LOGFILE%"
)

REM ════════════════════════════════════════
REM MODULE 3: Database Deployment
REM ════════════════════════════════════════
echo [%time%] Running: Database Deployment (.sql -^> MySQL) >> "%LOGFILE%"
if exist "%MODULE_DIR%\db_deploy.bat" (
    call "%MODULE_DIR%\db_deploy.bat" "%CONFIG%" "%LOGFILE%"
) else (
    echo [%time%] WARNING: db_deploy.bat not found! >> "%LOGFILE%"
)

REM ════════════════════════════════════════
REM MODULE 4: Web Deployment
REM ════════════════════════════════════════
echo [%time%] Running: Web Deployment (PHP -^> htdocs) >> "%LOGFILE%"
if exist "%MODULE_DIR%\web_deploy.bat" (
    call "%MODULE_DIR%\web_deploy.bat" "%CONFIG%" "%LOGFILE%"
) else (
    echo [%time%] WARNING: web_deploy.bat not found! >> "%LOGFILE%"
)

echo ========================================= >> "%LOGFILE%"
echo [%time%] ALL MODULES COMPLETE >> "%LOGFILE%"
echo ========================================= >> "%LOGFILE%"
echo. >> "%LOGFILE%"

REM Wait for USB removal
:WAIT_FOR_REMOVAL
if exist "%USB_DRIVE%\" (
    timeout /t %CHECK_INTERVAL% /nobreak >nul
    goto WAIT_FOR_REMOVAL
)

echo [%time%] USB REMOVED: %USB_DRIVE% >> "%LOGFILE%"
echo [%time%] Waiting for next insertion... >> "%LOGFILE%"
echo. >> "%LOGFILE%"

REM Loop back to wait for USB again
goto MAIN_LOOP

endlocal
