"""
test_support.py - Tests du Système de Support Client

Testé la création de tickets et la synchronisation cloud.
"""

import sys
from pathlib import Path

# Ajouter le répertoire courant au path
sys.path.insert(0, str(Path(__file__).parent))

from support import ticket_manager, SupportTicket
from cloud_sync import cloud_sync


def test_ticket_creation():
    """Test la création d'un ticket."""
    print("\n[TEST] Création de ticket...")
    
    try:
        ticket_id = ticket_manager.create_ticket(
            title="Test Ticket",
            description="Ceci est un ticket de test",
            category="bug",
            priority="medium",
            user_email="test@example.com"
        )
        
        print(f"[OK] Ticket créé: {ticket_id}")
        return ticket_id
    
    except Exception as e:
        print(f"[ERROR] Erreur: {e}")
        return None


def test_ticket_retrieval(ticket_id: str):
    """Test la récupération d'un ticket."""
    print("\n[TEST] Récupération du ticket...")
    
    try:
        ticket = ticket_manager.get_ticket(ticket_id)
        
        if ticket:
            print(f"[OK] Ticket récupéré:")
            print(f"     ID: {ticket.ticket_id}")
            print(f"     Title: {ticket.title}")
            print(f"     Status: {ticket.status}")
            return True
        else:
            print(f"[ERROR] Ticket non trouvé")
            return False
    
    except Exception as e:
        print(f"[ERROR] Erreur: {e}")
        return False


def test_ticket_note(ticket_id: str):
    """Test l'ajout d'une note."""
    print("\n[TEST] Ajout d'une note...")
    
    try:
        success = ticket_manager.add_note(ticket_id, "Test note")
        
        if success:
            ticket = ticket_manager.get_ticket(ticket_id)
            print(f"[OK] Note ajoutée:")
            print(f"     Notes: {len(ticket.notes)}")
            return True
        else:
            print(f"[ERROR] Impossible d'ajouter la note")
            return False
    
    except Exception as e:
        print(f"[ERROR] Erreur: {e}")
        return False


def test_ticket_status_update(ticket_id: str):
    """Test la mise à jour du statut."""
    print("\n[TEST] Mise à jour du statut...")
    
    try:
        success = ticket_manager.update_status(ticket_id, "in_progress")
        
        if success:
            ticket = ticket_manager.get_ticket(ticket_id)
            print(f"[OK] Statut mis à jour: {ticket.status}")
            return True
        else:
            print(f"[ERROR] Impossible de mettre à jour le statut")
            return False
    
    except Exception as e:
        print(f"[ERROR] Erreur: {e}")
        return False


def test_ticket_listing():
    """Test la liste des tickets."""
    print("\n[TEST] Listing des tickets...")
    
    try:
        tickets = ticket_manager.list_tickets()
        
        print(f"[OK] {len(tickets)} ticket(s) trouvé(s):")
        for ticket in tickets:
            print(f"     - {ticket.ticket_id}: {ticket.title}")
        
        return True
    
    except Exception as e:
        print(f"[ERROR] Erreur: {e}")
        return False


def test_ticket_export(ticket_id: str):
    """Test l'export d'un ticket."""
    print("\n[TEST] Export du ticket...")
    
    try:
        exported = ticket_manager.export_ticket(ticket_id)
        
        if exported:
            print(f"[OK] Ticket exporté (longueur: {len(exported)} caractères)")
            return True
        else:
            print(f"[ERROR] Export vide")
            return False
    
    except Exception as e:
        print(f"[ERROR] Erreur: {e}")
        return False


def test_cloud_config():
    """Test la configuration cloud."""
    print("\n[TEST] Configuration cloud...")
    
    try:
        config = cloud_sync.config
        
        if config:
            print(f"[OK] Configuration chargée:")
            for key in config:
                value = config[key]
                if len(str(value)) > 20:
                    print(f"     {key}: {str(value)[:20]}...")
                else:
                    print(f"     {key}: {value}")
        else:
            print(f"[OK] Aucune configuration (normal pour la première utilisation)")
        
        return True
    
    except Exception as e:
        print(f"[ERROR] Erreur: {e}")
        return False


def test_cloud_sync_mock():
    """Test la synchronisation cloud (sans vraies clés)."""
    print("\n[TEST] Test de synchronisation cloud...")
    
    try:
        ticket = SupportTicket(
            ticket_id="TKT-TEST",
            title="Test Sync",
            description="Test de synchronisation",
            category="bug",
            priority="high",
            status="open",
            user_email="test@example.com",
            created_at="2026-01-19T00:00:00",
            updated_at="2026-01-19T00:00:00"
        )
        
        results = cloud_sync.sync_all(ticket)
        
        if results:
            print(f"[OK] Résultats de synchronisation:")
            for service, success in results.items():
                status = "[OK]" if success else "[FAIL]"
                print(f"     {status} {service}")
        else:
            print(f"[OK] Aucun service configuré (normal)")
        
        return True
    
    except Exception as e:
        print(f"[ERROR] Erreur: {e}")
        return False


def main():
    """Exécute tous les tests."""
    print("=" * 60)
    print("TEST DU SYSTÈME DE SUPPORT CLIENT")
    print("=" * 60)
    
    results = {}
    
    # Test 1: Création
    ticket_id = test_ticket_creation()
    results['creation'] = ticket_id is not None
    
    if ticket_id:
        # Test 2: Récupération
        results['retrieval'] = test_ticket_retrieval(ticket_id)
        
        # Test 3: Note
        results['note'] = test_ticket_note(ticket_id)
        
        # Test 4: Statut
        results['status'] = test_ticket_status_update(ticket_id)
        
        # Test 5: Export
        results['export'] = test_ticket_export(ticket_id)
    
    # Test 6: Listing
    results['listing'] = test_ticket_listing()
    
    # Test 7: Config cloud
    results['cloud_config'] = test_cloud_config()
    
    # Test 8: Sync cloud
    results['cloud_sync'] = test_cloud_sync_mock()
    
    # Résumé
    print("\n" + "=" * 60)
    print("RÉSUMÉ")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, passed_status in results.items():
        status = "[OK]" if passed_status else "[FAIL]"
        print(f"{status} {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passés")
    
    if passed == total:
        print("\n✓ Tous les tests sont passés!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) échoué(s)")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
