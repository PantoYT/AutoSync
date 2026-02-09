@echo off
setlocal EnableDelayedExpansion

REM ==========================================
REM USB SYNC MODULE - COMPLETE VERSION
REM ==========================================
REM Features:
REM 1. Syncs klasaX folders (klasa1-5)
REM 2. Syncs standalone project folders
REM 3. UTF-8 support for Polish characters
REM 4. Timeout protection (90 seconds)
REM 5. Depth limiting and junction exclusion
REM ==========================================

REM Save current code page
for /f "tokens=2 delims=:" %%a in ('chcp') do set ORIGINAL_CP=%%a
set ORIGINAL_CP=%ORIGINAL_CP: =%

REM Switch to UTF-8 (65001) for proper Polish character handling
chcp 65001 >nul 2>&1

set CONFIG_FILE=%~1
set LOGFILE=%~2

echo [%time%] ======================================= >> "%LOGFILE%"
echo [%time%] USB SYNC MODULE START (COMPLETE) >> "%LOGFILE%"
echo [%time%] ======================================= >> "%LOGFILE%"
echo [%time%] UTF-8 enabled for Polish characters >> "%LOGFILE%"

REM Read USB drive from config
for /f "usebackq tokens=1,2 delims==" %%a in ("%CONFIG_FILE%") do (
    set LINE=%%a
    set VALUE=%%b
    for /f "tokens=* delims= " %%x in ("!LINE!") do set LINE=%%x
    for /f "tokens=* delims= " %%x in ("!VALUE!") do set VALUE=%%x
    if "!LINE!"=="drive" set USB_DRIVE=!VALUE!
)

REM Verify USB drive is accessible
if not exist "%USB_DRIVE%\" (
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
echo [%time%] ======================================= >> "%LOGFILE%"
echo [%time%] PHASE 1: LOCAL -^> USB (MIRROR MODE) >> "%LOGFILE%"
echo [%time%] ======================================= >> "%LOGFILE%"

echo [%time%] Syncing apps... >> "%LOGFILE%"
call :SYNC_MIRROR "apps"

echo [%time%] Syncing AutoHotkey scripts... >> "%LOGFILE%"
call :SYNC_MIRROR "ahk"

echo [%time%] Syncing general scripts... >> "%LOGFILE%"
call :SYNC_MIRROR "scripts"

echo [%time%] --------------------------------------- >> "%LOGFILE%"
echo [%time%] Phase 1 Summary: >> "%LOGFILE%"
echo [%time%] Success: %PHASE1_SUCCESS% >> "%LOGFILE%"
echo [%time%] Failed: %PHASE1_FAILED% >> "%LOGFILE%"
echo [%time%] --------------------------------------- >> "%LOGFILE%"

REM ==========================================
REM PHASE 2: USB TO LOCAL (COMPLETE SYNC)
REM ==========================================
echo [%time%] ======================================= >> "%LOGFILE%"
echo [%time%] PHASE 2: USB -^> LOCAL (COMPLETE SYNC) >> "%LOGFILE%"
echo [%time%] ======================================= >> "%LOGFILE%"

echo [%time%] Syncing school subjects... >> "%LOGFILE%"

echo [%time%] [Subject] Databases (db)... >> "%LOGFILE%"
call :SYNC_SUBJECT_COMPLETE "db"

echo [%time%] [Language] C++ (cpp)... >> "%LOGFILE%"
call :SYNC_LANGUAGE_COMPLETE "cpp"

echo [%time%] [Language] Python (python)... >> "%LOGFILE%"
call :SYNC_LANGUAGE_COMPLETE "python"

echo [%time%] [Subject] Web development (web)... >> "%LOGFILE%"
call :SYNC_SUBJECT_COMPLETE "web"

echo [%time%] [Subject] BHP (bhp)... >> "%LOGFILE%"
call :SYNC_SUBJECT_COMPLETE "bhp"

echo [%time%] [Subject] Podstawy Informatyki (pod_inf)... >> "%LOGFILE%"
call :SYNC_SUBJECT_COMPLETE "pod_inf"

echo [%time%] [Subject] Informatyka (informatyka)... >> "%LOGFILE%"
call :SYNC_SUBJECT_COMPLETE "informatyka"

echo [%time%] [Subject] Przygotowanie (przygot)... >> "%LOGFILE%"
call :SYNC_SUBJECT_COMPLETE "przygot"

echo [%time%] --------------------------------------- >> "%LOGFILE%"
echo [%time%] Phase 2 Summary: >> "%LOGFILE%"
echo [%time%] Success: %PHASE2_SUCCESS% >> "%LOGFILE%"
echo [%time%] Failed: %PHASE2_FAILED% >> "%LOGFILE%"
echo [%time%] Skipped (not found): %PHASE2_SKIPPED% >> "%LOGFILE%"
echo [%time%] --------------------------------------- >> "%LOGFILE%"

