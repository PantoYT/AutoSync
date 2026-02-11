@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

cls
echo ============================================
echo   USB FOLDER DIAGNOSTIC
echo ============================================
echo.

set USB_DRIVE=G:
set BASE=%USB_DRIVE%\Pliki\Technik Programista

if not exist "%USB_DRIVE%\" (
    echo ERROR: USB drive %USB_DRIVE% not found!
    pause
    exit /b 1
)

if not exist "%BASE%" (
    echo ERROR: Base folder not found!
    echo Expected: %BASE%
    echo.
    echo Your USB structure should be:
    echo %USB_DRIVE%\
    echo └── Pliki\
    echo     └── Technik Programista\
    echo.
    pause
    exit /b 1
)

echo [OK] Base folder exists: %BASE%
echo.

echo ============================================
echo WHAT'S ACTUALLY ON YOUR USB:
echo ============================================
echo.

REM List all folders
echo Main folders in "Technik Programista":
dir "%BASE%" /b /ad 2>nul
echo.

echo ============================================
echo CHECKING EXPECTED FOLDERS:
echo ============================================
echo.

REM Check each folder
call :CHECK "BazyDanych"
call :CHECK "Programowanie"
call :CHECK "Programowanie\cpp"
call :CHECK "Programowanie\python"
call :CHECK "StronyInternetowe"
call :CHECK "BHP"
call :CHECK "PodstawyInformatyki"
call :CHECK "Informatyka"
call :CHECK "PrzygotowanieZawodu"

echo.
echo ============================================
echo DETAILED TREE VIEW:
echo ============================================
echo.
tree "%BASE%" /F /A
echo.

pause
exit /b 0

:CHECK
set FOLDER=%~1
if exist "%BASE%\%FOLDER%" (
    echo [√] FOUND: %FOLDER%
    
    REM Count subfolders
    set COUNT=0
    for /d %%S in ("%BASE%\%FOLDER%\*") do set /a COUNT+=1
    
    if !COUNT! GTR 0 (
        echo     Subfolders (!COUNT!):
        for /d %%S in ("%BASE%\%FOLDER%\*") do echo       - %%~nxS
    ) else (
        echo     (empty)
    )
) else (
    echo [X] MISSING: %FOLDER%
)
echo.
goto :EOF

endlocal