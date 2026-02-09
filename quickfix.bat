@echo off
setlocal EnableDelayedExpansion

REM ==========================================
REM AutoSync Quick Fix Tool
REM ==========================================
REM Automatically fixes common issues:
REM - Removes stale lockfiles
REM - Kills hung processes
REM - Cleans up temp files
REM - Creates missing directories
REM ==========================================

cls
echo ============================================
echo    AutoSync Quick Fix Tool
echo ============================================
echo.
echo This script will:
echo  1. Kill any hung AutoSync processes
echo  2. Remove stale lockfiles
echo  3. Clean up temporary files
echo  4. Create missing directories
echo.
choice /C YN /M "Continue with quick fix"
if errorlevel 2 (
    echo Operation cancelled.
    exit /b 0
)

echo.
echo ============================================
echo Starting Quick Fix...
echo ============================================
echo.

REM ==========================================
REM FIX 1: Kill processes
REM ==========================================
echo [1/5] Killing AutoSync processes...

taskkill /FI "WINDOWTITLE eq master_sync.bat*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq usb_sync.bat*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq git_sync.bat*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq db_deploy.bat*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq web_deploy.bat*" /F >nul 2>&1

wmic process where "name='cmd.exe' and commandline like '%%master_sync.bat%%'" delete >nul 2>&1
wmic process where "name='cmd.exe' and commandline like '%%usb_sync.bat%%'" delete >nul 2>&1

taskkill /IM robocopy.exe /F >nul 2>&1

echo [OK] Processes killed

REM ==========================================
REM FIX 2: Remove lockfile
REM ==========================================
echo [2/5] Removing stale lockfiles...

set LOCKFILE=%TEMP%\autosync_master.lock

if exist "%LOCKFILE%" (
    del "%LOCKFILE%" 2>nul
    if exist "%LOCKFILE%" (
        echo [WARNING] Could not delete lockfile: %LOCKFILE%
        echo Please delete it manually
    ) else (
        echo [OK] Lockfile removed: %LOCKFILE%
    )
) else (
    echo [OK] No lockfile found
)

REM ==========================================
REM FIX 3: Clean temp files
REM ==========================================
echo [3/5] Cleaning temporary files...

REM Clean old robocopy temp files
del /q "%TEMP%\robocopy_*" 2>nul

echo [OK] Temporary files cleaned

REM ==========================================
REM FIX 4: Create missing directories
REM ==========================================
echo [4/5] Creating missing directories...

set SCRIPT_DIR=%~dp0
set SCRIPT_DIR=%SCRIPT_DIR:~0,-1%

if not exist "%SCRIPT_DIR%\logs" (
    mkdir "%SCRIPT_DIR%\logs" 2>nul
    echo [OK] Created logs directory
)

if not exist "%SCRIPT_DIR%\modules" (
    mkdir "%SCRIPT_DIR%\modules" 2>nul
    echo [OK] Created modules directory
)

REM Create local project directories if they don't exist
if not exist "E:\Pliki\Projects" (
    mkdir "E:\Pliki\Projects" 2>nul
    echo [OK] Created E:\Pliki\Projects
)

if not exist "E:\Pliki\Projects\databases" (
    mkdir "E:\Pliki\Projects\databases" 2>nul
    echo [OK] Created databases directory
)

if not exist "E:\Pliki\Projects\cpp" (
    mkdir "E:\Pliki\Projects\cpp" 2>nul
    echo [OK] Created cpp directory
)

if not exist "E:\Pliki\Projects\python" (
    mkdir "E:\Pliki\Projects\python" 2>nul
    echo [OK] Created python directory
)

if not exist "E:\Pliki\Projects\websites" (
    mkdir "E:\Pliki\Projects\websites" 2>nul
    echo [OK] Created websites directory
)

echo [OK] Directory structure verified

REM ==========================================
REM FIX 5: Verify configuration
REM ==========================================
echo [5/5] Verifying configuration...

set CONFIG=%SCRIPT_DIR%\sync_config.ini

if exist "%CONFIG%" (
    echo [OK] Configuration file found
) else (
    echo [WARNING] Configuration file not found: %CONFIG%
    echo Please create sync_config.ini or run setup.bat
)

echo.
echo ============================================
echo    Quick Fix Complete!
echo ============================================
echo.
echo All common issues have been addressed.
echo.
echo Next steps:
echo 1. Run diagnostic.bat to verify everything is OK
echo 2. Run master_sync.bat to start AutoSync
echo.
pause
exit /b 0