REM ==========================================
REM FINAL SUMMARY
REM ==========================================
echo [%time%] ======================================= >> "%LOGFILE%"
echo [%time%] USB SYNC MODULE COMPLETE >> "%LOGFILE%"
echo [%time%] ======================================= >> "%LOGFILE%"

set /a TOTAL_SUCCESS=%PHASE1_SUCCESS%+%PHASE2_SUCCESS%
set /a TOTAL_FAILED=%PHASE1_FAILED%+%PHASE2_FAILED%

echo [%time%] Total Success: %TOTAL_SUCCESS% >> "%LOGFILE%"
echo [%time%] Total Failed: %TOTAL_FAILED% >> "%LOGFILE%"
echo [%time%] ======================================= >> "%LOGFILE%"
echo.

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

REM Validate paths
if not defined SRC (
    echo [%time%] WARNING: No source defined for %KEY% >> "%LOGFILE%"
    goto :EOF
)
if not defined DST (
    echo [%time%] WARNING: No destination defined for %KEY% >> "%LOGFILE%"
    goto :EOF
)

if not exist "%SRC%" (
    echo [%time%] SKIP: Source not found: %SRC% >> "%LOGFILE%"
    set /a PHASE1_FAILED+=1
    goto :EOF
)

echo [%time%] MIRROR: %SRC% >> "%LOGFILE%"
echo [%time%]     -^> %DST% >> "%LOGFILE%"

REM Run robocopy with timeout protection
robocopy "%SRC%" "%DST%" /MIR /R:2 /W:3 /NFL /NDL /NJH /NJS /MT:2 /LEV:10 /XJ /XJD /UNICODE >> "%LOGFILE%" 2>&1

REM Robocopy exit codes: 0-7 = success, 8+ = errors
if errorlevel 8 (
    echo [%time%] ERROR: Mirror failed for %KEY% >> "%LOGFILE%"
    set /a PHASE1_FAILED+=1
) else (
    echo [%time%] SUCCESS: %KEY% mirrored (code: !ERRORLEVEL!) >> "%LOGFILE%"
    set /a PHASE1_SUCCESS+=1
)
goto :EOF

REM ==========================================
REM SUBROUTINE: SYNC_SUBJECT_COMPLETE
REM Syncs BOTH klasaX folders AND standalone projects
REM ==========================================
:SYNC_SUBJECT_COMPLETE
set SUBJECT=%~1
set SUBJ_SRC=
set SUBJ_DST=

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

REM Validate paths
if not defined SUBJ_SRC goto :EOF
if not defined SUBJ_DST goto :EOF

echo [%time%] Checking: %SUBJ_SRC% >> "%LOGFILE%"

if not exist "%SUBJ_SRC%" (
    echo [%time%] INFO: Subject folder not found (skipping): %SUBJECT% >> "%LOGFILE%"
    set /a PHASE2_SKIPPED+=1
    goto :EOF
)

REM Track if we synced anything
set ANYTHING_SYNCED=0

REM ==========================================
REM PART 1: Sync klasaX folders (klasa1-5)
REM ==========================================
echo [%time%] Scanning for klasa folders... >> "%LOGFILE%"

for %%k in (klasa1 klasa2 klasa3 klasa4 klasa5) do (
    set KLASA_SRC=%SUBJ_SRC%\%%k
    set KLASA_DST=%SUBJ_DST%\%%k
    
    if exist "!KLASA_SRC!" (
        echo [%time%] FOUND: %%k for %SUBJECT% >> "%LOGFILE%"
        
        REM Ensure destination exists
        if not exist "!KLASA_DST!" (
            echo [%time%] Creating destination: !KLASA_DST! >> "%LOGFILE%"
            mkdir "!KLASA_DST!" 2>nul
        )
        
        echo [%time%] MIRROR: !KLASA_SRC! >> "%LOGFILE%"
        echo [%time%]     -^> !KLASA_DST! >> "%LOGFILE%"
        
        REM Sync with robocopy
        call :SYNC_WITH_TIMEOUT "!KLASA_SRC!" "!KLASA_DST!" "%SUBJECT%\%%k"
        
        if !SYNC_RESULT! EQU 0 (
            set ANYTHING_SYNCED=1
        )
    ) else (
        echo [%time%] INFO: %%k not found for %SUBJECT% >> "%LOGFILE%"
    )
)

REM ==========================================
REM PART 2: Sync standalone project folders
REM ==========================================
echo [%time%] Scanning for standalone projects in %SUBJECT%... >> "%LOGFILE%"

