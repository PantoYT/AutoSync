@echo off
setlocal EnableDelayedExpansion

REM ==========================================
REM USB SYNC MODULE - FIXED VERSION
REM ==========================================
REM FIXES:
REM - Corrected robocopy exit code logic
REM - Fixed double error/success logging
REM - Proper UTF-8 handling
REM ==========================================

REM Save current code page
for /f "tokens=2 delims=:" %%a in ('chcp') do set ORIGINAL_CP=%%a
set ORIGINAL_CP=%ORIGINAL_CP: =%

set CONFIG_FILE=%~1
set LOGFILE=%~2

REM ==========================================
REM READ CONFIG FIRST (in original codepage)
REM ==========================================

REM Read USB drive from config (BEFORE switching to UTF-8)
for /f "usebackq tokens=1,2 delims==" %%a in ("%CONFIG_FILE%") do (
    set LINE=%%a
    set VALUE=%%b
    for /f "tokens=* delims= " %%x in ("!LINE!") do set LINE=%%x
    for /f "tokens=* delims= " %%x in ("!VALUE!") do set VALUE=%%x
    if "!LINE!"=="drive" set USB_DRIVE=!VALUE!
)

REM ==========================================
REM NOW switch to UTF-8 for Polish filenames
REM ==========================================

REM Switch to UTF-8 (65001) for proper Polish character handling
chcp 65001 >nul 2>&1

echo ============================================
echo USB SYNC MODULE - FIXED VERSION
echo ============================================
echo.
echo Config: %CONFIG_FILE%
echo USB Drive: %USB_DRIVE%
echo Log: %LOGFILE%
echo.

echo [%time%] ======================================= >> "%LOGFILE%"
echo [%time%] USB SYNC MODULE START (FIXED) >> "%LOGFILE%"
echo [%time%] ======================================= >> "%LOGFILE%"
echo [%time%] Config: %CONFIG_FILE% >> "%LOGFILE%"
echo [%time%] USB Drive: %USB_DRIVE% >> "%LOGFILE%"
echo [%time%] UTF-8 enabled for Polish characters >> "%LOGFILE%"

REM Verify USB drive is accessible
if not exist "%USB_DRIVE%\" (
    echo ============================================
    echo ERROR: USB drive %USB_DRIVE% not accessible!
    echo ============================================
    echo.
    echo [%time%] ERROR: USB drive %USB_DRIVE% not accessible! >> "%LOGFILE%"
    chcp %ORIGINAL_CP% >nul 2>&1
    exit /b 1
)

REM Initialize counters
set PHASE1_SUCCESS=0
set PHASE1_FAILED=0
set PHASE2_SUCCESS=0
set PHASE2_FAILED=0
set PHASE2_SKIPPED=0

REM ==========================================
REM PHASE 1: LOCAL TO USB (MIRROR MODE)
REM ==========================================
echo ============================================
echo PHASE 1: LOCAL -^> USB (MIRROR MODE)
echo ============================================
echo.

echo [%time%] ======================================= >> "%LOGFILE%"
echo [%time%] PHASE 1: LOCAL -^> USB (MIRROR MODE) >> "%LOGFILE%"
echo [%time%] ======================================= >> "%LOGFILE%"

echo [1/3] Syncing apps...
echo [%time%] Syncing apps... >> "%LOGFILE%"
call :SYNC_MIRROR "apps"

echo [2/3] Syncing AutoHotkey scripts...
echo [%time%] Syncing AutoHotkey scripts... >> "%LOGFILE%"
call :SYNC_MIRROR "ahk"

echo [3/3] Syncing general scripts...
echo [%time%] Syncing general scripts... >> "%LOGFILE%"
call :SYNC_MIRROR "scripts"

echo.
echo Phase 1 Complete: Success=%PHASE1_SUCCESS% Failed=%PHASE1_FAILED%
echo.

echo [%time%] --------------------------------------- >> "%LOGFILE%"
echo [%time%] Phase 1 Summary: >> "%LOGFILE%"
echo [%time%] Success: %PHASE1_SUCCESS% >> "%LOGFILE%"
echo [%time%] Failed: %PHASE1_FAILED% >> "%LOGFILE%"
echo [%time%] --------------------------------------- >> "%LOGFILE%"

REM ==========================================
REM PHASE 2: USB TO LOCAL (COMPLETE SYNC)
REM ==========================================
echo ============================================
echo PHASE 2: USB -^> LOCAL (COMPLETE SYNC)
echo ============================================
echo.

