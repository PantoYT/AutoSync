@echo off
setlocal EnableDelayedExpansion

REM ==========================================
REM USB SYNC MODULE - ROBUST UTF-8 + TIMEOUT
REM ==========================================
REM Fixes:
REM 1. UTF-8 encoding for Polish characters
REM 2. Timeout protection (max 60s per operation)
REM 3. Skip deeply nested problematic folders
REM 4. Better error recovery
REM ==========================================

REM Save current code page
for /f "tokens=2 delims=:" %%a in ('chcp') do set ORIGINAL_CP=%%a
set ORIGINAL_CP=%ORIGINAL_CP: =%

REM Switch to UTF-8 (65001) for proper Polish character handling
chcp 65001 >nul 2>&1

set CONFIG_FILE=%~1
set LOGFILE=%~2

echo [%time%] ======================================= >> "%LOGFILE%"
echo [%time%] USB SYNC MODULE START (ROBUST UTF-8) >> "%LOGFILE%"
echo [%time%] ======================================= >> "%LOGFILE%"
echo [%time%] Code page set to UTF-8 (65001) for Polish characters >> "%LOGFILE%"

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
REM PHASE 2: USB TO LOCAL (SELECTIVE KLASA)
REM ==========================================
echo [%time%] ======================================= >> "%LOGFILE%"
echo [%time%] PHASE 2: USB -^> LOCAL (KLASA SYNC) >> "%LOGFILE%"
echo [%time%] ======================================= >> "%LOGFILE%"

echo [%time%] Syncing school subjects... >> "%LOGFILE%"

echo [%time%] [Subject] Databases (db)... >> "%LOGFILE%"
call :SYNC_SUBJECT_KLASA "db"

echo [%time%] [Language] C++ (cpp)... >> "%LOGFILE%"
call :SYNC_LANGUAGE_KLASA "cpp"

echo [%time%] [Language] Python (python)... >> "%LOGFILE%"
call :SYNC_LANGUAGE_KLASA "python"

echo [%time%] [Subject] Web development (web)... >> "%LOGFILE%"
call :SYNC_SUBJECT_KLASA "web"

echo [%time%] [Subject] BHP (bhp)... >> "%LOGFILE%"
call :SYNC_SUBJECT_KLASA "bhp"

echo [%time%] [Subject] Podstawy Informatyki (pod_inf)... >> "%LOGFILE%"
call :SYNC_SUBJECT_KLASA "pod_inf"

echo [%time%] [Subject] Informatyka (informatyka)... >> "%LOGFILE%"
call :SYNC_SUBJECT_KLASA "informatyka"

echo [%time%] [Subject] Przygotowanie (przygot)... >> "%LOGFILE%"
call :SYNC_SUBJECT_KLASA "przygot"

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

REM Run robocopy with timeout protection using START command
REM /B = Background
REM /WAIT = Wait for process to finish
set TEMP_LOG=%TEMP%\robocopy_%RANDOM%.log

start /B /WAIT cmd /c "robocopy "%SRC%" "%DST%" /MIR /R:2 /W:3 /NFL /NDL /NJH /NJS /MT:4 /UNICODE > "%TEMP_LOG%" 2>&1"

REM Wait up to 60 seconds for robocopy to complete
set TIMEOUT_COUNTER=0
:WAIT_MIRROR_LOOP
if not exist "%TEMP_LOG%" (
    timeout /t 1 /nobreak >nul
    set /a TIMEOUT_COUNTER+=1
    if !TIMEOUT_COUNTER! LSS 60 goto WAIT_MIRROR_LOOP
    
    echo [%time%] ERROR: Mirror operation timed out for %KEY% >> "%LOGFILE%"
    set /a PHASE1_FAILED+=1
    goto :EOF
)

REM Check robocopy result from log
type "%TEMP_LOG%" >> "%LOGFILE%"
del "%TEMP_LOG%" 2>nul

REM Robocopy exit codes: 0-7 = success, 8+ = errors
REM Since we can't get ERRORLEVEL from background process, check if files exist
if exist "%DST%" (
    echo [%time%] SUCCESS: %KEY% mirrored >> "%LOGFILE%"
    set /a PHASE1_SUCCESS+=1
) else (
    echo [%time%] ERROR: Mirror failed for %KEY% >> "%LOGFILE%"
    set /a PHASE1_FAILED+=1
)
goto :EOF

