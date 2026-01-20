#!/bin/bash

# ============================================================================
# ⚡ DÉMARRAGE RAPIDE - Amazon Tracker Pro sur Zima OS
# ============================================================================

# Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

clear

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║        AMAZON TRACKER PRO - DÉMARRAGE RAPIDE              ║"
echo "║              Zima OS / Linux Edition                       ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo ""
echo -e "${YELLOW}🔍 Vérification de l'environnement...${NC}"
echo ""

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 n'est pas trouvé${NC}"
    echo ""
    echo -e "${YELLOW}Installation pour Zima OS:${NC}"
    echo "  sudo zypper install python3 python3-pip"
    echo ""
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1)
echo -e "${GREEN}✅ $PYTHON_VERSION trouvé${NC}"

# Vérifier les dépendances Python
echo ""
echo -e "${YELLOW}📦 Installation des dépendances Python...${NC}"

python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}   Installation de Flask...${NC}"
    python3 -m pip install -q flask requests beautifulsoup4 lxml psutil
fi

echo -e "${GREEN}✅ Dépendances OK${NC}"

# Rendre les scripts exécutables
echo ""
echo -e "${YELLOW}⚙️  Configuration des scripts...${NC}"
chmod +x run_web.sh start_server.sh install_dependencies.sh systemd_setup.sh 2>/dev/null
echo -e "${GREEN}✅ Scripts configurés${NC}"

# Menu de sélection
echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Choisissez comment démarrer l'application:${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo ""
echo "  ${YELLOW}1${NC} - Mode WEB (Recommandé - Interface navigateur)"
echo "  ${YELLOW}2${NC} - Mode SERVEUR (Avec redémarrage automatique)"
echo "  ${YELLOW}3${NC} - Configuration Systemd (Démarrage auto au boot)"
echo "  ${YELLOW}4${NC} - CLI Autonome (Chercher une souris directement)"
echo "  ${YELLOW}5${NC} - Quitter"
echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo ""

read -p "Entrez votre choix (1-5): " choice

case $choice in
    1)
        echo ""
        echo -e "${GREEN}🚀 Lancement de l'application WEB...${NC}"
        echo ""
        sleep 1
        ./run_web.sh
        ;;
    2)
        echo ""
        echo -e "${GREEN}🚀 Lancement du SERVEUR...${NC}"
        echo ""
        sleep 1
        ./start_server.sh
        ;;
    3)
        echo ""
        echo -e "${GREEN}⚙️  Configuration Systemd...${NC}"
        echo ""
        sleep 1
        sudo ./systemd_setup.sh
        ;;
    4)
        echo ""
        echo -e "${GREEN}🚀 Lancement du mode CLI...${NC}"
        echo ""
        python3 amazon_tracker.py
        ;;
    5)
        echo -e "${YELLOW}À bientôt! 👋${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}❌ Choix invalide${NC}"
        exit 1
        ;;
esac
