"""
Configuration du logging pour Amazon Tracker Pro

Ce module centralise toute la configuration de logging pour permettre
un suivi cohérent des opérations et du dépannage.
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

from config import log_config, data_config

# Crée le répertoire des logs s'il n'existe pas
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Timestamp pour les fichiers de log
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")


def setup_logging(name: str = "amazon_tracker") -> logging.Logger:
    """Configure le logging pour l'application.
    
    Crée un logger avec:
    - Fichier de log rotatif
    - Sortie console
    - Format standardisé
    
    Args:
        name: Nom du logger
        
    Returns:
        Logger configuré
        
    Example:
        >>> logger = setup_logging("mon_app")
        >>> logger.info("Application démarrée")
    """
    
    # Récupère ou crée le logger
    logger = logging.getLogger(name)
    
    # Définit le niveau de log
    log_level = getattr(logging, log_config.LEVEL)
    logger.setLevel(log_level)
    
    # Évite les logs dupliqués
    if logger.handlers:
        return logger
    
    # Format standardisé
    formatter = logging.Formatter(
        log_config.FORMAT,
        datefmt=log_config.DATE_FORMAT
    )
    
    # ==================== HANDLER FICHIER ====================
    
    # Fichier de log rotatif (max 5 fichiers de 5MB chacun)
    log_file = LOG_DIR / f"amazon_tracker_{TIMESTAMP}.log"
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # ==================== HANDLER CONSOLE ====================
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    logger.info(f"Logging configuré: {name} (niveau: {log_config.LEVEL})")
    logger.info(f"Fichier de log: {log_file}")
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Récupère ou crée un logger.
    
    Args:
        name: Nom du logger
        
    Returns:
        Logger
    """
    return logging.getLogger(name)


# ==================== CLASSES PERSONNALISÉES ====================

class ColoredFormatter(logging.Formatter):
    """Formatter avec couleurs pour la console."""
    
    # Couleurs ANSI
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Vert
        'WARNING': '\033[33m',    # Jaune
        'ERROR': '\033[31m',      # Rouge
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record: logging.LogRecord) -> str:
        """Formate un enregistrement de log avec couleurs.
        
        Args:
            record: Enregistrement à formater
            
        Returns:
            Enregistrement formaté avec couleurs
        """
        if sys.stdout.isatty():  # Seulement si c'est un terminal
            levelname = record.levelname
            color = self.COLORS.get(levelname, self.COLORS['INFO'])
            record.levelname = f"{color}{levelname}{self.COLORS['RESET']}"
        
        return super().format(record)


class FileLogger:
    """Utilitaire pour écrire les logs dans des fichiers séparés."""
    
    @staticmethod
    def get_file_logger(name: str, filename: str) -> logging.Logger:
        """Crée un logger qui écrit dans un fichier spécifique.
        
        Args:
            name: Nom du logger
            filename: Nom du fichier
            
        Returns:
            Logger configuré
        """
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        
        # Crée le handler de fichier
        file_path = LOG_DIR / filename
        handler = logging.FileHandler(file_path, encoding='utf-8')
        handler.setLevel(logging.DEBUG)
        
        # Formate l'output
        formatter = logging.Formatter(
            log_config.FORMAT,
            datefmt=log_config.DATE_FORMAT
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger


# ==================== LOGGERS SPÉCIALISÉS ====================

# Logger principal
logger = setup_logging("amazon_tracker")

# Loggers spécialisés
logger_search = get_logger("amazon_tracker.search")
logger_ai = get_logger("amazon_tracker.ai")
logger_database = get_logger("amazon_tracker.database")
logger_network = get_logger("amazon_tracker.network")
logger_ui = get_logger("amazon_tracker.ui")
logger_errors = FileLogger.get_file_logger("amazon_tracker.errors", "errors.log")


# ==================== UTILITAIRES DE LOG ====================

def log_exception(logger_instance: logging.Logger, exception: Exception, context: str = "") -> None:
    """Enregistre une exception avec contexte.
    
    Args:
        logger_instance: Logger à utiliser
        exception: Exception à enregistrer
        context: Contexte supplémentaire
    """
    context_str = f" - {context}" if context else ""
    logger_instance.error(
        f"Exception: {type(exception).__name__}: {str(exception)}{context_str}",
        exc_info=True
    )
    logger_errors.error(
        f"Exception: {type(exception).__name__}: {str(exception)}{context_str}",
        exc_info=True
    )


def log_performance(logger_instance: logging.Logger, operation: str, duration: float) -> None:
    """Enregistre les performances d'une opération.
    
    Args:
        logger_instance: Logger à utiliser
        operation: Nom de l'opération
        duration: Durée en secondes
    """
    if duration > 5.0:
        logger_instance.warning(f"Opération lente: {operation} ({duration:.2f}s)")
    else:
        logger_instance.debug(f"Opération: {operation} ({duration:.2f}s)")


# Initialisation au chargement du module
if __name__ == "__main__":
    logger.info("Module de logging initialisé")
    logger.debug("Message de debug")
    logger.warning("Message d'avertissement")
    logger.error("Message d'erreur")
