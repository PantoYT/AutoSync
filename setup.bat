@echo off
setlocal EnableDelayedExpansion
title AutoSync Setup Wizard
color 0A

:WELCOME
cls
echo.
echo  ╔════════════════════════════════════════════════════╗
echo  ║                                                    ║
echo  ║         AutoSync Setup Wizard v2.0                 ║
echo  ║         ══════════════════════════                 ║
echo  ║                                                    ║
echo  ║   Configure automatic USB sync, Git, databases,    ║
echo  ║   and web deployment in minutes!                   ║
echo  ║                                                    ║
echo  ╚════════════════════════════════════════════════════╝
echo.
echo  This wizard will help you configure AutoSync for this computer.
echo.
pause
cls

:DETECT_USB
echo.
echo ════════════════════════════════════════════════════
echo  STEP 1: Detecting USB Drive
echo ════════════════════════════════════════════════════
echo.
echo  Scanning for removable drives...
echo.

set USB_FOUND=
for %%D in (D E F G H I J K L M N O P Q R S T U V W X Y Z) do (
    if exist %%D:\ (
        vol %%D: 2>nul | find "Removable" >nul
        if not errorlevel 1 (
            echo  [√] Found USB at %%D:
            set USB_FOUND=%%D:
        )
    )
)

if defined USB_FOUND (
    echo.
    set /p USE_DETECTED="Use %USB_FOUND% as USB drive? (Y/N): "
    if /i "!USE_DETECTED!"=="Y" (
        set USB_DRIVE=%USB_FOUND%
        goto CONFIGURE_PATHS
    )
)

echo.
set /p USB_DRIVE="Enter USB drive letter manually (e.g., G:): "
if not defined USB_DRIVE goto DETECT_USB

:CONFIGURE_PATHS
cls
echo.
echo ════════════════════════════════════════════════════
echo  STEP 2: Configure Local Paths
echo ════════════════════════════════════════════════════
echo.
echo  Default paths will be used. Press Enter to accept defaults
echo  or enter your custom paths.
echo.

REM Local to USB paths
echo  [E: → USB Backups]
echo.
set /p APPS_SRC="Applications folder [E:\Aplikacje]: "
if not defined APPS_SRC set APPS_SRC=E:\Aplikacje

set /p AHK_SRC="AutoHotkey folder [E:\Autohotkey]: "
if not defined AHK_SRC set AHK_SRC=E:\Autohotkey

set /p SCRIPTS_SRC="Scripts folder [E:\Scripts]: "
if not defined SCRIPTS_SRC set SCRIPTS_SRC=E:\Scripts

echo.
echo  [USB → E: Projects]
echo.
set /p PROJECTS_ROOT="Projects root folder [E:\Pliki\Projects]: "
if not defined PROJECTS_ROOT set PROJECTS_ROOT=E:\Pliki\Projects

:CONFIGURE_MYSQL
cls
echo.
echo ════════════════════════════════════════════════════
echo  STEP 3: MySQL Configuration
echo ════════════════════════════════════════════════════
echo.
echo  Detecting MySQL installation...
echo.

set MYSQL_BIN=
if exist "C:\xampp\mysql\bin\mysql.exe" (
    set MYSQL_BIN=C:\xampp\mysql\bin\mysql.exe
    echo  [√] Found MySQL at: !MYSQL_BIN!
) else if exist "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" (
    set MYSQL_BIN=C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe
    echo  [√] Found MySQL at: !MYSQL_BIN!
) else (
    echo  [!] MySQL not detected automatically
)

echo.
if defined MYSQL_BIN (
    set /p USE_MYSQL="Use detected MySQL? (Y/N): "
    if /i "!USE_MYSQL!"=="N" set MYSQL_BIN=
)

if not defined MYSQL_BIN (
    set /p MYSQL_BIN="Enter MySQL bin path: "
)

set /p MYSQL_USER="MySQL username [root]: "
if not defined MYSQL_USER set MYSQL_USER=root

set /p MYSQL_PASS="MySQL password [leave empty if none]: "

:CONFIGURE_WEB
cls
echo.
echo ════════════════════════════════════════════════════
echo  STEP 4: Web Deployment Configuration
echo ════════════════════════════════════════════════════
echo.

set /p WEB_SOURCE="Web projects source [%PROJECTS_ROOT%\websites]: "
if not defined WEB_SOURCE set WEB_SOURCE=%PROJECTS_ROOT%\websites

set /p WEB_DEST="Web deployment destination [C:\xampp\htdocs\myfiles]: "
if not defined WEB_DEST set WEB_DEST=C:\xampp\htdocs\myfiles

:REVIEW
cls
echo.
echo ════════════════════════════════════════════════════
echo  STEP 5: Review Configuration
echo ════════════════════════════════════════════════════
echo.
echo  [USB Drive]
echo   Drive: %USB_DRIVE%
echo.
echo  [Local Backups]
echo   Apps:   %APPS_SRC%
echo   AHK:    %AHK_SRC%
echo   Scripts: %SCRIPTS_SRC%
echo.
echo  [Projects]
echo   Root: %PROJECTS_ROOT%
echo.
echo  [MySQL]
echo   Bin:  %MYSQL_BIN%
echo   User: %MYSQL_USER%
echo.
echo  [Web Deploy]
echo   Source: %WEB_SOURCE%
echo   Dest:   %WEB_DEST%
echo.
set /p CONFIRM="Is this correct? (Y/N): "
if /i not "!CONFIRM!"=="Y" goto WELCOME

