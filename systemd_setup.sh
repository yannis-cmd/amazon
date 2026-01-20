#!/bin/bash

# ============================================================================
# 🔧 Configuration Systemd - Amazon Tracker Pro (Zima OS / Linux)
# ============================================================================
# Permet de lancer l'app au démarrage et de la gérer avec systemctl
# ============================================================================

# Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}🔧 Configuration Systemd${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Vérifier si on est root
if [ "$EUID" -ne 0 ]; then
    echo -e "${YELLOW}⚠️  Ce script doit être exécuté en tant que root${NC}"
    echo "Relancez avec: sudo ./systemd_setup.sh"
    exit 1
fi

# Obtenir l'utilisateur courant
CURRENT_USER="${SUDO_USER:-$(whoami)}"
PROJECT_DIR="$(pwd)"

echo -e "${YELLOW}Configuration:${NC}"
echo "  • Utilisateur: $CURRENT_USER"
echo "  • Répertoire: $PROJECT_DIR"
echo ""

# Créer le fichier de service systemd
echo -e "${YELLOW}Création du service systemd...${NC}"

cat > /etc/systemd/system/amazon-tracker.service << EOF
[Unit]
Description=Amazon Tracker Pro - Web Application
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$PROJECT_DIR
ExecStart=/usr/bin/python3 $PROJECT_DIR/app_web.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

echo -e "${GREEN}✅ Service créé: /etc/systemd/system/amazon-tracker.service${NC}"
echo ""

# Recharger systemd
echo -e "${YELLOW}Rechargement de systemd...${NC}"
systemctl daemon-reload

echo -e "${GREEN}✅ Systemd rechargé${NC}"
echo ""

# Afficher les commandes disponibles
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✅ Configuration Terminée!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

echo -e "${YELLOW}Commandes disponibles:${NC}"
echo ""
echo -e "  ${GREEN}Démarrer l'application:${NC}"
echo "    sudo systemctl start amazon-tracker"
echo ""
echo -e "  ${GREEN}Arrêter l'application:${NC}"
echo "    sudo systemctl stop amazon-tracker"
echo ""
echo -e "  ${GREEN}Redémarrer l'application:${NC}"
echo "    sudo systemctl restart amazon-tracker"
echo ""
echo -e "  ${GREEN}Voir l'état:${NC}"
echo "    sudo systemctl status amazon-tracker"
echo ""
echo -e "  ${GREEN}Voir les logs:${NC}"
echo "    sudo journalctl -u amazon-tracker -f"
echo ""
echo -e "  ${GREEN}Activer au démarrage:${NC}"
echo "    sudo systemctl enable amazon-tracker"
echo ""
echo -e "  ${GREEN}Désactiver au démarrage:${NC}"
echo "    sudo systemctl disable amazon-tracker"
echo ""

# Optionnellement, démarrer maintenant
echo -e "${YELLOW}Voulez-vous démarrer l'application maintenant? (y/n)${NC}"
read -r response
if [[ "$response" == "y" ]] || [[ "$response" == "Y" ]]; then
    systemctl start amazon-tracker
    echo -e "${GREEN}✅ Application démarrée${NC}"
    echo ""
    echo -e "  Accès: ${YELLOW}http://localhost:5000${NC}"
fi
