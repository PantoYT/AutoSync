@echo off
REM ═══════════════════════════════════════════════════
REM Stop AutoSync
REM ═══════════════════════════════════════════════════

echo Stopping AutoSync...

REM Kill by command line search
taskkill /FI "WINDOWTITLE eq master_sync.bat*" /F >nul 2>&1

REM Also kill any cmd.exe running master_sync.bat
wmic process where "name='cmd.exe' and commandline like '%%master_sync.bat%%'" delete >nul 2>&1

echo AutoSync stopped.
timeout /t 2 >nul

exit
