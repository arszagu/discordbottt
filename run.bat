@echo off
chcp 65001 >nul
REM Skript zapuska Discord bota na Windows

echo ========================================
echo Discord Server Statistics Bot Launcher
echo ========================================
echo.

REM Proverka virtualnogo okruzhenia
if not exist "venv\" (
    echo [ERROR] Virtualnoe okruzhenie ne najdeno!
    echo Pozhaluysta zapustite: python -m venv venv
    pause
    exit /b 1
)

REM Aktivacija virtualnogo okruzhenia
echo [INFO] Aktiviruyu virtualnoe okruzhenie...
call venv\Scripts\activate.bat

REM Proverka requirements.txt
if exist "requirements.txt" (
    echo [INFO] Proverayu zavisimost...
    pip show discord.py >nul 2>&1
    if errorlevel 1 (
        echo [WARNING] Zavisimost ne ustanovlena! Ustanavljayu...
        pip install -r requirements.txt
    )
)

REM Zapusk bota
echo.
echo [INFO] Zapuskau Discord bot...
echo.
python main.py

pause
