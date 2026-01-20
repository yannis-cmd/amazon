@echo off
REM 🌐 Amazon Tracker Pro - Déploiement Ngrok (Windows)
REM 📡 Exposez votre serveur à Internet en 1 clic!

cls
echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║  🚀 DEPLOYMENT AMAZON TRACKER PRO - ACCES PUBLIC             ║
echo ║  📡 Ngrok - Accédez depuis n'importe où sur Internet!        ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

REM Vérifier si Flask est lancé
echo ⏳ Vérification du serveur Flask...
netstat -ano | findstr :3000 >nul
if errorlevel 1 (
    echo.
    echo ❌ ERREUR: Flask n'est pas lancé sur le port 3000
    echo.
    echo 📌 Solution:
    echo    1. Ouvrez une autre fenêtre PowerShell
    echo    2. Exécutez: run_web.bat
    echo    3. Puis relancez ce script
    echo.
    pause
    exit /b 1
)
echo ✅ Flask est en cours d'exécution

REM Installer Ngrok si besoin
echo.
echo 📦 Vérification de Ngrok...
ngrok --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Ngrok n'est pas installé
    echo.
    echo 📥 Téléchargement en cours...
    echo    (Cela peut prendre quelques minutes)
    echo.
    
    REM Essayer Chocolatey
    choco --version >nul 2>&1
    if errorlevel 1 (
        echo ❌ Chocolatey n'est pas installé
        echo.
        echo 📖 Téléchargez Ngrok manuellement:
        echo    https://ngrok.com/download
        echo.
        pause
        exit /b 1
    )
    
    choco install ngrok -y
    if errorlevel 1 (
        echo ❌ Erreur d'installation Ngrok
        pause
        exit /b 1
    )
)
echo ✅ Ngrok est prêt

echo.
echo 📡 Connexion à Ngrok...
echo ⏳ Veuillez attendre...
echo.

REM Lancer Ngrok
ngrok http 3000

echo.
echo ❌ Déploiement arrêté
pause