REM Get all subdirectories in the subject folder
for /d %%P in ("%SUBJ_SRC%\*") do (
    set PROJECT_NAME=%%~nxP
    
    REM Skip if it's a klasa folder (already handled above)
    set IS_KLASA=0
    for %%k in (klasa1 klasa2 klasa3 klasa4 klasa5) do (
        if /i "!PROJECT_NAME!"=="%%k" set IS_KLASA=1
    )
    
    REM If not a klasa folder, it's a standalone project
    if !IS_KLASA! EQU 0 (
        set PROJECT_SRC=%%P
        set PROJECT_DST=%SUBJ_DST%\!PROJECT_NAME!
        
        echo [%time%] FOUND: Standalone project "!PROJECT_NAME!" in %SUBJECT% >> "%LOGFILE%"
        
        REM Ensure destination exists
        if not exist "!PROJECT_DST!" (
            echo [%time%] Creating destination: !PROJECT_DST! >> "%LOGFILE%"
            mkdir "!PROJECT_DST!" 2>nul
        )
        
        echo [%time%] MIRROR: !PROJECT_SRC! >> "%LOGFILE%"
        echo [%time%]     -^> !PROJECT_DST! >> "%LOGFILE%"
        
        REM Sync with robocopy
        call :SYNC_WITH_TIMEOUT "!PROJECT_SRC!" "!PROJECT_DST!" "%SUBJECT%\!PROJECT_NAME!"
        
        if !SYNC_RESULT! EQU 0 (
            set ANYTHING_SYNCED=1
        )
    )
)

REM Final status for this subject
if !ANYTHING_SYNCED! EQU 0 (
    echo [%time%] INFO: No folders found for %SUBJECT% >> "%LOGFILE%"
    set /a PHASE2_SKIPPED+=1
)

goto :EOF

REM ==========================================
REM SUBROUTINE: SYNC_LANGUAGE_COMPLETE
REM Same as SYNC_SUBJECT_COMPLETE but for languages
REM ==========================================
:SYNC_LANGUAGE_COMPLETE
set LANG=%~1
set LANG_SRC=
set LANG_DST=

REM Read language paths from config
for /f "usebackq tokens=1,2 delims==" %%a in ("%CONFIG_FILE%") do (
    set LINE=%%a
    set VALUE=%%b
    for /f "tokens=* delims= " %%x in ("!LINE!") do set LINE=%%x
    for /f "tokens=* delims= " %%x in ("!VALUE!") do set VALUE=%%x
    
    if "!LINE!"=="%LANG%_src" (
        set LANG_SRC=!VALUE!
        set LANG_SRC=!LANG_SRC:{USB}=%USB_DRIVE%!
    )
    if "!LINE!"=="%LANG%_dst" set LANG_DST=!VALUE!
)

REM Validate paths
if not defined LANG_SRC goto :EOF
if not defined LANG_DST goto :EOF

echo [%time%] Checking: %LANG_SRC% >> "%LOGFILE%"

if not exist "%LANG_SRC%" (
    echo [%time%] INFO: Language folder not found (skipping): %LANG% >> "%LOGFILE%"
    set /a PHASE2_SKIPPED+=1
    goto :EOF
)

REM Track if we synced anything
set ANYTHING_SYNCED=0

REM ==========================================
REM PART 1: Sync klasaX folders (klasa1-5)
REM ==========================================
echo [%time%] Scanning for klasa folders... >> "%LOGFILE%"

for %%k in (klasa1 klasa2 klasa3 klasa4 klasa5) do (
    set KLASA_SRC=%LANG_SRC%\%%k
    set KLASA_DST=%LANG_DST%\%%k
    
    if exist "!KLASA_SRC!" (
        echo [%time%] FOUND: %%k for %LANG% >> "%LOGFILE%"
        
        REM Ensure destination exists
        if not exist "!KLASA_DST!" (
            echo [%time%] Creating destination: !KLASA_DST! >> "%LOGFILE%"
            mkdir "!KLASA_DST!" 2>nul
        )
        
        echo [%time%] MIRROR: !KLASA_SRC! >> "%LOGFILE%"
        echo [%time%]     -^> !KLASA_DST! >> "%LOGFILE%"
        
        REM Sync with robocopy
        call :SYNC_WITH_TIMEOUT "!KLASA_SRC!" "!KLASA_DST!" "%LANG%\%%k"
        
        if !SYNC_RESULT! EQU 0 (
            set ANYTHING_SYNCED=1
        )
    ) else (
        echo [%time%] INFO: %%k not found for %LANG% >> "%LOGFILE%"
    )
)

REM ==========================================
REM PART 2: Sync standalone project folders
REM ==========================================
echo [%time%] Scanning for standalone projects in %LANG%... >> "%LOGFILE%"

