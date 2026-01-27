@echo off
setlocal EnableDelayedExpansion

REM ==== MODULE: USB Sync ====
REM Handles E: ↔ USB bidirectional sync
REM Args: %1 = config file, %2 = log file

set CONFIG_FILE=%~1
set LOGFILE=%~2

echo [%time%] ═══════════════════════════════════ >> "%LOGFILE%"
echo [%time%] USB SYNC MODULE START >> "%LOGFILE%"
echo [%time%] ═══════════════════════════════════ >> "%LOGFILE%"

REM Read USB drive from config
for /f "usebackq tokens=1,2 delims==" %%a in ("%CONFIG_FILE%") do (
    set LINE=%%a
    set VALUE=%%b
    for /f "tokens=* delims= " %%x in ("!LINE!") do set LINE=%%x
    for /f "tokens=* delims= " %%x in ("!VALUE!") do set VALUE=%%x
    if "!LINE!"=="drive" set USB_DRIVE=!VALUE!
)

REM ==== PHASE 1: LOCAL → USB (MIRROR MODE) ====
echo [%time%] Phase 1: Syncing LOCAL to USB (MIRROR MODE) >> "%LOGFILE%"

call :SYNC_MIRROR "apps"
call :SYNC_MIRROR "ahk"
call :SYNC_MIRROR "scripts"

REM ==== PHASE 2: USB → LOCAL (STANDARD MODE) ====
echo [%time%] Phase 2: Syncing USB to LOCAL (STANDARD MODE) >> "%LOGFILE%"

call :SYNC_STANDARD "db"
call :SYNC_STANDARD "cpp"
call :SYNC_STANDARD "python"
call :SYNC_STANDARD "web"
call :SYNC_STANDARD "bhp"
call :SYNC_STANDARD "pod_inf"
call :SYNC_STANDARD "informatyka"
call :SYNC_STANDARD "przygot"

echo [%time%] USB Sync Module Complete >> "%LOGFILE%"
echo.
exit /b 0

REM ==== SUBROUTINES ====

:SYNC_MIRROR
set KEY=%~1
set SRC=
set DST=

REM Read source and destination from config
for /f "usebackq tokens=1,2 delims==" %%a in ("%CONFIG_FILE%") do (
    set LINE=%%a
    set VALUE=%%b
    for /f "tokens=* delims= " %%x in ("!LINE!") do set LINE=%%x
    for /f "tokens=* delims= " %%x in ("!VALUE!") do set VALUE=%%x
    
    if "!LINE!"=="%KEY%_src" set SRC=!VALUE!
    if "!LINE!"=="%KEY%_dst" (
        set DST=!VALUE!
        REM Replace {USB} placeholder
        set DST=!DST:{USB}=%USB_DRIVE%!
    )
)

if not defined SRC goto :EOF
if not defined DST goto :EOF

if not exist "%SRC%" (
    echo [%time%] WARNING: Source not found: %SRC% >> "%LOGFILE%"
    goto :EOF
)

echo [%time%] MIRROR: %SRC% -^> %DST% >> "%LOGFILE%"
robocopy "%SRC%" "%DST%" /MIR /R:3 /W:5 /NFL /NDL /NJH /NJS >> "%LOGFILE%" 2>&1

if errorlevel 8 (
    echo [%time%] ERROR: Mirror failed for %KEY% >> "%LOGFILE%"
    exit /b 1
) else (
    echo [%time%] SUCCESS: %KEY% mirrored >> "%LOGFILE%"
)

goto :EOF

:SYNC_STANDARD
set KEY=%~1
set SRC=
set DST=

REM Read source and destination from config
for /f "usebackq tokens=1,2 delims==" %%a in ("%CONFIG_FILE%") do (
    set LINE=%%a
    set VALUE=%%b
    for /f "tokens=* delims= " %%x in ("!LINE!") do set LINE=%%x
    for /f "tokens=* delims= " %%x in ("!VALUE!") do set VALUE=%%x
    
    if "!LINE!"=="%KEY%_src" (
        set SRC=!VALUE!
        REM Replace {USB} placeholder
        set SRC=!SRC:{USB}=%USB_DRIVE%!
    )
    if "!LINE!"=="%KEY%_dst" set DST=!VALUE!
)

if not defined SRC goto :EOF
if not defined DST goto :EOF

if not exist "%SRC%" (
    echo [%time%] WARNING: Source not found: %SRC% >> "%LOGFILE%"
    goto :EOF
)

echo [%time%] SYNC: %SRC% -^> %DST% >> "%LOGFILE%"
robocopy "%SRC%" "%DST%" /E /R:3 /W:5 /NFL /NDL /NJH /NJS >> "%LOGFILE%" 2>&1

if errorlevel 8 (
    echo [%time%] ERROR: Sync failed for %KEY% >> "%LOGFILE%"
    exit /b 1
) else (
    echo [%time%] SUCCESS: %KEY% synced >> "%LOGFILE%"
)

goto :EOF

endlocal
