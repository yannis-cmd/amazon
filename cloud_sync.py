"""
cloud_sync.py - Synchronisation Cloud des Tickets

Envoie les tickets vers Google Forms, Discord, Telegram ou Email
pour que l'utilisateur les reçoive même s'il n'est pas sur son PC.
"""

import json
import logging
import requests
from typing import Optional, Dict, Any
from pathlib import Path
from support import SupportTicket

logger = logging.getLogger("amazon_tracker.cloud_sync")


class CloudSync:
    """Synchronise les tickets vers le cloud."""
    
    CONFIG_FILE = "cloud_config.json"
    
    def __init__(self):
        """Initialise le sync cloud."""
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Charge la configuration."""
        if Path(self.CONFIG_FILE).exists():
            try:
                with open(self.CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Error loading cloud config: {e}")
        
        return {}
    
    def _save_config(self) -> None:
        """Sauvegarde la configuration."""
        try:
            with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving cloud config: {e}")
    
    def setup_google_forms(self, form_url: str) -> bool:
        """Configure Google Forms.
        
        Args:
            form_url: URL du formulaire Google
            
        Returns:
            True si succès
        """
        try:
            self.config['google_forms_url'] = form_url
            self._save_config()
            logger.info("Google Forms configured")
            return True
        except Exception as e:
            logger.error(f"Error configuring Google Forms: {e}")
            return False
    
    def setup_discord_webhook(self, webhook_url: str) -> bool:
        """Configure Discord Webhook.
        
        Args:
            webhook_url: URL du webhook Discord
            
        Returns:
            True si succès
        """
        try:
            self.config['discord_webhook'] = webhook_url
            self._save_config()
            logger.info("Discord webhook configured")
            return True
        except Exception as e:
            logger.error(f"Error configuring Discord: {e}")
            return False
    
    def setup_telegram(self, bot_token: str, chat_id: str) -> bool:
        """Configure Telegram.
        
        Args:
            bot_token: Token du bot Telegram
            chat_id: ID du chat
            
        Returns:
            True si succès
        """
        try:
            self.config['telegram_bot_token'] = bot_token
            self.config['telegram_chat_id'] = chat_id
            self._save_config()
            logger.info("Telegram configured")
            return True
        except Exception as e:
            logger.error(f"Error configuring Telegram: {e}")
            return False
    
    def setup_google_sheet(self, sheet_id: str, api_key: str) -> bool:
        """Configure Google Sheets (pour envoyer les données directement).
        
        Args:
            sheet_id: ID du Google Sheet
            api_key: Clé API Google
            
        Returns:
            True si succès
        """
        try:
            self.config['google_sheet_id'] = sheet_id
            self.config['google_api_key'] = api_key
            self._save_config()
            logger.info("Google Sheets configured")
            return True
        except Exception as e:
            logger.error(f"Error configuring Google Sheets: {e}")
            return False
    
    def sync_ticket_discord(self, ticket: SupportTicket) -> bool:
        """Envoie le ticket à Discord.
        
        Args:
            ticket: Ticket à envoyer
            
        Returns:
            True si succès
        """
        webhook_url = self.config.get('discord_webhook')
        if not webhook_url:
            logger.warning("Discord webhook not configured")
            return False
        
        try:
            # Déterminer la couleur selon la priorité
            color_map = {
                "critical": 16711680,  # Rouge
                "high": 16744448,      # Orange
                "medium": 16776960,    # Jaune
                "low": 65280           # Vert
            }
            color = color_map.get(ticket.priority, 3447003)  # Bleu par défaut
            
            message = {
                "embeds": [{
                    "title": f"📋 Nouveau Ticket: {ticket.ticket_id}",
                    "description": ticket.title,
                    "color": color,
                    "fields": [
                        {
                            "name": "Priorité",
                            "value": ticket.priority.upper(),
                            "inline": True
                        },
                        {
                            "name": "Catégorie",
                            "value": ticket.category,
                            "inline": True
                        },
                        {
                            "name": "Email",
                            "value": ticket.user_email,
                            "inline": False
                        },
                        {
                            "name": "Description",
                            "value": ticket.description[:500],
                            "inline": False
                        }
                    ],
                    "footer": {
                        "text": f"Créé: {ticket.created_at}"
                    }
                }]
            }
            
            response = requests.post(webhook_url, json=message, timeout=10)
            success = response.status_code == 204
            
            if success:
                logger.info(f"Ticket {ticket.ticket_id} sent to Discord")
            else:
                logger.warning(f"Discord sync failed: {response.status_code}")
            
            return success
        
        except Exception as e:
            logger.error(f"Error syncing to Discord: {e}")
            return False
    
    def sync_ticket_telegram(self, ticket: SupportTicket) -> bool:
        """Envoie le ticket à Telegram.
        
        Args:
            ticket: Ticket à envoyer
            
        Returns:
            True si succès
        """
        bot_token = self.config.get('telegram_bot_token')
        chat_id = self.config.get('telegram_chat_id')
        
        if not bot_token or not chat_id:
            logger.warning("Telegram not configured")
            return False
        
        try:
            message = f"""📋 Nouveau Ticket: {ticket.ticket_id}

