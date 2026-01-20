#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tunnel Ngrok pour Amazon Tracker Pro
Expose le serveur Flask sur Internet
"""

import time
import os
import subprocess
from pathlib import Path

def start_ngrok_tunnel():
    """Démarrer le tunnel ngrok"""
    print("=" * 70)
    print("  NGROK TUNNEL - AMAZON TRACKER PRO")
    print("=" * 70)
    print()
    
    try:
        # Vérifier si ngrok est installé
        result = subprocess.run(['ngrok', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            print("ERREUR: ngrok n'est pas installe")
            print("Installez ngrok depuis: https://ngrok.com/download")
            input("Appuyez sur Entree...")
            return
        
        print(f"Ngrok version: {result.stdout.strip()}")
        print()
        
        # Vérifier si authtoken est configuré
        config_file = Path.home() / '.ngrok2' / 'ngrok.yml'
        if not config_file.exists():
            config_file = Path.home() / 'AppData' / 'Local' / 'ngrok' / 'ngrok.yml'
        
        if config_file.exists():
            print(f"Configuration ngrok trouvee: {config_file}")
        else:
            print("Attention: Configuration ngrok non trouvee")
        
        print()
        print("Demarrage du tunnel sur port 3000...")
        print()
        
        # Lancer ngrok
        result = subprocess.Popen(
            ['ngrok', 'http', '3000', '--log=stdout'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Lire la sortie
        for line in result.stdout:
            print(line.strip())
            if "Forwarding" in line or "https://" in line:
                print()
                print("=" * 70)
                print("  SUCCES! Site expose sur Internet!")
                print("=" * 70)
        
    except FileNotFoundError:
        print("ERREUR: ngrok n'est pas installe ou pas en PATH")
        print()
        print("Solutions:")
        print("1. Telecharger ngrok: https://ngrok.com/download")
        print("2. Extraire dans un dossier")
        print("3. Ajouter a PATH (ou lancer depuis le dossier ngrok)")
        print()
    except Exception as e:
        print(f"Erreur: {e}")
        print()
        print("Assurez-vous que:")
        print("1. Flask est lance (run_web_v2_1.bat)")
        print("2. Ngrok est installe")
        print("3. L'authtoken est configure (ngrok config add-authtoken <token>)")
        print()
    
    input("Appuyez sur Entree pour quitter...")

if __name__ == "__main__":
    start_ngrok_tunnel()

if __name__ == "__main__":
    start_ngrok_tunnel()
