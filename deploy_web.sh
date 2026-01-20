#!/bin/bash
# 🌐 Amazon Tracker Pro - Déploiement Ngrok (macOS/Linux)
# 📡 Exposez votre serveur à Internet en 1 clic!

clear
echo ""
echo "╔═════════════════════════════════════════════════════════════╗"
echo "║  🚀 DEPLOYMENT AMAZON TRACKER PRO - ACCES PUBLIC           ║"
echo "║  📡 Ngrok - Accédez depuis n'importe où sur Internet!      ║"
echo "╚═════════════════════════════════════════════════════════════╝"
echo ""

# Vérifier si Flask est lancé
echo "⏳ Vérification du serveur Flask..."
if ! nc -z localhost 5000 2>/dev/null; then
    echo ""
    echo "❌ ERREUR: Flask n'est pas lancé sur le port 5000"
    echo ""
    echo "📌 Solution:"
    echo "   1. Ouvrez un autre terminal"
    echo "   2. Exécutez: bash run_web.sh"
    echo "   3. Puis relancez ce script"
    echo ""
    read -p "Appuyez sur ENTRÉE pour quitter..."
    exit 1
fi
echo "✅ Flask est en cours d'exécution"

# Installer Ngrok si besoin
echo ""
echo "📦 Vérification de Ngrok..."

if ! command -v ngrok &> /dev/null; then
    echo "⚠️  Ngrok n'est pas installé"
    echo ""
    echo "📥 Installation..."
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if ! command -v brew &> /dev/null; then
            echo "❌ Homebrew n'est pas installé"
            echo "   Installez depuis: https://brew.sh"
            exit 1
        fi
        brew install ngrok/ngrok/ngrok
    else
        # Linux
        if ! command -v apt-get &> /dev/null; then
            echo "❌ apt-get n'est pas disponible"
            echo "   Installez Ngrok manuellement: https://ngrok.com/download"
            exit 1
        fi
        sudo apt-get update
        sudo apt-get install -y ngrok
    fi
fi
echo "✅ Ngrok est prêt"

echo ""
echo "📡 Connexion à Ngrok..."
echo "⏳ Veuillez attendre..."
echo ""

# Lancer Ngrok
ngrok http 3000

echo ""
echo "❌ Déploiement arrêté"
