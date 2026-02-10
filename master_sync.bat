@echo off
setlocal EnableDelayedExpansion

REM ==========================================
REM AutoSync Master - CONTINUOUS MODE
REM ==========================================
REM Runs every 5 minutes automatically
REM No USB wait - just syncs on schedule
REM ==========================================

set LOCKFILE=%TEMP%\autosync_master.lock

REM Check for existing instance
if exist "%LOCKFILE%" (
    echo.
    echo ============================================
    echo WARNING: Another instance is running!
    echo ============================================
    echo Lockfile: %LOCKFILE%
    echo.
    choice /C YN /M "Delete lockfile and continue"
    if errorlevel 2 (
        echo Operation cancelled.
        pause
        exit /b 1
    )
    del "%LOCKFILE%" 2>nul
)

REM Create lockfile
echo AutoSync started: %date% %time% > "%LOCKFILE%"

set SCRIPT_DIR=%~dp0
set SCRIPT_DIR=%SCRIPT_DIR:~0,-1%

set CONFIG=%SCRIPT_DIR%\sync_config.ini
set LOG_DIR=%SCRIPT_DIR%\logs

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

REM Generate log filename
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do set LOG_DATE=%%c_%%a_%%b
set LOGFILE=%LOG_DIR%\sync_%LOG_DATE%.log

REM Check config
if not exist "%CONFIG%" (
    echo ERROR: Configuration file not found: %CONFIG%
    del "%LOCKFILE%" 2>nul
    pause
    exit /b 1
)

REM Read check interval (in minutes)
set CHECK_INTERVAL=5
for /f "usebackq tokens=1,2 delims==" %%a in ("%CONFIG%") do (
    set LINE=%%a
    set VALUE=%%b
    for /f "tokens=* delims= " %%x in ("!LINE!") do set LINE=%%x
    for /f "tokens=* delims= " %%x in ("!VALUE!") do set VALUE=%%x
    if "!LINE!"=="check_interval" set CHECK_INTERVAL=!VALUE!
)

REM Read USB drive
set USB_DRIVE=
for /f "usebackq tokens=1,2 delims==" %%a in ("%CONFIG%") do (
    set LINE=%%a
    set VALUE=%%b
    for /f "tokens=* delims= " %%x in ("!LINE!") do set LINE=%%x
    for /f "tokens=* delims= " %%x in ("!VALUE!") do set VALUE=%%x
    if "!LINE!"=="drive" set USB_DRIVE=!VALUE!
)

cls
echo ============================================
echo    AutoSync Master - CONTINUOUS MODE
echo ============================================
echo Started: %date% %time%
echo Config: %CONFIG%
echo Log: %LOGFILE%
echo Interval: %CHECK_INTERVAL% minutes
echo ============================================
echo.
echo Press Ctrl+C to stop
echo.

echo. >> "%LOGFILE%"
echo ============================================ >> "%LOGFILE%"
echo AutoSync Master Started - CONTINUOUS MODE >> "%LOGFILE%"
echo ============================================ >> "%LOGFILE%"
echo Timestamp: %date% %time% >> "%LOGFILE%"
echo Interval: %CHECK_INTERVAL% minutes >> "%LOGFILE%"
echo ============================================ >> "%LOGFILE%"

:MAIN_LOOP

echo ============================================
echo [%time%] STARTING SYNC CYCLE
echo ============================================
echo.

echo. >> "%LOGFILE%"
echo ============================================ >> "%LOGFILE%"
echo [%time%] SYNC CYCLE START >> "%LOGFILE%"
echo ============================================ >> "%LOGFILE%"

REM Check if USB is connected (optional - sync works without it)
if defined USB_DRIVE (
    if exist "%USB_DRIVE%\" (
        echo [%time%] USB drive %USB_DRIVE% detected
        echo [%time%] USB drive %USB_DRIVE% detected >> "%LOGFILE%"
        set USB_AVAILABLE=1
    ) else (
        echo [%time%] USB drive %USB_DRIVE% not connected (skipping USB sync)
        echo [%time%] USB drive %USB_DRIVE% not connected >> "%LOGFILE%"
        set USB_AVAILABLE=0
    )
) else (
    set USB_AVAILABLE=0
)

echo.

REM Track module execution
set MODULES_SUCCESS=0
set MODULES_FAILED=0
set MODULES_SKIPPED=0

REM ==========================================
REM MODULE 1: USB SYNC
REM ==========================================
if !USB_AVAILABLE! EQU 1 (
    if exist "%SCRIPT_DIR%\usb_sync.bat" (
        echo [%time%] [1/4] Running: USB Sync
        echo [%time%] [1/4] Running: USB Sync >> "%LOGFILE%"
        
        call "%SCRIPT_DIR%\usb_sync.bat" "%CONFIG%" "%LOGFILE%"
        
        if !ERRORLEVEL! EQU 0 (
            echo [%time%] [1/4] ✓ USB Sync completed
            echo [%time%] [1/4] SUCCESS: USB Sync >> "%LOGFILE%"
            set /a MODULES_SUCCESS+=1
        ) else (
            echo [%time%] [1/4] ✗ USB Sync failed
            echo [%time%] [1/4] FAILED: USB Sync >> "%LOGFILE%"
            set /a MODULES_FAILED+=1
        )
    ) else (
        echo [%time%] [1/4] - USB Sync not found
        echo [%time%] [1/4] SKIP: usb_sync.bat not found >> "%LOGFILE%"
        set /a MODULES_SKIPPED+=1
    )
) else (
    echo [%time%] [1/4] - USB Sync skipped (no USB)
    echo [%time%] [1/4] SKIP: USB not available >> "%LOGFILE%"
    set /a MODULES_SKIPPED+=1
)

