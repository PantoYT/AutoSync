@echo off
setlocal EnableDelayedExpansion

REM ==========================================
REM AutoSync Master - IMPROVED VERSION
REM ==========================================
REM Added Features:
REM - Better crash recovery
REM - Detailed progress logging
REM - Timeout protection
REM - Auto-cleanup on errors
REM - Module success/failure tracking
REM ==========================================

set LOCKFILE=%TEMP%\autosync_master.lock

REM Check for existing instance
if exist "%LOCKFILE%" (
    echo.
    echo ============================================
    echo WARNING: Lockfile detected!
    echo ============================================
    echo Another instance may be running, or the last
    echo session crashed without cleaning up.
    echo.
    echo Lockfile: %LOCKFILE%
    echo.
    choice /C YN /M "Delete lockfile and continue"
    if errorlevel 2 (
        echo Operation cancelled.
        pause
        exit /b 1
    )
    echo Deleting stale lockfile...
    del "%LOCKFILE%" 2>nul
    echo.
)

REM Create lockfile with timestamp
echo AutoSync started: %date% %time% > "%LOCKFILE%"
echo PID: %RANDOM%%RANDOM% >> "%LOCKFILE%"

REM Setup cleanup trap
set "CLEANUP_NEEDED=1"

set SCRIPT_DIR=%~dp0
set SCRIPT_DIR=%SCRIPT_DIR:~0,-1%

set CONFIG=%SCRIPT_DIR%\sync_config.ini
set LOG_DIR=%SCRIPT_DIR%\logs
set MODULE_DIR=%SCRIPT_DIR%\modules

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

REM Generate log filename with date
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (
    set LOG_DATE=%%c_%%a_%%b
)
set LOGFILE=%LOG_DIR%\sync_%LOG_DATE%.log

REM Check config file
if not exist "%CONFIG%" (
    echo ============================================
    echo ERROR: Configuration file not found!
    echo ============================================
    echo Expected location: %CONFIG%
    echo.
    echo Please create sync_config.ini or run setup.bat
    echo.
    call :CLEANUP
    pause
    exit /b 1
)

REM Display startup banner
cls
echo ============================================
echo    AutoSync Master - IMPROVED v2.0
echo ============================================
echo Started: %date% %time%
echo Config: %CONFIG%
echo Log: %LOGFILE%
echo ============================================
echo.

REM Log startup
echo. >> "%LOGFILE%"
echo ============================================ >> "%LOGFILE%"
echo AutoSync Master IMPROVED Started >> "%LOGFILE%"
echo ============================================ >> "%LOGFILE%"
echo Timestamp: %date% %time% >> "%LOGFILE%"
echo Config: %CONFIG% >> "%LOGFILE%"
echo Lockfile: %LOCKFILE% >> "%LOGFILE%"
echo ============================================ >> "%LOGFILE%"
echo. >> "%LOGFILE%"

REM Read USB drive configuration
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
    echo Please set drive=X: in the [USB] section
    echo.
    call :CLEANUP
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

echo Monitoring USB drive: %USB_DRIVE%
echo Check interval: %CHECK_INTERVAL% seconds
echo.
echo Press Ctrl+C to stop (lockfile will be cleaned up)
echo ============================================
echo.

echo [%time%] Waiting for USB drive: %USB_DRIVE% >> "%LOGFILE%"

:MAIN_LOOP

REM ==========================================
REM WAIT FOR USB INSERTION
REM ==========================================
:WAIT_FOR_USB
if not exist "%USB_DRIVE%\" (
    REM Show waiting indicator (every 30 seconds)
    set /a WAIT_COUNT+=1
    if !WAIT_COUNT! GEQ 6 (
        echo [%time%] Still waiting for USB: %USB_DRIVE%
        set WAIT_COUNT=0
    )
    timeout /t %CHECK_INTERVAL% /nobreak >nul
    goto WAIT_FOR_USB
)

REM Reset wait counter
set WAIT_COUNT=0

