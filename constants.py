"""
Constantes globales pour Amazon Tracker Pro

Toutes les valeurs magiques et constantes sont centralisées ici
pour améliorer la maintenabilité et faciliter les modifications.
"""

from typing import Final

# ==================== MESSAGES ====================

MESSAGES: Final[dict] = {
    "search_start": "Recherche en cours...",
    "search_success": "Recherche complétée",
    "search_error": "Erreur lors de la recherche",
    "loading": "Chargement en cours...",
    "no_results": "Aucun résultat trouvé",
    "invalid_query": "Requête invalide",
    "rate_limit": "Trop de requêtes, veuillez patienter",
    "network_error": "Erreur réseau - Impossible de se connecter",
    "parse_error": "Erreur lors du traitement des données",
    "link_unavailable": "Lien indisponible ou produit supprimé",
    "link_opened": "Lien ouvert dans le navigateur",
    "link_failed": "Impossible d'ouvrir le lien",
}

# ==================== CODES D'ERREUR ====================

ERROR_CODES: Final[dict] = {
    "NO_ERROR": 0,
    "SEARCH_FAILED": 101,
    "NETWORK_ERROR": 102,
    "PARSE_ERROR": 103,
    "INVALID_INPUT": 104,
    "FILE_ERROR": 105,
    "RATE_LIMITED": 106,
    "UNKNOWN": 999,
}

# ==================== REGEX PATTERNS ====================

PATTERNS: Final[dict] = {
    "budget_simple": r"(\d+)€?",
    "budget_range": r"(\d+)\s*(?:à|-)\s*(\d+)€?",
    "link_amazon": r"https?://(?:www\.)?amazon\.\w+/(?:[\w-]+/)*(?:dp|gp)/([A-Z0-9]{10})",
    "price": r"€?\s*(\d+(?:[.,]\d+)?)",
    "email": r"[\w\.-]+@[\w\.-]+\.\w+",
}

# ==================== STATUTS ====================

STATUS: Final[dict] = {
    "PENDING": "en_attente",
    "ACTIVE": "actif",
    "TRACKING": "suivi",
    "ALERT": "alerte",
    "COMPLETED": "complété",
}

# ==================== DÉLAIS ====================

DELAYS: Final[dict] = {
    "rate_limit": 1.0,  # secondes
    "search_timeout": 10,  # secondes
    "cache_expiry": 3600,  # secondes (1 heure)
    "ui_update": 100,  # millisecondes
    "animation": 200,  # millisecondes
}

# ==================== LIMITES ====================

LIMITS: Final[dict] = {
    "max_tracked_items": 100,
    "max_search_results": 20,
    "max_search_history": 50,
    "max_price_history": 365,
    "max_query_length": 200,
    "min_price_alert": 1,
    "max_price_alert": 999999,
}

# ==================== SUFFIXES POUR LES TAILLES ====================

SIZE_SUFFIXES: Final[list] = ["B", "KB", "MB", "GB", "TB"]

# ==================== CODES DE RÉPONSE HTTP ====================

HTTP_CODES: Final[dict] = {
    "OK": 200,
    "CREATED": 201,
    "BAD_REQUEST": 400,
    "NOT_FOUND": 404,
    "TOO_MANY_REQUESTS": 429,
    "SERVER_ERROR": 500,
    "SERVICE_UNAVAILABLE": 503,
}

# ==================== TYPES DE DONNÉES ====================

DATA_TYPES: Final[dict] = {
    "STRING": str,
    "INTEGER": int,
    "FLOAT": float,
    "BOOLEAN": bool,
    "LIST": list,
    "DICT": dict,
}
