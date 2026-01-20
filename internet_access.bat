@echo off
REM 🌐 AMAZON TRACKER PRO - ACCES INTERNET
REM Solutions pour acceder au site depuis l'exterieur

cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║  🌐 AMAZON TRACKER PRO - ACCES INTERNET                       ║
echo ║  Votre site fonctionne localement, partagez-le!               ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo.
echo ACCÉS LOCAL (FONCTIONNE MAINTENANT):
echo ──────────────────────────────────────
echo   Ce PC:        http://localhost:3000/
echo   Autre PC:     http://192.168.1.27:3000/
echo.
echo.
echo ACCÉS INTERNET (AVEC NGROK):
echo ──────────────────────────────────────
echo   Option 1 - Ngrok gratuit (URL aleatoire)
echo     - Creez compte: https://ngrok.com/
echo     - Copiez votre token
echo     - Lancez: python ngrok_tunnel.py
echo.
echo   Option 2 - Ngrok Pro (URL fixe)
echo     - Meme processus + Plan Pro (~5$/mois)
echo     - URL toujours la meme
echo.
echo.
echo CONSEIL:
echo ──────────────────────────────────────
echo Si vous avez un authtoken Ngrok, faites:
echo.
echo   $env:NGROK_AUTHTOKEN='VOTRE_TOKEN'
echo   python ngrok_tunnel.py
echo.
pause
