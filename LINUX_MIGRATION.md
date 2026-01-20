# 🔄 Migration vers Zima OS / Linux

## 📋 Résumé des Changements

Ce document décrit comment votre Amazon Tracker Pro fonctionne sur **Zima OS** et d'autres systèmes Linux.

### ✅ Fichiers Linux Créés

| Fichier | Ancien | Nouveau | Fonction |
|---------|--------|---------|----------|
| `start_server.sh` | `start_server.bat` | ✅ | Démarrage serveur avec redémarrage auto |
| `run_web.sh` | `run_web.bat` | ✅ | Application web Flask |
| `install_dependencies.sh` | - | ✅ | Installation auto dépendances |
| `systemd_setup.sh` | - | ✅ | Configuration démarrage automatique |
| `ZIMA_OS_SETUP.md` | - | ✅ | Guide installation complet |

---

## 🚀 Guide de Démarrage

### 1️⃣ Installation Rapide

```bash
# Ouvrir un terminal (Ctrl + Alt + T)

# Installer Python si nécessaire
sudo zypper install python3 python3-pip  # Zima OS
# ou
sudo apt-get install python3 python3-pip  # Ubuntu

# Aller au dossier du projet
cd ~/chemin/vers/amazon-tracker

# Rendre les scripts exécutables
chmod +x *.sh

# Installer les dépendances
./install_dependencies.sh

# Lancer l'application
./run_web.sh
```

### 2️⃣ Accéder à l'Application

- **Local:** http://localhost:5000
- **Réseau:** http://[votre-IP]:5000
  - Trouver IP: `hostname -I`

### 3️⃣ Arrêter l'Application

- `Ctrl + C` dans le terminal
- Ou: `pkill -f "python3.*app_web.py"`

---

## 🔧 Configuration Avancée

### Démarrage Automatique au Boot

```bash
# Configuration systemd (service automatique)
sudo ./systemd_setup.sh

# Puis:
sudo systemctl enable amazon-tracker
sudo systemctl start amazon-tracker
```

### Port Personnalisé

**Éditer `run_web.sh` ligne 43:**
```bash
PORT=5000  # Changer 5000 à votre port préféré
```

### Accès Public (via Ngrok)

```bash
# Installer ngrok
sudo zypper install ngrok  # Zima OS
# ou
snap install ngrok  # Ubuntu

# Lancer l'app
./run_web.sh

# Dans un autre terminal:
ngrok http 5000
```

---

## 📁 Structure Fichiers

```
amazon-tracker/
├── app_web.py              # Application Flask principale
├── run_web.sh              # ✅ Lancer web app (Linux)
├── start_server.sh         # ✅ Lancer serveur (Linux)
├── install_dependencies.sh # ✅ Installer dépendances (Linux)
├── systemd_setup.sh        # ✅ Configuration service (Linux)
│
├── amazon_tracker.py       # CLI version
├── requirements.txt        # Dépendances Python
├── config.py              # Configuration
│
├── templates/             # Templates HTML
├── static/                # CSS, JS, images
└── ZIMA_OS_SETUP.md       # ✅ Guide complet
```

---

## 🐛 Dépannage

### ❌ Command not found: ./run_web.sh

```bash
chmod +x run_web.sh  # Rendre exécutable
./run_web.sh         # Relancer
```

### ❌ ModuleNotFoundError

```bash
pip install -r requirements.txt
# ou
./install_dependencies.sh
```

### ❌ Port 5000 Already in Use

```bash
# Option 1: Tuer les processus Python
pkill -f "python3"

# Option 2: Utiliser un autre port
# Éditer run_web.sh et changer PORT=5000
```

### ❌ Permission Denied

```bash
chmod +x run_web.sh start_server.sh install_dependencies.sh systemd_setup.sh
```

---

## 📝 Notes Importantes

### 1. Chemins Fichiers
- Windows: `C:\Users\eisbr\...`
- Linux: `/home/username/...` ou `~/...`

**Le code Python gère automatiquement** les chemins grâce à `os.path` 👍

### 2. Python 3 vs Python
- Zima OS/Linux: **Toujours utiliser `python3`** (pas `python`)
- Les scripts utilisent `python3` automatiquement

### 3. Permissions Fichiers
```bash
# Appliquer à tous les scripts
chmod +x *.sh

# Créer dossier de logs si besoin
mkdir -p logs
chmod 755 logs
```

### 4. Dossier de Données

Les fichiers de données sont créés automatiquement:
- `articles_tracked.json`
- `search_cache.json`
- `amazon_tracker.log`

Ils se trouvent dans le même dossier que l'application.

---

## ✨ Fonctionnalités Testées

| Fonctionnalité | Status |
|---|---|
| Recherche Amazon | ✅ |
| Affichage Résultats | ✅ |
| Sauvegarde Articles | ✅ |
| Graphiques Prix | ✅ |
| Interface Web | ✅ |
| Responsive (mobile) | ✅ |
| Logs Activité | ✅ |

---

## 🎯 Prochaines Étapes

1. **Installer:** `./install_dependencies.sh`
2. **Lancer:** `./run_web.sh`
3. **Accéder:** http://localhost:5000
4. **Profiter!** 🎉

---

## 📞 Support

Pour plus d'aide:
- Consulter: [ZIMA_OS_SETUP.md](ZIMA_OS_SETUP.md)
- Logs: `tail -f amazon_tracker.log`
- Processus: `ps aux | grep python3`

---

**Bienvenue sur Zima OS! 🚀**
