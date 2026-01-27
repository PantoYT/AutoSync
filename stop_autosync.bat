@echo off
title Stop AutoSync (Enhanced)

echo.
echo ════════════════════════════════════════
echo  Stopping ALL AutoSync processes...
echo ════════════════════════════════════════
echo.

set KILLED=0

REM Kill master_sync.bat by window title
taskkill /FI "WindowTitle eq AutoSync Master*" /F >nul 2>&1
if not errorlevel 1 (
    echo [√] Stopped master_sync.bat
    set /a KILLED+=1
)

REM Kill ALL module processes by searching command line
for %%M in (usb_sync.bat git_sync.bat db_deploy.bat web_deploy.bat) do (
    for /f "tokens=2" %%i in ('tasklist ^| find "cmd.exe"') do (
        wmic process where "ProcessId=%%i" get CommandLine 2>nul | find "%%M" >nul
        if not errorlevel 1 (
            taskkill /PID %%i /F >nul 2>&1
            echo [√] Stopped %%M (PID: %%i)
            set /a KILLED+=1
        )
    )
)

REM Also check for wscript running master_launcher.vbs
for /f "tokens=2" %%i in ('tasklist ^| find "wscript.exe"') do (
    wmic process where "ProcessId=%%i" get CommandLine 2>nul | find "master_launcher.vbs" >nul
    if not errorlevel 1 (
        taskkill /PID %%i /F >nul 2>&1
        echo [√] Stopped launcher (PID: %%i)
        set /a KILLED+=1
    )
)

echo.
if %KILLED% GTR 0 (
    echo [√] Stopped %KILLED% AutoSync process(es)
) else (
    echo [!] No AutoSync processes found running
)
echo.
echo To restart, double-click master_launcher.vbs
echo.
pause