echo.

REM ==========================================
REM MODULE 2: GIT SYNC
REM ==========================================
if exist "%SCRIPT_DIR%\git_sync.bat" (
    echo [%time%] [2/4] Running: Git Sync
    echo [%time%] [2/4] Running: Git Sync >> "%LOGFILE%"
    
    call "%SCRIPT_DIR%\git_sync.bat" "%CONFIG%" "%LOGFILE%"
    
    if !ERRORLEVEL! EQU 0 (
        echo [%time%] [2/4] ✓ Git Sync completed
        echo [%time%] [2/4] SUCCESS: Git Sync >> "%LOGFILE%"
        set /a MODULES_SUCCESS+=1
    ) else (
        echo [%time%] [2/4] ✗ Git Sync failed
        echo [%time%] [2/4] FAILED: Git Sync >> "%LOGFILE%"
        set /a MODULES_FAILED+=1
    )
) else (
    echo [%time%] [2/4] - Git Sync not found
    echo [%time%] [2/4] SKIP: git_sync.bat not found >> "%LOGFILE%"
    set /a MODULES_SKIPPED+=1
)

echo.

REM ==========================================
REM MODULE 3: DATABASE DEPLOYMENT
REM ==========================================
if exist "%SCRIPT_DIR%\db_deploy.bat" (
    echo [%time%] [3/4] Running: Database Deploy
    echo [%time%] [3/4] Running: Database Deploy >> "%LOGFILE%"
    
    call "%SCRIPT_DIR%\db_deploy.bat" "%CONFIG%" "%LOGFILE%"
    
    if !ERRORLEVEL! EQU 0 (
        echo [%time%] [3/4] ✓ Database Deploy completed
        echo [%time%] [3/4] SUCCESS: Database Deploy >> "%LOGFILE%"
        set /a MODULES_SUCCESS+=1
    ) else (
        echo [%time%] [3/4] ✗ Database Deploy failed
        echo [%time%] [3/4] FAILED: Database Deploy >> "%LOGFILE%"
        set /a MODULES_FAILED+=1
    )
) else (
    echo [%time%] [3/4] - Database Deploy not found
    echo [%time%] [3/4] SKIP: db_deploy.bat not found >> "%LOGFILE%"
    set /a MODULES_SKIPPED+=1
)

echo.

REM ==========================================
REM MODULE 4: WEB DEPLOYMENT
REM ==========================================
if exist "%SCRIPT_DIR%\web_deploy.bat" (
    echo [%time%] [4/4] Running: Web Deploy
    echo [%time%] [4/4] Running: Web Deploy >> "%LOGFILE%"
    
    call "%SCRIPT_DIR%\web_deploy.bat" "%CONFIG%" "%LOGFILE%"
    
    if !ERRORLEVEL! EQU 0 (
        echo [%time%] [4/4] ✓ Web Deploy completed
        echo [%time%] [4/4] SUCCESS: Web Deploy >> "%LOGFILE%"
        set /a MODULES_SUCCESS+=1
    ) else (
        echo [%time%] [4/4] ✗ Web Deploy failed
        echo [%time%] [4/4] FAILED: Web Deploy >> "%LOGFILE%"
        set /a MODULES_FAILED+=1
    )
) else (
    echo [%time%] [4/4] - Web Deploy not found
    echo [%time%] [4/4] SKIP: web_deploy.bat not found >> "%LOGFILE%"
    set /a MODULES_SKIPPED+=1
)

echo.
echo ============================================
echo [%time%] SYNC CYCLE COMPLETE
echo ============================================
echo Success: %MODULES_SUCCESS% ^| Failed: %MODULES_FAILED% ^| Skipped: %MODULES_SKIPPED%
echo.
echo Next sync in %CHECK_INTERVAL% minutes...
echo ============================================
echo.

echo. >> "%LOGFILE%"
echo ============================================ >> "%LOGFILE%"
echo [%time%] SYNC CYCLE COMPLETE >> "%LOGFILE%"
echo ============================================ >> "%LOGFILE%"
echo Success: %MODULES_SUCCESS% >> "%LOGFILE%"
echo Failed: %MODULES_FAILED% >> "%LOGFILE%"
echo Skipped: %MODULES_SKIPPED% >> "%LOGFILE%"
echo Next sync: %CHECK_INTERVAL% minutes >> "%LOGFILE%"
echo ============================================ >> "%LOGFILE%"

REM Wait for next cycle (convert minutes to seconds)
set /a WAIT_SECONDS=%CHECK_INTERVAL%*60
timeout /t %WAIT_SECONDS% /nobreak

goto MAIN_LOOP

REM Cleanup on exit (Ctrl+C)
if exist "%LOCKFILE%" del "%LOCKFILE%" 2>nul
endlocal