echo [%time%] ======================================= >> "%LOGFILE%"
echo [%time%] PHASE 2: USB -^> LOCAL (COMPLETE SYNC) >> "%LOGFILE%"
echo [%time%] ======================================= >> "%LOGFILE%"

echo Syncing school subjects...
echo [%time%] Syncing school subjects... >> "%LOGFILE%"

echo [1/8] Databases (db)...
echo [%time%] [Subject] Databases (db)... >> "%LOGFILE%"
call :SYNC_SUBJECT "db"

echo [2/8] C++ (cpp)...
echo [%time%] [Language] C++ (cpp)... >> "%LOGFILE%"
call :SYNC_SUBJECT "cpp"

echo [3/8] Python (python)...
echo [%time%] [Language] Python (python)... >> "%LOGFILE%"
call :SYNC_SUBJECT "python"

echo [4/8] Web development (web)...
echo [%time%] [Subject] Web development (web)... >> "%LOGFILE%"
call :SYNC_SUBJECT "web"

echo [5/8] BHP (bhp)...
echo [%time%] [Subject] BHP (bhp)... >> "%LOGFILE%"
call :SYNC_SUBJECT "bhp"

echo [6/8] Podstawy Informatyki (pod_inf)...
echo [%time%] [Subject] Podstawy Informatyki (pod_inf)... >> "%LOGFILE%"
call :SYNC_SUBJECT "pod_inf"

echo [7/8] Informatyka (informatyka)...
echo [%time%] [Subject] Informatyka (informatyka)... >> "%LOGFILE%"
call :SYNC_SUBJECT "informatyka"

echo [8/8] Przygotowanie (przygot)...
echo [%time%] [Subject] Przygotowanie (przygot)... >> "%LOGFILE%"
call :SYNC_SUBJECT "przygot"

echo.
echo Phase 2 Complete: Success=%PHASE2_SUCCESS% Failed=%PHASE2_FAILED% Skipped=%PHASE2_SKIPPED%
echo.

echo [%time%] --------------------------------------- >> "%LOGFILE%"
echo [%time%] Phase 2 Summary: >> "%LOGFILE%"
echo [%time%] Success: %PHASE2_SUCCESS% >> "%LOGFILE%"
echo [%time%] Failed: %PHASE2_FAILED% >> "%LOGFILE%"
echo [%time%] Skipped (not found): %PHASE2_SKIPPED% >> "%LOGFILE%"
echo [%time%] --------------------------------------- >> "%LOGFILE%"

REM ==========================================
REM FINAL SUMMARY
REM ==========================================
echo ============================================
echo SYNC COMPLETE
echo ============================================

echo [%time%] ======================================= >> "%LOGFILE%"
echo [%time%] USB SYNC MODULE COMPLETE >> "%LOGFILE%"
echo [%time%] ======================================= >> "%LOGFILE%"

set /a TOTAL_SUCCESS=%PHASE1_SUCCESS%+%PHASE2_SUCCESS%
set /a TOTAL_FAILED=%PHASE1_FAILED%+%PHASE2_FAILED%

echo Total Success: %TOTAL_SUCCESS%
echo Total Failed: %TOTAL_FAILED%
echo.

echo [%time%] Total Success: %TOTAL_SUCCESS% >> "%LOGFILE%"
echo [%time%] Total Failed: %TOTAL_FAILED% >> "%LOGFILE%"
echo [%time%] ======================================= >> "%LOGFILE%"

REM Restore original code page
chcp %ORIGINAL_CP% >nul 2>&1

if %TOTAL_FAILED% GTR 0 (
    exit /b 1
) else (
    exit /b 0
)

REM ==========================================
REM SUBROUTINE: SYNC_MIRROR
REM ==========================================
:SYNC_MIRROR
set KEY=%~1
set SRC=
set DST=

REM Temporarily switch back to original codepage for config reading
chcp %ORIGINAL_CP% >nul 2>&1

REM Read source and destination from config
for /f "usebackq tokens=1,2 delims==" %%a in ("%CONFIG_FILE%") do (
    set LINE=%%a
    set VALUE=%%b
    for /f "tokens=* delims= " %%x in ("!LINE!") do set LINE=%%x
    for /f "tokens=* delims= " %%x in ("!VALUE!") do set VALUE=%%x
    
    if "!LINE!"=="%KEY%_src" set SRC=!VALUE!
    if "!LINE!"=="%KEY%_dst" (
        set DST=!VALUE!
        set DST=!DST:{USB}=%USB_DRIVE%!
    )
)

REM Switch back to UTF-8
chcp 65001 >nul 2>&1

