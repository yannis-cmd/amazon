#!/usr/bin/env python3
"""
test_discord_sync.py - Teste la synchronisation Discord

Ce script crée un ticket de test et vérifie qu'il est bien envoyé à Discord.
"""

import sys
import os
from pathlib import Path

# Ajouter le chemin
sys.path.insert(0, str(Path(__file__).parent))

try:
    from support_client.support import ticket_manager, ticket_notifier
    print("✅ Modules importés avec succès")
except ImportError:
    try:
        from support import ticket_manager, ticket_notifier
        print("✅ Modules importés avec succès (depuis racine)")
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        sys.exit(1)

def test_discord_sync():
    """Teste la synchronisation Discord."""
    print("\n" + "="*60)
    print("🧪 TEST DE SYNCHRONISATION DISCORD")
    print("="*60)
    
    # Vérifier la configuration Discord
    if ticket_notifier.webhook_url:
        print(f"✅ Discord webhook configuré:")
        print(f"   URL: {ticket_notifier.webhook_url[:50]}...")
    else:
        print("❌ Discord webhook NON configuré")
        print("   Veuillez configurer Discord via l'application")
        return False
    
    # Créer un ticket de test
    print("\n📝 Création d'un ticket de test...")
    ticket_id = ticket_manager.create_ticket(
        title="🧪 TICKET DE TEST - Discord Sync",
        description="Ceci est un ticket de test pour vérifier la synchronisation Discord.\n\nSi vous recevez ce message sur Discord, c'est que tout fonctionne! ✅",
        category="bug",
        priority="high",
        user_email="test@example.com"
    )
    print(f"✅ Ticket créé avec l'ID: {ticket_id}")
    
    # Récupérer le ticket
    print("\n📋 Récupération du ticket...")
    ticket = ticket_manager.get_ticket(ticket_id)
    if ticket:
        print(f"✅ Ticket récupéré:")
        print(f"   Titre: {ticket.title}")
        print(f"   Priorité: {ticket.priority}")
        print(f"   Catégorie: {ticket.category}")
    else:
        print("❌ Erreur lors de la récupération du ticket")
        return False
    
    # Envoyer vers Discord
    print("\n🚀 Envoi du ticket vers Discord...")
    success = ticket_notifier.notify_discord(ticket)
    
    if success:
        print("✅ SUCCÈS! Le ticket a été envoyé à Discord!")
        print("   Vérifiez votre serveur Discord pour voir le message")
    else:
        print("❌ ERREUR! L'envoi vers Discord a échoué")
        print("   Vérifiez que le webhook Discord est valide")
        return False
    
    print("\n" + "="*60)
    print("✅ TEST TERMINÉ AVEC SUCCÈS!")
    print("="*60)
    return True

if __name__ == "__main__":
    success = test_discord_sync()
    sys.exit(0 if success else 1)
