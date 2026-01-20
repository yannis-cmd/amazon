"""
Configuration centralisée pour Amazon Tracker Pro

Ce module contient toutes les constantes et configurations
de l'application pour faciliter la maintenance et les mises à jour.
"""

from dataclasses import dataclass
from typing import Final

# ==================== VERSIONS ====================

__version__: Final[str] = "1.0.0"
__author__: Final[str] = "Development Team"
__date__: Final[str] = "2026-01-18"
__license__: Final[str] = "MIT"


# ==================== CONFIGURATION ====================

@dataclass(frozen=True)
class UIConfig:
    """Configuration de l'interface utilisateur"""
    WINDOW_WIDTH: int = 1200
    WINDOW_HEIGHT: int = 850
    
    # Couleurs
    BG_DARK: str = "#1a1a1a"
    BG_MEDIUM: str = "#2d2d2d"
    BG_LIGHT: str = "#3a3a3a"
    FG_TEXT: str = "#ffffff"
    ACCENT_COLOR: str = "#FF9900"  # Couleur Amazon
    
    # Polices
    FONT_NORMAL: tuple = ('Arial', 9)
    FONT_BOLD: tuple = ('Arial', 9, 'bold')
    FONT_TITLE: tuple = ('Arial', 18, 'bold')
    
    # Dimensions
    FRAME_PADDING: int = 15
    BUTTON_PADDING: int = 8


@dataclass(frozen=True)
class DataConfig:
    """Configuration des données et fichiers"""
    DB_FILE: str = "articles_tracked.json"
    CACHE_FILE: str = "search_cache.json"
    LOG_FILE: str = "amazon_tracker.log"
    
    # Limites
    MAX_RESULTS: int = 10
    PRICE_HISTORY_DAYS: int = 30
    MAX_QUERY_LENGTH: int = 200


@dataclass(frozen=True)
class AmazonConfig:
    """Configuration spécifique à Amazon"""
    BASE_URL: str = "https://www.amazon.fr"
    SEARCH_URL: str = "https://www.amazon.fr/s?k={query}&ref=nb_sb_noss_2"
    
    USER_AGENT: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
    
    # Timeouts
    REQUEST_TIMEOUT: int = 10
    MIN_SEARCH_DELAY: float = 1.0  # Délai minimum entre requêtes (respect du serveur)
    
    # Headers
    LANGUAGE: str = "fr-FR"
    ENCODING: str = "utf-8"


@dataclass(frozen=True)
class AIConfig:
    """Configuration de l'Assistant IA"""
    # Profils utilisateur
    PROFILES = {
        "beginner": {
            "expertise": 3,
            "level": "débutant",
            "description": "Nouvel utilisateur, besoin de simplification"
        },
        "intermediate": {
            "expertise": 5,
            "level": "intermédiaire",
            "description": "Utilisateur ayant quelques connaissances"
        },
        "advanced": {
            "expertise": 8,
            "level": "avancé",
            "description": "Utilisateur technique"
        }
    }
    
    # Budget ranges
    BUDGET_RANGES = {
        "<20": {
            "label": "Moins de 20€",
            "min": 0,
            "max": 20
        },
        "20-50": {
            "label": "20 à 50€",
            "min": 20,
            "max": 50
        },
        "50-100": {
            "label": "50 à 100€",
            "min": 50,
            "max": 100
        },
        "100-200": {
            "label": "100 à 200€",
            "min": 100,
            "max": 200
        },
        ">200": {
            "label": "Plus de 200€",
            "min": 200,
            "max": 999999
        }
    }


@dataclass(frozen=True)
class LogConfig:
    """Configuration du logging"""
    LEVEL: str = "INFO"
    FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"


# ==================== INSTANCES GLOBALES ====================

ui_config = UIConfig()
data_config = DataConfig()
amazon_config = AmazonConfig()
ai_config = AIConfig()
log_config = LogConfig()