✏️ Titre: {ticket.title}
🔴 Priorité: {ticket.priority}
📂 Catégorie: {ticket.category}
📧 Email: {ticket.user_email}

📝 Description:
{ticket.description}

⏰ Date: {ticket.created_at}"""
            
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = {
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            
            response = requests.post(url, json=data, timeout=10)
            success = response.status_code == 200
            
            if success:
                logger.info(f"Ticket {ticket.ticket_id} sent to Telegram")
            else:
                logger.warning(f"Telegram sync failed: {response.status_code}")
            
            return success
        
        except Exception as e:
            logger.error(f"Error syncing to Telegram: {e}")
            return False
    
    def sync_ticket_google_sheet(self, ticket: SupportTicket) -> bool:
        """Envoie le ticket à Google Sheets.
        
        Args:
            ticket: Ticket à envoyer
            
        Returns:
            True si succès
        """
        sheet_id = self.config.get('google_sheet_id')
        api_key = self.config.get('google_api_key')
        
        if not sheet_id or not api_key:
            logger.warning("Google Sheets not configured")
            return False
        
        try:
            # Préparer les données
            values = [[
                ticket.ticket_id,
                ticket.title,
                ticket.description,
                ticket.category,
                ticket.priority,
                ticket.status,
                ticket.user_email,
                ticket.created_at,
                ticket.updated_at
            ]]
            
            url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/A:I!append"
            params = {"key": api_key}
            body = {
                "values": values,
                "majorDimension": "ROWS"
            }
            
            response = requests.post(
                url,
                json=body,
                params=params,
                timeout=10
            )
            
            success = response.status_code == 200
            
            if success:
                logger.info(f"Ticket {ticket.ticket_id} sent to Google Sheets")
            else:
                logger.warning(f"Google Sheets sync failed: {response.status_code}")
            
            return success
        
        except Exception as e:
            logger.error(f"Error syncing to Google Sheets: {e}")
            return False
    
    def sync_all(self, ticket: SupportTicket) -> Dict[str, bool]:
        """Envoie le ticket à tous les services configurés.
        
        Args:
            ticket: Ticket à envoyer
            
        Returns:
            Dict avec résultats par service
        """
        results = {}
        
        # Discord
        if self.config.get('discord_webhook'):
            results['discord'] = self.sync_ticket_discord(ticket)
        
        # Telegram
        if self.config.get('telegram_bot_token'):
            results['telegram'] = self.sync_ticket_telegram(ticket)
        
        # Google Sheets
        if self.config.get('google_sheet_id'):
            results['google_sheets'] = self.sync_ticket_google_sheet(ticket)
        
        return results


# Instance globale
cloud_sync = CloudSync()


# ==================== EXEMPLE D'UTILISATION ====================

if __name__ == "__main__":
    # Configuration (exemple)
    # cloud_sync.setup_discord_webhook("https://discordapp.com/api/webhooks/...")
    # cloud_sync.setup_telegram("123456:ABCdef...", "123456789")
    
    # Créer un ticket de test
    ticket = SupportTicket(
        ticket_id="TKT-TEST123",
        title="Test de synchronisation",
        description="Ceci est un ticket de test",
        category="bug",
        priority="medium",
        status="open",
        user_email="test@example.com",
        created_at="2026-01-19T10:30:00",
        updated_at="2026-01-19T10:30:00"
    )
    
    # Envoyer à tous les services
    results = cloud_sync.sync_all(ticket)
    print(f"Sync results: {results}")