REM Validate paths
if not defined SRC (
    echo   WARNING: No source defined for %KEY%
    echo [%time%] WARNING: No source defined for %KEY% >> "%LOGFILE%"
    goto :EOF
)
if not defined DST (
    echo   WARNING: No destination defined for %KEY%
    echo [%time%] WARNING: No destination defined for %KEY% >> "%LOGFILE%"
    goto :EOF
)

if not exist "%SRC%" (
    echo   SKIP: Source not found: %SRC%
    echo [%time%] SKIP: Source not found: %SRC% >> "%LOGFILE%"
    set /a PHASE1_FAILED+=1
    goto :EOF
)

echo   Mirroring: %SRC%
echo             -^> %DST%

echo [%time%] MIRROR: %SRC% >> "%LOGFILE%"
echo [%time%]     -^> %DST% >> "%LOGFILE%"

REM Run robocopy and capture exit code
robocopy "%SRC%" "%DST%" /MIR /R:2 /W:3 /NFL /NDL /NJH /NJS /MT:2 /LEV:10 /XJ /XJD /UNICODE >> "%LOGFILE%" 2>&1
set ROBO_EXIT=!ERRORLEVEL!

REM FIXED: Robocopy exit codes 0-7 = success, 8+ = errors
if !ROBO_EXIT! GEQ 8 (
    echo   ERROR: Mirror failed (code: !ROBO_EXIT!)
    echo [%time%] ERROR: Mirror failed for %KEY% (code: !ROBO_EXIT!) >> "%LOGFILE%"
    set /a PHASE1_FAILED+=1
) else (
    echo   SUCCESS (code: !ROBO_EXIT!)
    echo [%time%] SUCCESS: %KEY% mirrored (code: !ROBO_EXIT!) >> "%LOGFILE%"
    set /a PHASE1_SUCCESS+=1
)
echo.
goto :EOF

REM ==========================================
REM SUBROUTINE: SYNC_SUBJECT (UNIFIED)
REM ==========================================
:SYNC_SUBJECT
set SUBJECT=%~1
set SUBJ_SRC=
set SUBJ_DST=

REM Temporarily switch back to original codepage for config reading
chcp %ORIGINAL_CP% >nul 2>&1

REM Read subject paths from config
for /f "usebackq tokens=1,2 delims==" %%a in ("%CONFIG_FILE%") do (
    set LINE=%%a
    set VALUE=%%b
    for /f "tokens=* delims= " %%x in ("!LINE!") do set LINE=%%x
    for /f "tokens=* delims= " %%x in ("!VALUE!") do set VALUE=%%x
    
    if "!LINE!"=="%SUBJECT%_src" (
        set SUBJ_SRC=!VALUE!
        set SUBJ_SRC=!SUBJ_SRC:{USB}=%USB_DRIVE%!
    )
    if "!LINE!"=="%SUBJECT%_dst" set SUBJ_DST=!VALUE!
)

REM Switch back to UTF-8
chcp 65001 >nul 2>&1

REM Validate paths
if not defined SUBJ_SRC (
    echo   Config missing: %SUBJECT%_src
    goto :EOF
)
if not defined SUBJ_DST (
    echo   Config missing: %SUBJECT%_dst
    goto :EOF
)

echo   Checking: %SUBJ_SRC%

echo [%time%] Checking: %SUBJ_SRC% >> "%LOGFILE%"

if not exist "%SUBJ_SRC%" (
    echo   Not found (skipping)
    echo [%time%] INFO: Subject folder not found (skipping): %SUBJECT% >> "%LOGFILE%"
    set /a PHASE2_SKIPPED+=1
    goto :EOF
)

REM Track if we synced anything
set ANYTHING_SYNCED=0

REM ==========================================
REM Sync klasaX folders (klasa1-5)
REM ==========================================
echo   Scanning klasa folders...
echo [%time%] Scanning for klasa folders... >> "%LOGFILE%"

