@echo off
setlocal EnableDelayedExpansion

REM ==== MODULE: Web Deployment ====
REM Moves PHP projects from source to htdocs
REM Naming: {class}_{foldername} or just {foldername} if no parent
REM Args: %1 = config file, %2 = log file

set CONFIG_FILE=%~1
set LOGFILE=%~2

echo [%time%] ═══════════════════════════════════ >> "%LOGFILE%"
echo [%time%] WEB DEPLOYMENT MODULE START >> "%LOGFILE%"
echo [%time%] ═══════════════════════════════════ >> "%LOGFILE%"

REM Read web deploy config
for /f "usebackq tokens=1,2 delims==" %%a in ("%CONFIG_FILE%") do (
    set LINE=%%a
    set VALUE=%%b
    for /f "tokens=* delims= " %%x in ("!LINE!") do set LINE=%%x
    for /f "tokens=* delims= " %%x in ("!VALUE!") do set VALUE=%%x
    
    if "!LINE!"=="source" set WEB_SOURCE=!VALUE!
    if "!LINE!"=="destination" set WEB_DEST=!VALUE!
)

REM Defaults
if not defined WEB_SOURCE set WEB_SOURCE=E:\Pliki\Projects\websites
if not defined WEB_DEST set WEB_DEST=C:\xampp\htdocs\myfiles

REM Check if source exists
if not exist "%WEB_SOURCE%" (
    echo [%time%] ERROR: Web source not found: %WEB_SOURCE% >> "%LOGFILE%"
    exit /b 1
)

REM Create destination if doesn't exist
if not exist "%WEB_DEST%" (
    echo [%time%] Creating htdocs directory: %WEB_DEST% >> "%LOGFILE%"
    mkdir "%WEB_DEST%"
)

echo [%time%] Scanning for PHP projects in: %WEB_SOURCE% >> "%LOGFILE%"

set COUNT=0
set MOVED=0
set SKIPPED=0

REM Find all PHP files and process their parent directories
for /r "%WEB_SOURCE%" %%F in (*.php) do (
    set PHP_FILE=%%F
    call :PROCESS_PHP_PROJECT "!PHP_FILE!"
)

echo [%time%] ────────────────────────────────── >> "%LOGFILE%"
echo [%time%] Web Deployment Summary: >> "%LOGFILE%"
echo [%time%] Projects processed: %COUNT% >> "%LOGFILE%"
echo [%time%] Moved: %MOVED% >> "%LOGFILE%"
echo [%time%] Already in place: %SKIPPED% >> "%LOGFILE%"
echo [%time%] Web Deployment Module Complete >> "%LOGFILE%"
echo.
exit /b 0

REM ==== SUBROUTINES ====

:PROCESS_PHP_PROJECT
set PHP_FILE=%~1
set PHP_DIR=%~dp1
set PHP_DIR=!PHP_DIR:~0,-1!

REM Get project folder name
for %%A in ("!PHP_DIR!") do (
    set FOLDER_NAME=%%~nxA
    set PARENT_DIR=%%~dpA
)

REM Remove trailing backslash from parent
set PARENT_DIR=!PARENT_DIR:~0,-1!

REM Get class name (parent folder)
for %%B in ("!PARENT_DIR!") do set CLASS_NAME=%%~nxB

REM Check if folder is directly in SOURCE (no class prefix needed)
if /I "!PARENT_DIR!"=="%WEB_SOURCE%" (
    set TARGET=%WEB_DEST%\!FOLDER_NAME!
    set PREFIX_MODE=direct
) else (
    set TARGET=%WEB_DEST%\!CLASS_NAME!_!FOLDER_NAME!
    set PREFIX_MODE=prefixed
)

REM Check if we already processed this project
echo !PROCESSED_PROJECTS! | find "!PHP_DIR!" >nul
if not errorlevel 1 goto :EOF

REM Mark as processed
set PROCESSED_PROJECTS=!PROCESSED_PROJECTS! !PHP_DIR!
set /a COUNT+=1

REM Check if already in htdocs
if exist "!TARGET!" (
    echo [%time%] SKIP: !FOLDER_NAME! already in htdocs >> "%LOGFILE%"
    set /a SKIPPED+=1
    goto :EOF
)

REM Move project to htdocs
echo [%time%] MOVING: !PHP_DIR! >> "%LOGFILE%"
echo [%time%]    TO: !TARGET! >> "%LOGFILE%"

move "!PHP_DIR!" "!TARGET!" >nul 2>&1

if errorlevel 1 (
    echo [%time%] ERROR: Failed to move !FOLDER_NAME! >> "%LOGFILE%"
) else (
    echo [%time%] SUCCESS: !FOLDER_NAME! moved to htdocs >> "%LOGFILE%"
    set /a MOVED+=1
)

goto :EOF

endlocal
