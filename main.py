"""
main.py - Point d'entrée principal

Ce fichier lance l'application Amazon Tracker Pro.
À utiliser plutôt que d'appeler amazon_tracker.py directement.
"""

import sys
import logging
from pathlib import Path

# Ajoute le répertoire courant au path pour imports relatifs
sys.path.insert(0, str(Path(__file__).parent))

# Import des modules
try:
    import tkinter as tk
    from amazon_tracker import AmazonTrackerApp
    from logger import setup_logging
except ImportError as e:
    print(f"ERREUR: Impossible d'importer les modules requis: {e}")
    print("Assurez-vous que requirements.txt est installé:")
    print("  pip install -r requirements.txt")
    sys.exit(1)


def main():
    """Fonction principale d'entrée de l'application."""
    # Configure le logging
    logger = setup_logging("amazon_tracker")
    
    try:
        logger.info("=" * 60)
        logger.info("🚀 Démarrage d'Amazon Tracker Pro")
        logger.info("=" * 60)
        
        # Crée la fenêtre root tkinter
        root = tk.Tk()
        
        # Crée l'application
        app = AmazonTrackerApp(root)
        
        logger.info("✅ Application initialisée avec succès")
        
        # Lance la boucle d'événement
        logger.info("⏳ Lancement de la boucle d'événement")
        root.mainloop()
        
    except KeyboardInterrupt:
        logger.info("⏹️  Arrêt demandé par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Erreur fatale: {e}", exc_info=True)
        print(f"\n❌ ERREUR: {e}")
        print("\nConsultez les logs pour plus de détails:")
        print("  logs/amazon_tracker_*.log")
        sys.exit(1)


if __name__ == "__main__":
    main()
