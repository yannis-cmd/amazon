#!/usr/bin/env python3
"""
build_mobile_app.py - Script de compilation automatique pour Android/iOS

Compile l'application Amazon Tracker Pro vers APK ou IPA
"""

import subprocess
import sys
import os
import platform
from pathlib import Path


def print_header(text):
    """Affiche un en-tête formaté"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")


def check_requirements():
    """Vérifie les prérequis"""
    print_header("🔍 Vérification des prérequis")
    
    # Vérifier Python
    print("✓ Python3: OK")
    
    # Vérifier pip
    try:
        subprocess.run(["pip", "--version"], capture_output=True, check=True)
        print("✓ pip: OK")
    except:
        print("✗ pip: NON TROUVÉ")
        return False
    
    # Vérifier buildozer
    try:
        subprocess.run(["buildozer", "--version"], capture_output=True, check=True)
        print("✓ Buildozer: OK")
    except:
        print("✗ Buildozer: NON TROUVÉ")
        print("  Installation: pip install buildozer")
        return False
    
    # Vérifier cython
    try:
        import cython
        print("✓ Cython: OK")
    except:
        print("✗ Cython: NON TROUVÉ")
        print("  Installation: pip install cython")
        return False
    
    return True


def build_android(debug=True):
    """Compile pour Android"""
    print_header("📦 Compilation Android")
    
    # Vérifier les variables d'environnement
    if not os.environ.get("ANDROID_SDK_ROOT"):
        print("⚠️  ANDROID_SDK_ROOT non défini")
        print("   Définissez: export ANDROID_SDK_ROOT=/path/to/sdk")
        return False
    
    if not os.environ.get("ANDROID_NDK_ROOT"):
        print("⚠️  ANDROID_NDK_ROOT non défini")
        print("   Définissez: export ANDROID_NDK_ROOT=/path/to/ndk")
        return False
    
    print("✓ Variables d'environnement configurées")
    print()
    
    # Compiler
    mode = "debug" if debug else "release"
    cmd = ["buildozer", "android", mode]
    
    print(f"🚀 Exécution: {' '.join(cmd)}")
    print("⏳ Cela peut prendre plusieurs minutes...\n")
    
    try:
        result = subprocess.run(cmd, check=True)
        
        print_header("✅ Compilation réussie!")
        
        if debug:
            print("📱 Fichier: ./bin/amazon_tracker-1.0.0-debug.apk")
        else:
            print("📱 Fichier: ./bin/amazon_tracker-1.0.0-release.apk")
        
        print("\n🔧 Installation sur appareil:")
        if debug:
            print("   adb install -r ./bin/amazon_tracker-1.0.0-debug.apk")
        else:
            print("   1. Uploadez l'APK sur Google Play Console")
            print("   2. Soumettez pour révision")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print_header("❌ Erreur de compilation")
        print(f"Code d'erreur: {e.returncode}")
        return False


def build_ios(debug=True):
    """Compile pour iOS"""
    print_header("📦 Compilation iOS")
    
    # Vérifier que c'est macOS
    if platform.system() != "Darwin":
        print("❌ iOS ne peut être compilé que sur macOS")
        return False
    
    # Vérifier Xcode
    try:
        subprocess.run(["xcode-select", "--version"], capture_output=True, check=True)
        print("✓ Xcode: OK")
    except:
        print("✗ Xcode: NON TROUVÉ")
        print("  Installez Xcode depuis l'App Store")
        return False
    
    # Compiler
    mode = "debug" if debug else "release"
    cmd = ["buildozer", "ios", mode]
    
    print(f"🚀 Exécution: {' '.join(cmd)}")
    print("⏳ Cela peut prendre plusieurs minutes...\n")
    
    try:
        result = subprocess.run(cmd, check=True)
        
        print_header("✅ Compilation réussie!")
        
        print("📱 Projet généré: ./dist/amazontracker-1.0.0.xcworkspace")
        print("\n🔧 Ouverture avec Xcode:")
        print("   open ./dist/amazontracker-1.0.0.xcworkspace")
        print("\nPuis:")
        print("   1. Sélectionnez votre appareil")
        print("   2. Cliquez sur Run")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print_header("❌ Erreur de compilation")
        print(f"Code d'erreur: {e.returncode}")
        return False


def main():
    """Fonction principale"""
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════════╗")
    print("║           🛒 Amazon Tracker Pro - Build Mobile App                    ║")
    print("╚════════════════════════════════════════════════════════════════════════╝")
    
    # Vérifier les prérequis
    if not check_requirements():
        print("\n❌ Certains prérequis sont manquants")
        print("Installez les dépendances: pip install -r requirements_mobile.txt")
        sys.exit(1)
    
    # Choisir la plateforme
    print("\n📱 Sélectionnez une plateforme:")
    print("   1. Android (APK)")
    print("   2. iOS (IPA)")
    print("   3. Les deux")
    
    choice = input("\nVotre choix (1-3): ").strip()
    
    # Choisir la version
    print("\n📦 Type de build:")
    print("   1. Debug (pour test)")
    print("   2. Release (pour production)")
    
    build_choice = input("\nVotre choix (1-2): ").strip()
    debug = build_choice == "1"
    
    success = True
    
    # Compiler pour Android
    if choice in ["1", "3"]:
        if not build_android(debug):
            success = False
    
    # Compiler pour iOS
    if choice in ["2", "3"]:
        if not build_ios(debug):
            success = False
    
    # Résultat final
    if success:
        print_header("🎉 Compilation terminée avec succès!")
        print("📱 Vos applications sont prêtes pour le déploiement!")
    else:
        print_header("❌ Des erreurs se sont produites")
        print("Vérifiez les logs ci-dessus pour plus de détails")
        sys.exit(1)


if __name__ == "__main__":
    main()
