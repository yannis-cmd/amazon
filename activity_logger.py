"""
activity_logger.py - Enregistrement de l'activité des utilisateurs

Suit toutes les actions (création de tickets, modifications, etc.)
et les stocke dans un fichier JSON pour audit.
Envoie aussi les logs à Discord webhook.
"""

import json
import logging
import requests
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
from dataclasses import dataclass, asdict
import platform
import getpass

logger = logging.getLogger("amazon_tracker.activity_logger")

# Discord Webhook
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1462917224154005647/eDTFaXGmuPFZlGJMLxJukL1f6qroMX7kDHGepF_WEaMw5cu0EHG9isxk8FclBcpum1_1"


@dataclass
class ActivityLog:
    """Enregistrement d'une activité."""
    timestamp: str
    user: str
    action: str
    details: Dict[str, Any]
    ip_address: Optional[str] = None
    machine: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit en dictionnaire."""
        return asdict(self)


class ActivityLogger:
    """Enregistre l'activité des utilisateurs."""
    
    LOG_FILE = "activity_logs.json"
    
    def __init__(self):
        """Initialise le logger d'activité."""
        self.log_file = Path(self.LOG_FILE)
        self.logs: List[ActivityLog] = []
        self._load_logs()
        logger.info("Activity logger initialized")
    
    def _load_logs(self) -> None:
        """Charge les logs existants."""
        try:
            if self.log_file.exists():
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Charger les logs
                    if isinstance(data, list):
                        self.logs = data
                    elif isinstance(data, dict) and "logs" in data:
                        self.logs = data["logs"]
                    logger.info(f"Loaded {len(self.logs)} activity logs")
        except Exception as e:
            logger.error(f"Error loading activity logs: {e}")
            self.logs = []
    
    def _save_logs(self) -> None:
        """Sauvegarde les logs."""
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(self.logs, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving activity logs: {e}")
    
    def log_action(
        self,
        user: str,
        action: str,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None
    ) -> None:
        """Enregistre une action utilisateur et l'envoie à Discord.
        
        Args:
            user: Nom/email de l'utilisateur
            action: Description de l'action
            details: Détails supplémentaires
            ip_address: Adresse IP (optionnel)
        """
        try:
            timestamp = datetime.now().isoformat()
            
            log_entry = {
                "timestamp": timestamp,
                "user": user,
                "action": action,
                "details": details or {},
                "ip_address": ip_address,
                "machine": platform.node()
            }
            
            self.logs.append(log_entry)
            self._save_logs()
            
            # Discord désactivé - logs locaux uniquement
            # self._send_to_discord(user, action, details)
            
            logger.info(f"Action logged: {user} - {action}")
            
        except Exception as e:
            logger.error(f"Error logging action: {e}")
    
    def _send_to_discord(self, user: str, action: str, details: Optional[Dict[str, Any]] = None) -> None:
        """Envoie le log à Discord webhook"""
        try:
            action_icons = {
                'search': 'RECHERCHE',
                'add_article': 'ARTICLE AJOUTE',
                'delete_article': 'ARTICLE SUPPRIME',
                'support_ticket': 'TICKET SUPPORT',
                'ticket_created': 'NOUVEAU TICKET',
                'ticket_updated': 'TICKET MISE A JOUR'
            }
            
            action_colors = {
                'search': 3447003,
                'add_article': 65280,
                'delete_article': 16711680,
                'support_ticket': 16711680,
                'ticket_created': 16711680,
                'ticket_updated': 16776960
            }
            
            title = action_icons.get(action, action.upper())
            color = action_colors.get(action, 3447003)
            
            message = f"**Utilisateur:** {user}"
            if details:
                if isinstance(details, dict):
                    for key, value in details.items():
                        message += f"\n**{key}:** {value}"
                else:
                    message += f"\n{details}"
            
            embed = {
                "title": title,
                "description": message,
                "color": color,
                "timestamp": datetime.now().isoformat()
            }
            
            payload = {"embeds": [embed]}
            response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5)
            if response.status_code not in [200, 204]:
                logger.warning(f"Discord webhook error: {response.status_code} - {response.text}")
        except Exception as e:
            logger.warning(f"Failed to send to Discord: {str(e)}")
    
    def get_user_logs(self, user: str) -> List[Dict[str, Any]]:
        """Récupère les logs d'un utilisateur.
        
        Args:
            user: Email/nom de l'utilisateur
            
        Returns:
            Liste des logs filtrés
        """
        return [log for log in self.logs if log.get("user") == user]
    
    def get_action_logs(self, action: str) -> List[Dict[str, Any]]:
        """Récupère les logs d'une action spécifique.
        
        Args:
            action: Type d'action
            
        Returns:
            Liste des logs filtrés
        """
        return [log for log in self.logs if log.get("action") == action]
    
    def get_recent_logs(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Récupère les logs récents.
        
        Args:
            limit: Nombre maximum de logs à retourner
            
        Returns:
            Derniers logs
        """
        return self.logs[-limit:]
    
    def get_all_users(self) -> List[str]:
        """Récupère la liste de tous les utilisateurs.
        
        Returns:
            Liste unique des utilisateurs
        """
        users = set()
        for log in self.logs:
            if log.get("user"):
                users.add(log["user"])
        return sorted(list(users))
    
    def get_statistics(self) -> Dict[str, Any]:
        """Récupère les statistiques des logs.
        
        Returns:
            Dictionnaire avec les stats
        """
        if not self.logs:
            return {
                "total_logs": 0,
                "total_users": 0,
                "total_actions": 0,
                "users": [],
                "actions_by_type": {}
            }
        
        users = self.get_all_users()
        actions_by_type = {}
        
        for log in self.logs:
            action = log.get("action", "unknown")
            actions_by_type[action] = actions_by_type.get(action, 0) + 1
        
        return {
            "total_logs": len(self.logs),
            "total_users": len(users),
            "total_actions": sum(actions_by_type.values()),
            "users": users,
            "actions_by_type": actions_by_type
        }
    
    def export_logs(self, filename: Optional[str] = None) -> str:
        """Exporte les logs en JSON.
        
        Args:
            filename: Nom du fichier de sortie
            
        Returns:
            Chemin du fichier
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"activity_logs_export_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    "export_timestamp": datetime.now().isoformat(),
                    "total_logs": len(self.logs),
                    "logs": self.logs
                }, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Logs exported to {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Error exporting logs: {e}")
            return ""
    
    def clear_old_logs(self, days: int = 30) -> int:
        """Supprime les logs plus anciens que N jours.
        
        Args:
            days: Nombre de jours à conserver
            
        Returns:
            Nombre de logs supprimés
        """
        try:
            from datetime import timedelta
            
            cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
            original_count = len(self.logs)
            
            self.logs = [
                log for log in self.logs
                if log.get("timestamp", "") > cutoff_date
            ]
            
            deleted = original_count - len(self.logs)
            if deleted > 0:
                self._save_logs()
                logger.info(f"Deleted {deleted} old activity logs")
            
            return deleted
            
        except Exception as e:
            logger.error(f"Error clearing old logs: {e}")
            return 0


# Instance globale
activity_logger = ActivityLogger()


# Exemple d'utilisation
if __name__ == "__main__":
    # Enregistrer quelques actions de test
    activity_logger.log_action(
        user="user1@example.com",
        action="ticket_created",
        details={"ticket_id": "TKT-123", "priority": "high"}
    )
    
    activity_logger.log_action(
        user="user2@example.com",
        action="ticket_viewed",
        details={"ticket_id": "TKT-123"}
    )
    
    # Afficher les stats
    stats = activity_logger.get_statistics()
    print(f"Statistics: {stats}")