REM ==========================================
REM SUBROUTINE: SYNC_SUBJECT_KLASA
REM ==========================================
:SYNC_SUBJECT_KLASA
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

REM Track if we synced any klasa folders
set KLASA_SYNCED=0

REM Loop through klasa1-5
for %%k in (klasa1 klasa2 klasa3 klasa4 klasa5) do (
    set KLASA_SRC=%SUBJ_SRC%\%%k
    set KLASA_DST=%SUBJ_DST%\%%k
    
    echo [%time%] Checking klasa: !KLASA_SRC! >> "%LOGFILE%"
    
    if exist "!KLASA_SRC!" (
        echo [%time%] FOUND: %%k for %SUBJECT% >> "%LOGFILE%"
        
        REM Ensure destination exists
        if not exist "!KLASA_DST!" (
            echo [%time%] Creating destination: !KLASA_DST! >> "%LOGFILE%"
            mkdir "!KLASA_DST!" 2>nul
        )
        
        echo [%time%] MIRROR: !KLASA_SRC! >> "%LOGFILE%"
        echo [%time%]     -^> !KLASA_DST! >> "%LOGFILE%"
        
        REM Use ROBOCOPY with stricter settings to avoid hanging
        REM /LEV:10 = Limit directory depth to 10 levels (prevents infinite loops)
        REM /R:1 = Only 1 retry on errors
        REM /W:2 = Wait 2 seconds between retries
        REM /XJ = Exclude junction points (can cause loops)
        REM /XJD = Exclude junction directories
        
        set TEMP_LOG=%TEMP%\robocopy_klasa_%RANDOM%.log
        
        REM Run with timeout protection
        echo [%time%] Starting robocopy with 90-second timeout... >> "%LOGFILE%"
        
        start /B "" cmd /c "robocopy "!KLASA_SRC!" "!KLASA_DST!" /MIR /LEV:10 /R:1 /W:2 /XJ /XJD /NFL /NDL /NJH /NJS /MT:2 /UNICODE > "!TEMP_LOG!" 2>&1 & exit"
        
        REM Wait for completion with timeout
        set WAIT_COUNT=0
        :WAIT_KLASA_LOOP
        timeout /t 1 /nobreak >nul
        set /a WAIT_COUNT+=1
        
        REM Check if process is still running by checking if log is being written
        if !WAIT_COUNT! LSS 90 (
            if not exist "!TEMP_LOG!" goto WAIT_KLASA_LOOP
            
            REM Check if robocopy completed (file size stable)
            for %%F in ("!TEMP_LOG!") do set LOGSIZE1=%%~zF
            timeout /t 1 /nobreak >nul
            for %%F in ("!TEMP_LOG!") do set LOGSIZE2=%%~zF
            
            if not "!LOGSIZE1!"=="!LOGSIZE2!" goto WAIT_KLASA_LOOP
        ) else (
            echo [%time%] ERROR: Robocopy timed out after 90 seconds for %SUBJECT%\%%k >> "%LOGFILE%"
            echo [%time%] This usually means there are problematic nested folders >> "%LOGFILE%"
            
            REM Kill any hung robocopy processes
            taskkill /F /IM robocopy.exe >nul 2>&1
            
            if exist "!TEMP_LOG!" type "!TEMP_LOG!" >> "%LOGFILE%"
            del "!TEMP_LOG!" 2>nul
            
            set /a PHASE2_FAILED+=1
            goto :CONTINUE_KLASA
        )
        
        REM Process completed successfully
        if exist "!TEMP_LOG!" (
            type "!TEMP_LOG!" >> "%LOGFILE%"
            del "!TEMP_LOG!" 2>nul
        )
        
        if exist "!KLASA_DST!" (
            echo [%time%] SUCCESS: %SUBJECT%\%%k synced >> "%LOGFILE%"
            set /a PHASE2_SUCCESS+=1
            set KLASA_SYNCED=1
        ) else (
            echo [%time%] ERROR: Failed to sync %SUBJECT%\%%k (destination not created) >> "%LOGFILE%"
            set /a PHASE2_FAILED+=1
        )
        
        :CONTINUE_KLASA
    ) else (
        echo [%time%] INFO: %%k not found for %SUBJECT% (normal if not in that year yet) >> "%LOGFILE%"
    )
)