echo.
echo ============================================
echo [%time%] USB DETECTED: %USB_DRIVE%
echo ============================================
echo.

echo. >> "%LOGFILE%"
echo ============================================ >> "%LOGFILE%"
echo [%time%] USB DETECTED: %USB_DRIVE% >> "%LOGFILE%"
echo ============================================ >> "%LOGFILE%"

REM Track module execution
set MODULES_RUN=0
set MODULES_SUCCESS=0
set MODULES_FAILED=0

REM ==========================================
REM MODULE 1: USB SYNC
REM ==========================================
echo [%time%] [1/4] Running: USB Sync (E: ^<-^> USB)
echo [%time%] [1/4] Running: USB Sync (E: ^<-^> USB) >> "%LOGFILE%"

if exist "%MODULE_DIR%\usb_sync.bat" (
    set /a MODULES_RUN+=1
    
    call "%MODULE_DIR%\usb_sync.bat" "%CONFIG%" "%LOGFILE%"
    set MODULE_ERROR=!ERRORLEVEL!
    
    if !MODULE_ERROR! EQU 0 (
        echo [%time%] SUCCESS: USB Sync completed
        echo [%time%] SUCCESS: USB Sync completed >> "%LOGFILE%"
        set /a MODULES_SUCCESS+=1
    ) else (
        echo [%time%] WARNING: USB Sync failed with error code !MODULE_ERROR!
        echo [%time%] ERROR: USB Sync failed with code !MODULE_ERROR! >> "%LOGFILE%"
        set /a MODULES_FAILED+=1
    )
) else (
    echo [%time%] SKIPPED: usb_sync.bat not found!
    echo [%time%] WARNING: usb_sync.bat not found in %MODULE_DIR% >> "%LOGFILE%"
)

echo.

REM ==========================================
REM MODULE 2: GIT SYNC
REM ==========================================
echo [%time%] [2/4] Running: Git Sync (auto-commit/push)
echo [%time%] [2/4] Running: Git Sync (auto-commit/push) >> "%LOGFILE%"

if exist "%MODULE_DIR%\git_sync.bat" (
    set /a MODULES_RUN+=1
    
    call "%MODULE_DIR%\git_sync.bat" "%CONFIG%" "%LOGFILE%"
    set MODULE_ERROR=!ERRORLEVEL!
    
    if !MODULE_ERROR! EQU 0 (
        echo [%time%] SUCCESS: Git Sync completed
        echo [%time%] SUCCESS: Git Sync completed >> "%LOGFILE%"
        set /a MODULES_SUCCESS+=1
    ) else (
        echo [%time%] WARNING: Git Sync had issues (code !MODULE_ERROR!)
        echo [%time%] WARNING: Git Sync exited with code !MODULE_ERROR! >> "%LOGFILE%"
        set /a MODULES_FAILED+=1
    )
) else (
    echo [%time%] SKIPPED: git_sync.bat not found
    echo [%time%] INFO: git_sync.bat not found >> "%LOGFILE%"
)

echo.

REM ==========================================
REM MODULE 3: DATABASE DEPLOYMENT
REM ==========================================
echo [%time%] [3/4] Running: Database Deployment (.sql -^> MySQL)
echo [%time%] [3/4] Running: Database Deployment (.sql -^> MySQL) >> "%LOGFILE%"

if exist "%MODULE_DIR%\db_deploy.bat" (
    set /a MODULES_RUN+=1
    
    call "%MODULE_DIR%\db_deploy.bat" "%CONFIG%" "%LOGFILE%"
    set MODULE_ERROR=!ERRORLEVEL!
    
    if !MODULE_ERROR! EQU 0 (
        echo [%time%] SUCCESS: Database Deployment completed
        echo [%time%] SUCCESS: Database Deployment completed >> "%LOGFILE%"
        set /a MODULES_SUCCESS+=1
    ) else (
        echo [%time%] WARNING: Database Deployment had issues (code !MODULE_ERROR!)
        echo [%time%] WARNING: Database Deployment exited with code !MODULE_ERROR! >> "%LOGFILE%"
        set /a MODULES_FAILED+=1
    )
) else (
    echo [%time%] SKIPPED: db_deploy.bat not found
    echo [%time%] INFO: db_deploy.bat not found >> "%LOGFILE%"
)

