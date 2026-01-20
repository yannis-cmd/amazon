#!/bin/bash
# install_mobile.sh - Script d'installation pour Android/iOS

echo "╔════════════════════════════════════════════════════════════════════════╗"
echo "║           🛒 Amazon Tracker Pro - Installation Mobile                 ║"
echo "╚════════════════════════════════════════════════════════════════════════╝"
echo ""

# Déterminer le système d'exploitation
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "msys" ]]; then
    OS="windows"
else
    OS="unknown"
fi

echo "Système détecté: $OS"
echo ""

# Vérifier les prérequis
echo "🔍 Vérification des prérequis..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé"
    echo "   Téléchargez-le à: https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python3 trouvé: $(python3 --version)"

if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 n'est pas installé"
    exit 1
fi

echo "✅ pip3 trouvé"
echo ""

# Installation des dépendances
echo "📦 Installation des dépendances..."
echo ""

# Dépendances communes
DEPENDENCIES="kivy requests beautifulsoup4 buildozer cython"

for dep in $DEPENDENCIES; do
    echo "📥 Installation de $dep..."
    pip3 install "$dep"
done

echo ""
echo "✅ Dépendances installées!"
echo ""

# Configuration spécifique à chaque plateforme
case $OS in
    "linux")
        echo "🐧 Configuration pour Linux/Android..."
        echo ""
        
        # Installation des dépendances Linux pour buildozer
        echo "📥 Installation des dépendances Linux..."
        
        if command -v apt-get &> /dev/null; then
            sudo apt-get update
            sudo apt-get install -y \
                build-essential \
                git \
                python3 python3-dev python3-pip \
                libssl-dev \
                libffi-dev \
                libsodium-dev \
                libltdl-dev
        fi
        
        # Installation du NDK Android
        echo ""
        echo "📥 Configuration Android NDK..."
        echo "   Téléchargez le NDK depuis:"
        echo "   https://developer.android.com/ndk/downloads"
        echo ""
        ;;
    
    "macos")
        echo "🍎 Configuration pour macOS/iOS..."
        echo ""
        
        # Installation Xcode
        echo "📥 Installation des outils Xcode..."
        xcode-select --install
        
        # Installation des dépendances macOS
        if ! command -v brew &> /dev/null; then
            echo "📥 Installation de Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        
        brew install libffi libsodium libltdl
        
        echo ""
        echo "📥 Configuration iOS..."
        echo "   Vous devrez installer:"
        echo "   - Xcode (via App Store)"
        echo "   - CocoaPods: sudo gem install cocoapods"
        echo ""
        ;;
    
    "windows")
        echo "🪟 Configuration pour Windows..."
        echo ""
        echo "⚠️  Pour Android sur Windows:"
        echo "    1. Installez Android Studio"
        echo "    2. Installez le NDK Android"
        echo "    3. Configurez les variables d'environnement"
        echo ""
        ;;
esac

# Création de l'APK Android
echo ""
echo "╔════════════════════════════════════════════════════════════════════════╗"
echo "║                    🚀 Compilation vers APK                            ║"
echo "╚════════════════════════════════════════════════════════════════════════╝"
echo ""

read -p "Voulez-vous compiler vers APK Android? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📦 Compilation vers APK..."
    buildozer android debug
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ APK compilé avec succès!"
        echo ""
        echo "📱 Installation sur appareil:"
        echo "   1. Branchez votre appareil Android"
        echo "   2. Activez le mode développeur et USB Debug"
        echo "   3. Exécutez: adb install -r ./bin/amazon_tracker-1.0.0-debug.apk"
        echo ""
    else
        echo "❌ Erreur lors de la compilation"
        exit 1
    fi
fi

# Création pour iOS
echo ""
echo "╔════════════════════════════════════════════════════════════════════════╗"
echo "║                    🍎 Compilation vers iOS                            ║"
echo "╚════════════════════════════════════════════════════════════════════════╝"
echo ""

read -p "Voulez-vous compiler vers iOS? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📦 Compilation vers iOS..."
    buildozer ios debug
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Projet iOS compilé!"
        echo ""
        echo "📱 Installation sur iPhone/iPad:"
        echo "   1. Ouvrez le projet avec Xcode"
        echo "   2. Sélectionnez votre appareil"
        echo "   3. Cliquez sur Run"
        echo ""
    else
        echo "❌ Erreur lors de la compilation iOS"
    fi
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════════════╗"
echo "║                      ✅ Installation terminée!                        ║"
echo "╚════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "📚 Documentation:"
echo "   • Buildozer: https://buildozer.readthedocs.io/"
echo "   • Kivy: https://kivy.org/"
echo "   • Android: https://developer.android.com/"
echo ""
echo "📞 Support: support@amazontracker.com"
echo ""
