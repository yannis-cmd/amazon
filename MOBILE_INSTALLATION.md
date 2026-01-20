═══════════════════════════════════════════════════════════════════════════════
  📱 GUIDE D'INSTALLATION AMAZON TRACKER PRO - ANDROID & iOS
═══════════════════════════════════════════════════════════════════════════════

VERSION: 1.0
DATE: 2026-01-19
PLATEFORMES: Android 5.0+, iOS 13.0+

───────────────────────────────────────────────────────────────────────────────
 🚀 DÉMARRAGE RAPIDE
───────────────────────────────────────────────────────────────────────────────

OPTION 1: Télécharger l'APK pré-compilé (RECOMMANDÉ)
────────────────────────────────────────────────────

1. Téléchargez l'APK depuis:
   🔗 https://github.com/amazontracker/releases/download/v1.0.0/amazontracker-1.0.0-release.apk

2. Sur votre appareil Android:
   • Allez dans Paramètres → Sécurité
   • Activez "Sources inconnues"
   • Ouvrez le fichier APK
   • Appuyez sur "Installer"

3. Lancez l'application: 🛒 Amazon Tracker Pro


OPTION 2: Compiler vous-même depuis les sources
─────────────────────────────────────────────────

Voir section "COMPILATION AVANCÉE" ci-dessous


───────────────────────────────────────────────────────────────────────────────
 📋 PRÉREQUIS
───────────────────────────────────────────────────────────────────────────────

POUR ANDROID:
✓ Android 5.0 (API 21) ou supérieur
✓ Au moins 100 MB d'espace libre
✓ Connexion Internet
✓ Mode développeur activé (si compilation)

POUR iOS:
✓ iOS 13.0 ou supérieur
✓ Compte Apple ID
✓ Mac avec Xcode (si compilation)
✓ Au moins 500 MB d'espace libre


───────────────────────────────────────────────────────────────────────────────
 🔧 INSTALLATION STEP-BY-STEP
───────────────────────────────────────────────────────────────────────────────

ANDROID - Installation manuelle:

1. Télécharger l'APK
   ┌─────────────────────────────────────────┐
   │ Fichier: amazontracker-1.0.0.apk       │
   │ Taille: ~50 MB                         │
   │ Format: APK (Android Package)          │
   └─────────────────────────────────────────┘

2. Activer les sources inconnues
   Paramètres → Applications → Sources inconnues → Activer

3. Installer l'APK
   Ouvrez le fichier .apk
   Appuyez sur "Installer"
   Attendez la fin de l'installation

4. Lancer l'application
   Appuyez sur "Ouvrir"
   Ou trouvez l'app dans le tiroir d'applications


iOS - Installation via TestFlight (Beta):

1. Installer TestFlight
   App Store → Recherchez "TestFlight" → Installer

2. Accéder à la version bêta
   Ouvrez le lien d'invitation TestFlight
   Appuyez sur "Ouvrir dans TestFlight"
   Appuyez sur "Installer"

3. Lancer l'application
   TestFlight → Amazon Tracker Pro → Lancer


───────────────────────────────────────────────────────────────────────────────
 💡 UTILISATION DE L'APPLICATION
───────────────────────────────────────────────────────────────────────────────

ÉCRAN PRINCIPAL:
┌─────────────────────────────────────────┐
│        🛒 Amazon Tracker Pro            │
├─────────────────────────────────────────┤
│ 🔍 Rechercher un article                │
│ [________________] 🔍 Rechercher 💬    │
│                                         │
│ Résultats / Articles suivis:            │
│ ┌─────────────────────────────────────┐ │
│ │ Article 1                           │ │
│ │ Prix: 99,99€                        │ │
│ ├─────────────────────────────────────┤ │
│ │ Article 2                           │ │
│ │ Prix: 149,99€                       │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ [📋 Mes] [📊 Logs] [⚙️ Config]         │
└─────────────────────────────────────────┘

FONCTIONNALITÉS:

🔍 Rechercher
  • Tapez le nom d'un produit
  • Cliquez sur "Rechercher"
  • Les résultats s'affichent

💬 Support
  • Entrez votre email
  • Décrivez votre problème
  • Cliquez sur "Envoyer"
  • Synchronisation Discord automatique

📋 Mes Articles
  • Consultez vos articles suivis
  • Voir les prix actuels
  • Consulter l'historique

📊 Logs d'Activité
  • Voir toutes vos actions
  • Filtrer par utilisateur
  • Exporter les données

⚙️ Configuration
  • Configurer Discord Webhook
  • Paramètres de synchronisation


───────────────────────────────────────────────────────────────────────────────
 🔓 PERMISSIONS REQUISES
───────────────────────────────────────────────────────────────────────────────

ANDROID:

📱 Accès à Internet
  → Nécessaire pour rechercher les prix sur Amazon
  → Consulter les données en temps réel

🔐 Stockage
  → Sauvegarder les articles suivis localement
  → Sauvegarder les configurations

NOTES:
  • L'application n'accède JAMAIS à vos contacts
  • L'application n'accède JAMAIS à votre localisation
  • L'application n'accède JAMAIS à votre caméra


