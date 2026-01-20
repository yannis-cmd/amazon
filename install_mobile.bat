@echo off
REM install_mobile.bat - Script d'installation pour Android/iOS sur Windows

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════════════════╗
echo ║           🛒 Amazon Tracker Pro - Installation Mobile                 ║
echo ╚════════════════════════════════════════════════════════════════════════╝
echo.

REM Vérifier Python
echo 🔍 Vérification des prérequis...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé
    echo    Téléchargez-le à: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python trouvé
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip n'est pas installé
    pause
    exit /b 1
)

echo ✅ pip trouvé
echo.

REM Installation des dépendances
echo 📦 Installation des dépendances...
echo.

set DEPENDENCIES=kivy requests beautifulsoup4 buildozer cython
for %%D in (%DEPENDENCIES%) do (
    echo 📥 Installation de %%D...
    python -m pip install %%D
)

echo.
echo ✅ Dépendances installées!
echo.

REM Configuration Android
echo.
echo ╔════════════════════════════════════════════════════════════════════════╗
echo ║                    Android Setup                                       ║
echo ╚════════════════════════════════════════════════════════════════════════╝
echo.

echo 📥 Pour Android, vous devez:
echo    1. Installer Android Studio: https://developer.android.com/studio
echo    2. Installer Android NDK
echo    3. Configurer les variables d'environnement:
echo       - ANDROID_SDK_ROOT (chemin vers Android SDK)
echo       - ANDROID_NDK_ROOT (chemin vers Android NDK)
echo.

set /p SETUP_ANDROID="Avez-vous configuré Android SDK/NDK? (y/n) "
if /i "%SETUP_ANDROID%"=="y" (
    
    echo.
    echo ╔════════════════════════════════════════════════════════════════════════╗
    echo ║                    🚀 Compilation vers APK                            ║
    echo ╚════════════════════════════════════════════════════════════════════════╝
    echo.
    
    set /p COMPILE_APK="Voulez-vous compiler vers APK Android? (y/n) "
    if /i "%COMPILE_APK%"=="y" (
        echo 📦 Compilation vers APK...
        buildozer android debug
        
        if errorlevel 0 (
            echo.
            echo ✅ APK compilé avec succès!
            echo.
            echo 📱 Installation sur appareil:
            echo    1. Branchez votre appareil Android
            echo    2. Activez le mode développeur et USB Debug
            echo    3. Exécutez: adb install -r ./bin/amazon_tracker-1.0.0-debug.apk
            echo.
        ) else (
            echo ❌ Erreur lors de la compilation
            pause
            exit /b 1
        )
    )
)

echo.
echo ╔════════════════════════════════════════════════════════════════════════╗
echo ║                      ✅ Installation terminée!                        ║
echo ╚════════════════════════════════════════════════════════════════════════╝
echo.

echo 📚 Liens utiles:
echo    • Buildozer: https://buildozer.readthedocs.io/
echo    • Kivy: https://kivy.org/
echo    • Android: https://developer.android.com/
echo.

echo 📞 Télécharger l'APK depuis Google Play (futur):
echo    • https://play.google.com/store/apps/details?id=org.amazontracker
echo.

pause
