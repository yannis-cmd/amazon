#!/bin/bash

# ============================================================================
# 📦 AMAZON TRACKER PRO - Installation Dépendances (Zima OS / Linux)
# ============================================================================

# Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}📦 Installation Dépendances${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Déterminer le gestionnaire de paquets
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS_ID="$ID"
else
    OS_ID="unknown"
fi

# Installer les dépendances système selon la distribution
echo -e "${YELLOW}🔧 Installation des dépendances système...${NC}"

case "$OS_ID" in
    *suse*|*opensuse*)
        echo "  Détecté: Zima OS / OpenSUSE"
        sudo zypper refresh
        sudo zypper install -y python3 python3-pip python3-devel gcc
        ;;
    ubuntu|debian)
        echo "  Détecté: Ubuntu / Debian"
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip python3-dev build-essential
        ;;
    fedora)
        echo "  Détecté: Fedora"
        sudo dnf install -y python3 python3-pip python3-devel gcc
        ;;
    arch)
        echo "  Détecté: Arch"
        sudo pacman -Sy python python-pip base-devel
        ;;
    *)
        echo -e "${YELLOW}  ⚠️  Distribution non identifiée: $OS_ID${NC}"
        echo "  Installation manuelle requise: python3, python3-pip, build-essential"
        ;;
esac

echo ""
echo -e "${YELLOW}✅ Dépendances système installées${NC}"
echo ""

# Vérifier Python
echo -e "${YELLOW}🐍 Vérification Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 n'est pas trouvé${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✅ Python $PYTHON_VERSION${NC}"
echo ""

# Installer/mettre à jour pip
echo -e "${YELLOW}📦 Mise à jour de pip...${NC}"
python3 -m pip install --upgrade pip setuptools wheel

echo ""
echo -e "${YELLOW}📦 Installation des dépendances Python...${NC}"

# Installer les dépendances du projet
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Dépendances installées avec succès${NC}"
    else
        echo -e "${RED}❌ Erreur lors de l'installation${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}⚠️  requirements.txt non trouvé${NC}"
    echo "   Installation des dépendances courantes..."
    pip install flask requests beautifulsoup4 lxml psutil
fi

echo ""
echo -e "${YELLOW}📦 Installation des dépendances supplémentaires...${NC}"
pip install waitress gunicorn

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✅ Installation Terminée!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "Vous pouvez maintenant lancer l'application:"
echo -e "  ${YELLOW}./run_web.sh${NC}"
echo ""
