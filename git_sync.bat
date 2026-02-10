@echo off
setlocal EnableDelayedExpansion

REM ==== MODULE: Git Auto-Sync ====
REM Handles automatic git add/commit/push with smart messages
REM Args: %1 = config file, %2 = log file

set CONFIG_FILE=%~1
set LOGFILE=%~2

echo [%time%] ═══════════════════════════════════ >> "%LOGFILE%"
echo [%time%] GIT SYNC MODULE START >> "%LOGFILE%"
echo [%time%] ═══════════════════════════════════ >> "%LOGFILE%"

REM Read git config
for /f "usebackq tokens=1,2 delims==" %%a in ("%CONFIG_FILE%") do (
    set LINE=%%a
    set VALUE=%%b
    for /f "tokens=* delims= " %%x in ("!LINE!") do set LINE=%%x
    for /f "tokens=* delims= " %%x in ("!VALUE!") do set VALUE=%%x
    
    if "!LINE!"=="root" set GIT_ROOT=!VALUE!
    if "!LINE!"=="auto_commit" set AUTO_COMMIT=!VALUE!
    if "!LINE!"=="auto_push" set AUTO_PUSH=!VALUE!
    if "!LINE!"=="smart_messages" set SMART_MSG=!VALUE!
    if "!LINE!"=="scan_subdirs" set SCAN_SUBDIRS=!VALUE!
)

REM Defaults
if not defined GIT_ROOT set GIT_ROOT=E:\Pliki\Projects
if not defined AUTO_COMMIT set AUTO_COMMIT=true
if not defined AUTO_PUSH set AUTO_PUSH=true
if not defined SMART_MSG set SMART_MSG=true
if not defined SCAN_SUBDIRS set SCAN_SUBDIRS=true

REM Check if git root exists
if not exist "%GIT_ROOT%" (
    echo [%time%] ERROR: Git root not found: %GIT_ROOT% >> "%LOGFILE%"
    exit /b 1
)

REM Sync root directory if it's a git repo
if exist "%GIT_ROOT%\.git" (
    call :GIT_SYNC_REPO "%GIT_ROOT%"
)

REM Scan subdirectories for git repos
if /i "%SCAN_SUBDIRS%"=="true" (
    for /d %%d in ("%GIT_ROOT%\*") do (
        if exist "%%d\.git" (
            call :GIT_SYNC_REPO "%%d"
        )
    )
)

echo [%time%] Git Sync Module Complete >> "%LOGFILE%"
echo.
exit /b 0

REM ==== SUBROUTINES ====

:GIT_SYNC_REPO
set REPO_PATH=%~1
echo [%time%] Checking repo: %REPO_PATH% >> "%LOGFILE%"

pushd "%REPO_PATH%"

REM Check if there are any changes
git status --porcelain > nul 2>&1
if errorlevel 1 (
    echo [%time%] Not a valid git repo: %REPO_PATH% >> "%LOGFILE%"
    popd
    goto :EOF
)

REM Get status and check if there are changes
for /f "delims=" %%i in ('git status --porcelain 2^>nul') do set HAS_CHANGES=1

if not defined HAS_CHANGES (
    echo [%time%] No changes in: %REPO_PATH% >> "%LOGFILE%"
    popd
    goto :EOF
)

REM Stage all changes
git add . >> "%LOGFILE%" 2>&1

REM Generate smart commit message
if /i "%SMART_MSG%"=="true" (
    call :GENERATE_SMART_MESSAGE
) else (
    set COMMIT_MSG=Auto backup %date% %time%
)

REM Commit changes
if /i "%AUTO_COMMIT%"=="true" (
    echo [%time%] Committing: !COMMIT_MSG! >> "%LOGFILE%"
    git commit -m "!COMMIT_MSG!" >> "%LOGFILE%" 2>&1
    
    if errorlevel 1 (
        echo [%time%] WARNING: Commit failed for %REPO_PATH% >> "%LOGFILE%"
        popd
        exit /b 1
    )
    
    REM Push to remote
    if /i "%AUTO_PUSH%"=="true" (
        echo [%time%] Pushing to origin... >> "%LOGFILE%"
        git push origin >> "%LOGFILE%" 2>&1
        
        if errorlevel 1 (
            echo [%time%] WARNING: Push failed for %REPO_PATH% >> "%LOGFILE%"
            echo [%time%] (Changes are committed locally) >> "%LOGFILE%"
        ) else (
            echo [%time%] SUCCESS: Pushed %REPO_PATH% >> "%LOGFILE%"
        )
    )
) else (
    echo [%time%] Skipping commit (auto_commit=false) >> "%LOGFILE%"
)

popd
goto :EOF

:GENERATE_SMART_MESSAGE
REM Count file types and generate descriptive message
set MODIFIED=0
set ADDED=0
set DELETED=0
set FILE_TYPES=

for /f "tokens=1,2" %%a in ('git status --porcelain') do (
    set STATUS=%%a
    set FILE=%%b
    
    REM Count change types
    if "!STATUS!"=="M" set /a MODIFIED+=1
    if "!STATUS!"=="A" set /a ADDED+=1
    if "!STATUS!"=="D" set /a DELETED+=1
    if "!STATUS!"=="??" set /a ADDED+=1
    
    REM Extract file extension
    for %%f in ("!FILE!") do set EXT=%%~xf
    set EXT=!EXT:~1!
    
    REM Track file types (simple approach)
    if not defined FILE_TYPES (
        set FILE_TYPES=!EXT!
    ) else (
        echo !FILE_TYPES! | find "!EXT!" >nul
        if errorlevel 1 set FILE_TYPES=!FILE_TYPES!, !EXT!
    )
)

REM Build smart message
set COMMIT_MSG=Auto:
if %MODIFIED% GTR 0 set COMMIT_MSG=!COMMIT_MSG! %MODIFIED% modified
if %ADDED% GTR 0 (
    if %MODIFIED% GTR 0 (
        set COMMIT_MSG=!COMMIT_MSG!,
    )
    set COMMIT_MSG=!COMMIT_MSG! %ADDED% added
)
if %DELETED% GTR 0 (
    if %MODIFIED% GTR 0 (
        set COMMIT_MSG=!COMMIT_MSG!,
    )
    if %ADDED% GTR 0 (
        set COMMIT_MSG=!COMMIT_MSG!,
    )
    set COMMIT_MSG=!COMMIT_MSG! %DELETED% deleted
)

REM Add file types if available
if defined FILE_TYPES (
    set COMMIT_MSG=!COMMIT_MSG! (!FILE_TYPES! files^)
)

REM Add timestamp
set COMMIT_MSG=!COMMIT_MSG! - %date% %time%

goto :EOF

endlocal