for %%k in (klasa1 klasa2 klasa3 klasa4 klasa5) do (
    set KLASA_SRC=%SUBJ_SRC%\%%k
    set KLASA_DST=%SUBJ_DST%\%%k
    
    if exist "!KLASA_SRC!" (
        echo   Found: %%k
        echo [%time%] FOUND: %%k for %SUBJECT% >> "%LOGFILE%"
        
        REM Ensure destination exists
        if not exist "!KLASA_DST!" (
            echo   Creating: !KLASA_DST!
            echo [%time%] Creating destination: !KLASA_DST! >> "%LOGFILE%"
            mkdir "!KLASA_DST!" 2>nul
        )
        
        echo   Syncing: !KLASA_SRC! -^> !KLASA_DST!
        echo [%time%] MIRROR: !KLASA_SRC! >> "%LOGFILE%"
        echo [%time%]     -^> !KLASA_DST! >> "%LOGFILE%"
        
        robocopy "!KLASA_SRC!" "!KLASA_DST!" /MIR /LEV:10 /R:1 /W:2 /XJ /XJD /NFL /NDL /NJH /NJS /MT:2 /UNICODE >> "%LOGFILE%" 2>&1
        
        set ROBO_EXIT=!ERRORLEVEL!
        
        REM FIXED: Proper exit code checking
        if !ROBO_EXIT! GEQ 8 (
            echo   ERROR syncing %%k (code: !ROBO_EXIT!)
            echo [%time%] ERROR: Failed to sync %SUBJECT%\%%k (exit code: !ROBO_EXIT!) >> "%LOGFILE%"
            set /a PHASE2_FAILED+=1
        ) else (
            echo   SUCCESS %%k (code: !ROBO_EXIT!)
            echo [%time%] SUCCESS: %SUBJECT%\%%k synced (exit code: !ROBO_EXIT!) >> "%LOGFILE%"
            set /a PHASE2_SUCCESS+=1
            set ANYTHING_SYNCED=1
        )
    )
)

REM ==========================================
REM Sync standalone project folders
REM ==========================================
echo   Scanning standalone projects...
echo [%time%] Scanning for standalone projects in %SUBJECT%... >> "%LOGFILE%"

set FOLDER_COUNT=0

for /d %%P in ("%SUBJ_SRC%\*") do (
    set /a FOLDER_COUNT+=1
    set PROJECT_NAME=%%~nxP
    
    REM Skip if it's a klasa folder
    set IS_KLASA=0
    for %%k in (klasa1 klasa2 klasa3 klasa4 klasa5) do (
        if /i "!PROJECT_NAME!"=="%%k" set IS_KLASA=1
    )
    
    if !IS_KLASA! EQU 0 (
        set PROJECT_SRC=%%P
        set PROJECT_DST=%SUBJ_DST%\!PROJECT_NAME!
        
        echo   Found project: !PROJECT_NAME!
        echo [%time%] FOUND: Standalone project "!PROJECT_NAME!" in %SUBJECT% >> "%LOGFILE%"
        
        if not exist "!PROJECT_DST!" (
            echo   Creating: !PROJECT_DST!
            echo [%time%] Creating destination: !PROJECT_DST! >> "%LOGFILE%"
            mkdir "!PROJECT_DST!" 2>nul
        )
        
        echo   Syncing: !PROJECT_SRC! -^> !PROJECT_DST!
        echo [%time%] MIRROR: !PROJECT_SRC! >> "%LOGFILE%"
        echo [%time%]     -^> !PROJECT_DST! >> "%LOGFILE%"
        
        robocopy "!PROJECT_SRC!" "!PROJECT_DST!" /MIR /LEV:10 /R:1 /W:2 /XJ /XJD /NFL /NDL /NJH /NJS /MT:2 /UNICODE >> "%LOGFILE%" 2>&1
        
        set ROBO_EXIT=!ERRORLEVEL!
        
        REM FIXED: Proper exit code checking
        if !ROBO_EXIT! GEQ 8 (
            echo   ERROR syncing !PROJECT_NAME! (code: !ROBO_EXIT!)
            echo [%time%] ERROR: Failed to sync %SUBJECT%\!PROJECT_NAME! (exit code: !ROBO_EXIT!) >> "%LOGFILE%"
            set /a PHASE2_FAILED+=1
        ) else (
            echo   SUCCESS !PROJECT_NAME! (code: !ROBO_EXIT!)
            echo [%time%] SUCCESS: %SUBJECT%\!PROJECT_NAME! synced (exit code: !ROBO_EXIT!) >> "%LOGFILE%"
            set /a PHASE2_SUCCESS+=1
            set ANYTHING_SYNCED=1
        )
    )
)

echo   Total folders scanned: !FOLDER_COUNT!
echo [%time%] Scanned %SUBJECT%: !FOLDER_COUNT! folders total >> "%LOGFILE%"

if !ANYTHING_SYNCED! EQU 0 (
    echo   No folders synced
    echo [%time%] INFO: No folders synced for %SUBJECT% >> "%LOGFILE%"
    set /a PHASE2_SKIPPED+=1
)

echo.
goto :EOF

endlocal