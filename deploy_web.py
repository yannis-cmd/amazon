"""
🌐 Amazon Tracker Pro - Déploiement Ngrok
📡 Expose votre serveur local à Internet en 10 secondes!
✅ Tout le monde peut accéder depuis n'importe où
"""

import subprocess
import sys
import os
import requests
import json
import time
from pathlib import Path

def install_ngrok():
    """Installer Ngrok s'il n'existe pas"""
    print("\n📦 Vérification de Ngrok...")
    
    try:
        subprocess.run(['ngrok', '--version'], capture_output=True, check=True)
        print("✅ Ngrok est déjà installé")
        return True
    except:
        print("⚠️  Ngrok n'est pas installé")
        print("📥 Installation de Ngrok...")
        
        try:
            if sys.platform == 'win32':
                # Windows
                print("  Téléchargement pour Windows...")
                os.system('choco install ngrok -y')
            elif sys.platform == 'darwin':
                # macOS
                print("  Téléchargement pour macOS...")
                os.system('brew install ngrok')
            else:
                # Linux
                print("  Téléchargement pour Linux...")
                os.system('apt-get install ngrok-free')
            
            print("✅ Ngrok installé avec succès!")
            return True
        except Exception as e:
            print(f"❌ Erreur installation: {e}")
            print("\n📖 Installez manuellement depuis: https://ngrok.com/download")
            return False

def check_flask_running():
    """Vérifier si Flask est en cours d'exécution"""
    try:
        response = requests.get('http://localhost:3000', timeout=2)
        return True
    except:
        return False

def deploy_with_ngrok():
    """Déployer l'app avec Ngrok"""
    
    print("\n" + "═" * 80)
    print("  🚀 DÉPLOIEMENT AMAZON TRACKER PRO - ACCÈS PUBLIC")
    print("═" * 80)
    
    # Étape 1: Vérifier Flask
    print("\n⏳ Vérification du serveur Flask...")
    if not check_flask_running():
        print("❌ Flask n'est pas lancé!")
        print("   Démarrez d'abord: python app_web.py")
        sys.exit(1)
    
    print("✅ Flask est en cours d'exécution sur http://localhost:3000")
    
    # Étape 2: Installer Ngrok
    if not install_ngrok():
        sys.exit(1)
    
    # Étape 3: Lancer Ngrok
    print("\n📡 Connexion à Ngrok...")
    print("⏳ Veuillez attendre...")
    
    try:
        # Démarrer Ngrok
        process = subprocess.Popen(
            ['ngrok', 'http', '3000', '--bind-tls=true'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Attendre que Ngrok démarre
        time.sleep(3)
        
        # Récupérer l'URL publique via l'API Ngrok
        try:
            ngrok_status = requests.get('http://localhost:4040/api/tunnels', timeout=5).json()
            
            if 'tunnels' in ngrok_status and len(ngrok_status['tunnels']) > 0:
                tunnel = ngrok_status['tunnels'][0]
                public_url = tunnel['public_url']
                
                print("\n" + "═" * 80)
                print("✅ DÉPLOIEMENT RÉUSSI!")
                print("═" * 80)
                print(f"\n🌍 URL PUBLIQUE: {public_url}")
                print(f"\n📱 Accès depuis n'importe où:")
                print(f"   {public_url}")
                print(f"\n💾 URL sauvegardée dans: deployment_url.txt")
                print(f"\n📊 Dashboard Ngrok: http://localhost:4040")
                print("\n" + "═" * 80)
                
                # Sauvegarder l'URL
                with open('deployment_url.txt', 'w') as f:
                    f.write(f"🌍 URL PUBLIQUE AMAZON TRACKER PRO\n")
                    f.write(f"═" * 60 + "\n\n")
                    f.write(f"Accédez depuis n'importe où:\n")
                    f.write(f"{public_url}\n\n")
                    f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Durée: Tant que le script est actif\n\n")
                    f.write(f"📝 ATTENTION: Fermez le script pour désactiver l'accès public\n")
                
                print("\n💬 Partagez cette URL avec vos amis:")
                print(f"   👉 {public_url}")
                
                print("\n✅ Appuyez sur CTRL+C pour arrêter le déploiement...")
                
                # Garder le processus actif
                process.wait()
                
            else:
                print("❌ Erreur: Ngrok ne démarre pas correctement")
                sys.exit(1)
        
        except requests.exceptions.ConnectionError:
            print("❌ Impossible de se connecter à Ngrok")
            print("   Essayez de relancer le script")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Déploiement arrêté")
        print("🔒 L'accès public est désactivé")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    deploy_with_ngrok()