REM Get all subdirectories in the language folder
for /d %%P in ("%LANG_SRC%\*") do (
    set PROJECT_NAME=%%~nxP
    
    REM Skip if it's a klasa folder (already handled above)
    set IS_KLASA=0
    for %%k in (klasa1 klasa2 klasa3 klasa4 klasa5) do (
        if /i "!PROJECT_NAME!"=="%%k" set IS_KLASA=1
    )
    
    REM If not a klasa folder, it's a standalone project
    if !IS_KLASA! EQU 0 (
        set PROJECT_SRC=%%P
        set PROJECT_DST=%LANG_DST%\!PROJECT_NAME!
        
        echo [%time%] FOUND: Standalone project "!PROJECT_NAME!" in %LANG% >> "%LOGFILE%"
        
        REM Ensure destination exists
        if not exist "!PROJECT_DST!" (
            echo [%time%] Creating destination: !PROJECT_DST! >> "%LOGFILE%"
            mkdir "!PROJECT_DST!" 2>nul
        )
        
        echo [%time%] MIRROR: !PROJECT_SRC! >> "%LOGFILE%"
        echo [%time%]     -^> !PROJECT_DST! >> "%LOGFILE%"
        
        REM Sync with robocopy
        call :SYNC_WITH_TIMEOUT "!PROJECT_SRC!" "!PROJECT_DST!" "%LANG%\!PROJECT_NAME!"
        
        if !SYNC_RESULT! EQU 0 (
            set ANYTHING_SYNCED=1
        )
    )
)

REM Final status for this language
if !ANYTHING_SYNCED! EQU 0 (
    echo [%time%] INFO: No folders found for %LANG% >> "%LOGFILE%"
    set /a PHASE2_SKIPPED+=1
)

goto :EOF

REM ==========================================
REM SUBROUTINE: SYNC_WITH_TIMEOUT
REM Robust sync with timeout protection
REM ==========================================
:SYNC_WITH_TIMEOUT
set "SYNC_SRC=%~1"
set "SYNC_DST=%~2"
set "SYNC_NAME=%~3"
set SYNC_RESULT=1

set TEMP_LOG=%TEMP%\robocopy_%RANDOM%.log

echo [%time%] Starting robocopy with 90-second timeout... >> "%LOGFILE%"

REM Run robocopy in background
start /B "" cmd /c "robocopy "%SYNC_SRC%" "%SYNC_DST%" /MIR /LEV:10 /R:1 /W:2 /XJ /XJD /NFL /NDL /NJH /NJS /MT:2 /UNICODE > "%TEMP_LOG%" 2>&1 & exit"

REM Wait for completion with timeout
set WAIT_COUNT=0
:WAIT_SYNC_LOOP
timeout /t 1 /nobreak >nul 2>nul
set /a WAIT_COUNT+=1

if %WAIT_COUNT% LSS 90 (
    if not exist "%TEMP_LOG%" goto WAIT_SYNC_LOOP
    
    REM Check if robocopy completed (file size stable for 2 seconds)
    for %%F in ("%TEMP_LOG%") do set LOGSIZE1=%%~zF
    timeout /t 1 /nobreak >nul 2>nul
    for %%F in ("%TEMP_LOG%") do set LOGSIZE2=%%~zF
    timeout /t 1 /nobreak >nul 2>nul
    for %%F in ("%TEMP_LOG%") do set LOGSIZE3=%%~zF
    
    if not "%LOGSIZE1%"=="%LOGSIZE2%" goto WAIT_SYNC_LOOP
    if not "%LOGSIZE2%"=="%LOGSIZE3%" goto WAIT_SYNC_LOOP
    
    REM File size stable for 2 seconds - robocopy finished
    goto SYNC_COMPLETED
)

REM Timeout occurred
echo [%time%] ERROR: Robocopy timed out after 90 seconds for %SYNC_NAME% >> "%LOGFILE%"
echo [%time%] Killing hung robocopy process... >> "%LOGFILE%"

taskkill /F /IM robocopy.exe >nul 2>&1

if exist "%TEMP_LOG%" type "%TEMP_LOG%" >> "%LOGFILE%"
del "%TEMP_LOG%" 2>nul

set /a PHASE2_FAILED+=1
set SYNC_RESULT=1
goto :EOF

:SYNC_COMPLETED
REM Process completed successfully
if exist "%TEMP_LOG%" (
    type "%TEMP_LOG%" >> "%LOGFILE%"
    del "%TEMP_LOG%" 2>nul
)

if exist "%SYNC_DST%" (
    echo [%time%] SUCCESS: %SYNC_NAME% synced >> "%LOGFILE%"
    set /a PHASE2_SUCCESS+=1
    set SYNC_RESULT=0
) else (
    echo [%time%] ERROR: Failed to sync %SYNC_NAME% (destination not created) >> "%LOGFILE%"
    set /a PHASE2_FAILED+=1
    set SYNC_RESULT=1
)

goto :EOF

endlocal