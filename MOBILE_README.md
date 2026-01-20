# 📱 Amazon Tracker Pro - Application Mobile

Application mobile multiplateformes (Android & iOS) pour tracker les prix Amazon.

## 🚀 Installation Rapide

### Android (Recommandé)

```bash
# Télécharger l'APK
wget https://github.com/amazontracker/releases/download/v1.0.0/amazontracker-1.0.0-release.apk

# Installer via ADB
adb install amazontracker-1.0.0-release.apk
```

### iOS

Téléchargez depuis l'App Store (version 1.0.0+)

## 📋 Fichiers

- `amazon_tracker_mobile.py` - Code source Kivy
- `buildozer.spec` - Configuration de compilation
- `install_mobile.sh` - Script d'installation (Linux/macOS)
- `install_mobile.bat` - Script d'installation (Windows)
- `requirements_mobile.txt` - Dépendances Python
- `MOBILE_INSTALLATION.md` - Guide d'installation complet

## 🔧 Compilation

### Prérequis

```bash
pip install -r requirements_mobile.txt
```

### Android

```bash
# Configurer les chemins
export ANDROID_SDK_ROOT="/path/to/sdk"
export ANDROID_NDK_ROOT="/path/to/ndk"

# Compiler
buildozer android debug
# Ou pour version release:
buildozer android release
```

### iOS

```bash
# Compiler
buildozer ios debug

# Ouvrir avec Xcode
open dist/amazontracker-1.0.0.xcworkspace
```

## 📱 Fonctionnalités

- 🔍 Recherche de produits Amazon
- 💾 Suivi des prix
- 💬 Support client avec Discord
- 📊 Logs d'activité
- ⚙️ Configuration en app
- 🌐 Synchronisation cloud

## 🔐 Permissions

**Android:**
- `INTERNET` - Connexion réseau
- `ACCESS_NETWORK_STATE` - Vérifier la connexion

**iOS:**
- Accès Internet

## 📦 Taille de l'App

- **APK Android:** ~50 MB
- **iOS:** ~60 MB

## 🛠️ Développement

Voir `MOBILE_INSTALLATION.md` pour le guide de développement complet.

## 📞 Support

- 📧 Email: support@amazontracker.com
- 🐛 Issues: github.com/amazontracker/issues
- 💬 Discord: [Lien du serveur]

## 📄 Licence

MIT License - Voir LICENSE file