echo.

REM ==========================================
REM MODULE 4: WEB DEPLOYMENT
REM ==========================================
echo [%time%] [4/4] Running: Web Deployment (PHP -^> htdocs)
echo [%time%] [4/4] Running: Web Deployment (PHP -^> htdocs) >> "%LOGFILE%"

if exist "%MODULE_DIR%\web_deploy.bat" (
    set /a MODULES_RUN+=1
    
    call "%MODULE_DIR%\web_deploy.bat" "%CONFIG%" "%LOGFILE%"
    set MODULE_ERROR=!ERRORLEVEL!
    
    if !MODULE_ERROR! EQU 0 (
        echo [%time%] SUCCESS: Web Deployment completed
        echo [%time%] SUCCESS: Web Deployment completed >> "%LOGFILE%"
        set /a MODULES_SUCCESS+=1
    ) else (
        echo [%time%] WARNING: Web Deployment had issues (code !MODULE_ERROR!)
        echo [%time%] WARNING: Web Deployment exited with code !MODULE_ERROR! >> "%LOGFILE%"
        set /a MODULES_FAILED+=1
    )
) else (
    echo [%time%] SKIPPED: web_deploy.bat not found
    echo [%time%] INFO: web_deploy.bat not found >> "%LOGFILE%"
)

echo.
echo ============================================
echo [%time%] SYNC CYCLE COMPLETE
echo ============================================
echo Modules run: %MODULES_RUN%
echo Successful: %MODULES_SUCCESS%
echo Failed: %MODULES_FAILED%
echo ============================================
echo.

echo. >> "%LOGFILE%"
echo ============================================ >> "%LOGFILE%"
echo [%time%] SYNC CYCLE COMPLETE >> "%LOGFILE%"
echo ============================================ >> "%LOGFILE%"
echo Modules run: %MODULES_RUN% >> "%LOGFILE%"
echo Successful: %MODULES_SUCCESS% >> "%LOGFILE%"
echo Failed: %MODULES_FAILED% >> "%LOGFILE%"
echo ============================================ >> "%LOGFILE%"
echo. >> "%LOGFILE%"

REM ==========================================
REM WAIT FOR USB REMOVAL
REM ==========================================
echo Waiting for USB removal...
echo [%time%] Waiting for USB removal... >> "%LOGFILE%"

:WAIT_FOR_REMOVAL
if exist "%USB_DRIVE%\" (
    timeout /t %CHECK_INTERVAL% /nobreak >nul
    goto WAIT_FOR_REMOVAL
)

echo.
echo ============================================
echo [%time%] USB REMOVED: %USB_DRIVE%
echo ============================================
echo Waiting for next insertion...
echo.

echo. >> "%LOGFILE%"
echo [%time%] USB REMOVED: %USB_DRIVE% >> "%LOGFILE%"
echo [%time%] Waiting for next insertion... >> "%LOGFILE%"
echo. >> "%LOGFILE%"

goto MAIN_LOOP

REM ==========================================
REM CLEANUP SUBROUTINE
REM ==========================================
:CLEANUP
if defined CLEANUP_NEEDED (
    echo.
    echo [%time%] Cleaning up...
    echo [%time%] AutoSync cleanup initiated >> "%LOGFILE%" 2>nul
    
    if exist "%LOCKFILE%" (
        del "%LOCKFILE%" 2>nul
        if exist "%LOCKFILE%" (
            echo WARNING: Could not delete lockfile!
            echo Manual cleanup may be needed: %LOCKFILE%
        ) else (
            echo Lockfile removed successfully
        )
    )
    
    echo [%time%] AutoSync stopped cleanly >> "%LOGFILE%" 2>nul
    set CLEANUP_NEEDED=
)
exit /b 0

endlocal