:WRITE_CONFIG
cls
echo.
echo ════════════════════════════════════════════════════
echo  STEP 6: Writing Configuration
echo ════════════════════════════════════════════════════
echo.

set CONFIG_FILE=%~dp0sync_config.ini

echo  Creating config file: %CONFIG_FILE%

(
echo [USB]
echo drive=%USB_DRIVE%
echo check_interval=5
echo.
echo [LocalToUSB]
echo apps_src=%APPS_SRC%
echo apps_dst={USB}\Pliki\Inne\Instalki
echo.
echo ahk_src=%AHK_SRC%
echo ahk_dst={USB}\Pliki\Inne\AutoHotkey
echo.
echo scripts_src=%SCRIPTS_SRC%
echo scripts_dst={USB}\Pliki\Inne\Scripts
echo.
echo [USBToLocal]
echo db_src={USB}\Pliki\Technik Programista\Bazy Danych
echo db_dst=%PROJECTS_ROOT%\databases
echo.
echo cpp_src={USB}\Pliki\Technik Programista\Programowanie\cpp
echo cpp_dst=%PROJECTS_ROOT%\cpp
echo.
echo python_src={USB}\Pliki\Technik Programista\Programowanie\python
echo python_dst=%PROJECTS_ROOT%\python
echo.
echo web_src={USB}\Pliki\Technik Programista\Strony internetowe
echo web_dst=%PROJECTS_ROOT%\websites
echo.
echo bhp_src={USB}\Pliki\Technik Programista\BHP
echo bhp_dst=%PROJECTS_ROOT%\BHP
echo.
echo pod_inf_src={USB}\Pliki\Technik Programista\Podstawy Informatyki
echo pod_inf_dst=%PROJECTS_ROOT%\Podstawy informatyki
echo.
echo informatyka_src={USB}\Pliki\Technik Programista\Informatyka
echo informatyka_dst=%PROJECTS_ROOT%\Informatyka
echo.
echo przygot_src={USB}\Pliki\Technik Programista\Przygotowanie do zawodu programisty
echo przygot_dst=%PROJECTS_ROOT%\Przygotowanie do zawodu programisty
echo.
echo [Git]
echo root=%PROJECTS_ROOT%
echo auto_commit=true
echo auto_push=true
echo smart_messages=true
echo scan_subdirs=true
echo.
echo [MySQL]
echo bin=%MYSQL_BIN%
echo user=%MYSQL_USER%
echo pass=%MYSQL_PASS%
echo sql_base=%PROJECTS_ROOT%\databases
echo charset=utf8mb4
echo.
echo [WebDeploy]
echo source=%WEB_SOURCE%
echo destination=%WEB_DEST%
echo.
echo [Logging]
echo dir=logs
echo retention_days=30
) > "%CONFIG_FILE%"

echo  [√] Configuration written successfully!
echo.

:STARTUP_OPTION
echo ════════════════════════════════════════════════════
echo  STEP 7: Auto-Start Configuration
echo ════════════════════════════════════════════════════
echo.
echo  Would you like AutoSync to start automatically when
echo  Windows starts?
echo.
set /p AUTO_START="Enable auto-start? (Y/N): "

if /i "!AUTO_START!"=="Y" (
    echo.
    echo  Creating startup shortcut...
    
    set STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
    set VBS_PATH=%~dp0master_launcher.vbs
    
    REM Create shortcut using PowerShell
    powershell -Command "$WS = New-Object -ComObject WScript.Shell; $SC = $WS.CreateShortcut('!STARTUP_DIR!\AutoSync.lnk'); $SC.TargetPath = '!VBS_PATH!'; $SC.Save()" >nul 2>&1
    
    if errorlevel 1 (
        echo  [!] Failed to create startup shortcut
        echo  You can manually add master_launcher.vbs to startup folder
    ) else (
        echo  [√] Auto-start enabled!
    )
)

:COMPLETE
cls
echo.
echo  ╔════════════════════════════════════════════════════╗
echo  ║                                                    ║
echo  ║              Setup Complete! ✓                     ║
echo  ║                                                    ║
echo  ╚════════════════════════════════════════════════════╝
echo.
echo  AutoSync is now configured and ready to use!
echo.
echo  To start AutoSync:
echo   • Double-click: master_launcher.vbs
echo   • Or run: master_sync.bat
echo.
if /i "!AUTO_START!"=="Y" (
    echo  AutoSync will start automatically on next boot.
    echo.
)
echo  Configuration saved to: sync_config.ini
echo  Logs will be saved to: logs\
echo.
echo  Press any key to exit...
pause >nul

endlocal
exit /b 0
