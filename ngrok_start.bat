@echo off
REM 📡 NGROK TUNNEL - AMAZON TRACKER PRO
REM Lance le tunnel ngrok pour exposer le serveur sur Internet

cls
echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║  📡 NGROK TUNNEL - AMAZON TRACKER PRO                        ║
echo ║  Expose le serveur sur Internet (gratuit)                    ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

REM Vérifier si Flask est lancé
echo Verification du serveur Flask sur port 3000...
netstat -ano | findstr :3000 >nul
if errorlevel 1 (
    echo.
    echo ERREUR: Flask n'est pas lance sur le port 3000
    echo.
    echo Solution:
    echo   1. Ouvrez une autre fenetre PowerShell
    echo   2. Executez: run_web_v2_1.bat
    echo   3. Puis relancez ce script
    echo.
    pause
    exit /b 1
)
echo OK - Flask est lance
echo.

REM Lancer le tunnel ngrok
echo Demarrage du tunnel Ngrok...
echo.

python ngrok_tunnel.py

pause
