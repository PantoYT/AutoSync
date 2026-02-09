@echo off
echo ============================================
echo  NUCLEAR STOP - Killing ALL AutoSync processes
echo ============================================
echo.

echo [1/4] Killing by window title...
taskkill /FI "WINDOWTITLE eq master_sync.bat*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq usb_sync.bat*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq git_sync.bat*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq db_deploy.bat*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq web_deploy.bat*" /F >nul 2>&1

echo [2/4] Killing by command line (master_sync)...
wmic process where "name='cmd.exe' and commandline like '%%master_sync.bat%%'" delete >nul 2>&1

echo [3/4] Killing by command line (modules)...
wmic process where "name='cmd.exe' and commandline like '%%usb_sync.bat%%'" delete >nul 2>&1
wmic process where "name='cmd.exe' and commandline like '%%git_sync.bat%%'" delete >nul 2>&1
wmic process where "name='cmd.exe' and commandline like '%%db_deploy.bat%%'" delete >nul 2>&1
wmic process where "name='cmd.exe' and commandline like '%%web_deploy.bat%%'" delete >nul 2>&1

echo [4/4] Killing robocopy processes...
taskkill /IM robocopy.exe /F >nul 2>&1

echo.
echo ============================================
echo  ALL AutoSync processes terminated
echo ============================================
echo.
pause

exit