───────────────────────────────────────────────────────────────────────────────
 ⚙️ COMPILATION AVANCÉE
───────────────────────────────────────────────────────────────────────────────

POUR LES DÉVELOPPEURS - Compiler desde les sources:


COMPILATION ANDROID:
────────────────────

1. Prérequis:
   • Python 3.7+
   • Java JDK 8 ou 11
   • Android SDK
   • Android NDK 23b
   • Buildozer

2. Installation des dépendances:
   
   # Linux/macOS:
   bash install_mobile.sh
   
   # Windows:
   install_mobile.bat

3. Configuration:
   
   export ANDROID_SDK_ROOT="/path/to/android-sdk"
   export ANDROID_NDK_ROOT="/path/to/android-ndk-r23b"

4. Compilation:
   
   buildozer android debug
   
   Sortie: ./bin/amazon_tracker-1.0.0-debug.apk

5. Installation sur appareil:
   
   adb connect <device-ip>:5555  # (si WiFi)
   adb install -r ./bin/amazon_tracker-1.0.0-debug.apk


COMPILATION iOS:
────────────────

1. Prérequis:
   • Mac avec Xcode 12+
   • iOS 13.0+
   • CocoaPods
   • Apple Developer Account

2. Installation:
   
   bash install_mobile.sh

3. Compilation:
   
   buildozer ios debug
   
   Sortie: ./dist/amazontracker-1.0.0.xcworkspace

4. Ouverture avec Xcode:
   
   open ./dist/amazontracker-1.0.0.xcworkspace
   
   • Sélectionnez votre appareil
   • Cliquez sur Run

5. Déploiement sur App Store:
   
   Consultez: https://developer.apple.com/


───────────────────────────────────────────────────────────────────────────────
 🆘 DÉPANNAGE
───────────────────────────────────────────────────────────────────────────────

Problème: L'APK ne s'installe pas
Solution:
  1. Vérifiez que vous avez activé "Sources inconnues"
  2. Vérifiez l'espace disponible (>100 MB)
  3. Réessayez l'installation
  4. Redémarrez l'appareil

Problème: L'application plante au démarrage
Solution:
  1. Videz le cache: Paramètres → Apps → Amazon Tracker → Forcer l'arrêt
  2. Réinstallez l'application
  3. Vérifiez que votre appareil est à jour

Problème: Les données ne se synchronisent pas
Solution:
  1. Vérifiez la connexion Internet
  2. Configurez Discord Webhook (⚙️ Config)
  3. Consultez Paramètres → À propos pour les logs

Problème: Les recherches ne fonctionnent pas
Solution:
  1. Vérifiez la connexion Internet
  2. Essayez un autre terme de recherche
  3. Redémarrez l'application

Problème: Stockage insuffisant
Solution:
  1. Supprimez des articles suivis inutiles
  2. Videz le cache de l'app
  3. Supprimez d'autres applications
  4. Libérez au moins 100 MB


───────────────────────────────────────────────────────────────────────────────
 📊 SPÉCIFICATIONS TECHNIQUES
───────────────────────────────────────────────────────────────────────────────

ANDROID:
  Versions minimales: Android 5.0 (API 21)
  Versions cibles: Android 13+
  Architecture: ARM64, ARMv7
  Taille de l'APK: ~50 MB
  Framework: Kivy 2.2.1

iOS:
  Version minimale: iOS 13.0
  Version cible: iOS 17+
  Architecture: ARM64
  Taille: ~60 MB
  Framework: Kivy 2.2.1

COMMUNES:
  Python: 3.11
  Kivy: 2.2.1
  Requests: 2.31.0
  BeautifulSoup4: 4.12.2


───────────────────────────────────────────────────────────────────────────────
 📞 SUPPORT
───────────────────────────────────────────────────────────────────────────────

AIDE:
  • Consulter cette documentation
  • Utiliser le bouton "💬 Support" dans l'app
  • Envoyer un email: support@amazontracker.com

SIGNALER UN BUG:
  • GitHub: https://github.com/amazontracker/issues
  • Email: bugs@amazontracker.com

DEMANDER UNE FONCTIONNALITÉ:
  • GitHub: https://github.com/amazontracker/discussions
  • Email: features@amazontracker.com


───────────────────────────────────────────────────────────────────────────────
 🔄 MISES À JOUR
───────────────────────────────────────────────────────────────────────────────

Pour mettre à jour l'application:

ANDROID:
  1. Ouvrez Google Play Store
  2. Recherchez "Amazon Tracker Pro"
  3. Appuyez sur "Mettre à jour"
  4. Attendez la fin de la mise à jour

iOS:
  1. Ouvrez App Store
  2. Allez dans "Mises à jour"
  3. Recherchez "Amazon Tracker Pro"
  4. Appuyez sur "Mettre à jour"


HISTORIQUE DES MISES À JOUR:
  v1.0.0 (2026-01-19) - Lancement initial
         - Recherche de produits
         - Suivi des prix
         - Support client
         - Logs d'activité
         - Synchronisation Discord


═══════════════════════════════════════════════════════════════════════════════