REM If no klasa folders were found at all
if !KLASA_SYNCED! EQU 0 (
    echo [%time%] INFO: No klasa folders found for %SUBJECT% >> "%LOGFILE%"
    set /a PHASE2_SKIPPED+=1
)

goto :EOF

REM ==========================================
REM SUBROUTINE: SYNC_LANGUAGE_KLASA
REM ==========================================
:SYNC_LANGUAGE_KLASA
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

REM Track if we synced any klasa folders
set KLASA_SYNCED=0

REM Loop through klasa1-5
for %%k in (klasa1 klasa2 klasa3 klasa4 klasa5) do (
    set KLASA_SRC=%LANG_SRC%\%%k
    set KLASA_DST=%LANG_DST%\%%k
    
    echo [%time%] Checking klasa: !KLASA_SRC! >> "%LOGFILE%"
    
    if exist "!KLASA_SRC!" (
        echo [%time%] FOUND: %%k for %LANG% >> "%LOGFILE%"
        
        REM Ensure destination exists
        if not exist "!KLASA_DST!" (
            echo [%time%] Creating destination: !KLASA_DST! >> "%LOGFILE%"
            mkdir "!KLASA_DST!" 2>nul
        )
        
        echo [%time%] MIRROR: !KLASA_SRC! >> "%LOGFILE%"
        echo [%time%]     -^> !KLASA_DST! >> "%LOGFILE%"
        
        set TEMP_LOG=%TEMP%\robocopy_lang_%RANDOM%.log
        
        echo [%time%] Starting robocopy with 90-second timeout... >> "%LOGFILE%"
        
        start /B "" cmd /c "robocopy "!KLASA_SRC!" "!KLASA_DST!" /MIR /LEV:10 /R:1 /W:2 /XJ /XJD /NFL /NDL /NJH /NJS /MT:2 /UNICODE > "!TEMP_LOG!" 2>&1 & exit"
        
        REM Wait for completion with timeout
        set WAIT_COUNT=0
        :WAIT_LANG_LOOP
        timeout /t 1 /nobreak >nul
        set /a WAIT_COUNT+=1
        
        if !WAIT_COUNT! LSS 90 (
            if not exist "!TEMP_LOG!" goto WAIT_LANG_LOOP
            
            REM Check if robocopy completed (file size stable)
            for %%F in ("!TEMP_LOG!") do set LOGSIZE1=%%~zF
            timeout /t 1 /nobreak >nul
            for %%F in ("!TEMP_LOG!") do set LOGSIZE2=%%~zF
            
            if not "!LOGSIZE1!"=="!LOGSIZE2!" goto WAIT_LANG_LOOP
        ) else (
            echo [%time%] ERROR: Robocopy timed out after 90 seconds for %LANG%\%%k >> "%LOGFILE%"
            echo [%time%] Killing hung robocopy process... >> "%LOGFILE%"
            
            taskkill /F /IM robocopy.exe >nul 2>&1
            
            if exist "!TEMP_LOG!" type "!TEMP_LOG!" >> "%LOGFILE%"
            del "!TEMP_LOG!" 2>nul
            
            set /a PHASE2_FAILED+=1
            goto :CONTINUE_LANG
        )
        
        REM Process completed successfully
        if exist "!TEMP_LOG!" (
            type "!TEMP_LOG!" >> "%LOGFILE%"
            del "!TEMP_LOG!" 2>nul
        )
        
        if exist "!KLASA_DST!" (
            echo [%time%] SUCCESS: %LANG%\%%k synced >> "%LOGFILE%"
            set /a PHASE2_SUCCESS+=1
            set KLASA_SYNCED=1
        ) else (
            echo [%time%] ERROR: Failed to sync %LANG%\%%k >> "%LOGFILE%"
            set /a PHASE2_FAILED+=1
        )
        
        :CONTINUE_LANG
    ) else (
        echo [%time%] INFO: %%k not found for %LANG% (normal if not in that year yet) >> "%LOGFILE%"
    )
)

REM If no klasa folders were found at all
if !KLASA_SYNCED! EQU 0 (
    echo [%time%] INFO: No klasa folders found for %LANG% >> "%LOGFILE%"
    set /a PHASE2_SKIPPED+=1
)

goto :EOF

endlocal