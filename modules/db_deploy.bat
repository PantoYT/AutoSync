@echo off
setlocal EnableDelayedExpansion

REM ==== MODULE: Database Deployment ====
REM Scans for .sql files and creates/imports them into MySQL
REM Database names: {class}_{filename}
REM Args: %1 = config file, %2 = log file

set CONFIG_FILE=%~1
set LOGFILE=%~2

echo [%time%] ═══════════════════════════════════ >> "%LOGFILE%"
echo [%time%] DATABASE DEPLOYMENT MODULE START >> "%LOGFILE%"
echo [%time%] ═══════════════════════════════════ >> "%LOGFILE%"

REM Read MySQL config
for /f "usebackq tokens=1,2 delims==" %%a in ("%CONFIG_FILE%") do (
    set LINE=%%a
    set VALUE=%%b
    for /f "tokens=* delims= " %%x in ("!LINE!") do set LINE=%%x
    for /f "tokens=* delims= " %%x in ("!VALUE!") do set VALUE=%%x
    
    if "!LINE!"=="bin" set MYSQL_BIN=!VALUE!
    if "!LINE!"=="user" set MYSQL_USER=!VALUE!
    if "!LINE!"=="pass" set MYSQL_PASS=!VALUE!
    if "!LINE!"=="sql_base" set SQL_BASE=!VALUE!
    if "!LINE!"=="charset" set CHARSET=!VALUE!
)

REM Defaults
if not defined MYSQL_BIN set MYSQL_BIN=C:\xampp\mysql\bin\mysql.exe
if not defined MYSQL_USER set MYSQL_USER=root
if not defined MYSQL_PASS set MYSQL_PASS=
if not defined SQL_BASE set SQL_BASE=E:\Pliki\Projects\databases
if not defined CHARSET set CHARSET=utf8mb4

REM Check if MySQL exists
if not exist "%MYSQL_BIN%" (
    echo [%time%] ERROR: MySQL not found at: %MYSQL_BIN% >> "%LOGFILE%"
    echo [%time%] Skipping database deployment >> "%LOGFILE%"
    exit /b 1
)

REM Check if SQL base directory exists
if not exist "%SQL_BASE%" (
    echo [%time%] ERROR: SQL base directory not found: %SQL_BASE% >> "%LOGFILE%"
    exit /b 1
)

echo [%time%] Scanning for .sql files in: %SQL_BASE% >> "%LOGFILE%"

set COUNT=0
set SUCCESS=0
set FAILED=0

REM Scan all .sql files recursively
for /r "%SQL_BASE%" %%F in (*.sql) do (
    set /a COUNT+=1
    call :DEPLOY_SQL "%%F"
)

echo [%time%] ────────────────────────────────── >> "%LOGFILE%"
echo [%time%] Database Deployment Summary: >> "%LOGFILE%"
echo [%time%] Total SQL files: %COUNT% >> "%LOGFILE%"
echo [%time%] Successfully deployed: %SUCCESS% >> "%LOGFILE%"
echo [%time%] Failed: %FAILED% >> "%LOGFILE%"
echo [%time%] Database Deployment Module Complete >> "%LOGFILE%"
echo.
exit /b 0

REM ==== SUBROUTINES ====

:DEPLOY_SQL
set FILE=%~1
set FILENAME=%~n1

REM Get relative path from SQL_BASE
set REL_PATH=%FILE%
set REL_PATH=!REL_PATH:%SQL_BASE%\=!

REM Extract class name (first directory in path)
for /f "tokens=1 delims=\" %%K in ("!REL_PATH!") do set CLASS=%%K

REM Build final database name: {class}_{filename}
set DB_NAME=!CLASS!_!FILENAME!

REM Remove spaces and special characters from DB name
set DB_NAME=!DB_NAME: =_!
set DB_NAME=!DB_NAME:-=_!

echo [%time%] Deploying: !FILE! >> "%LOGFILE%"
echo [%time%]   - Database: !DB_NAME! >> "%LOGFILE%"
echo [%time%]   - Class: !CLASS! >> "%LOGFILE%"

REM Drop and create database
"%MYSQL_BIN%" -u %MYSQL_USER% %MYSQL_PASS% -e "DROP DATABASE IF EXISTS `!DB_NAME!`; CREATE DATABASE `!DB_NAME!` CHARACTER SET %CHARSET%;" >> "%LOGFILE%" 2>&1

if errorlevel 1 (
    echo [%time%] ERROR: Failed to create database: !DB_NAME! >> "%LOGFILE%"
    set /a FAILED+=1
    goto :EOF
)

REM Import SQL file
"%MYSQL_BIN%" -u %MYSQL_USER% %MYSQL_PASS% "!DB_NAME!" < "!FILE!" >> "%LOGFILE%" 2>&1

if errorlevel 1 (
    echo [%time%] ERROR: Failed to import: !FILE! >> "%LOGFILE%"
    set /a FAILED+=1
) else (
    echo [%time%] SUCCESS: !DB_NAME! deployed >> "%LOGFILE%"
    set /a SUCCESS+=1
)

goto :EOF

endlocal
