"""
Définitions de types pour Amazon Tracker Pro

Ce module centralise tous les type hints personnalisés utilisés
dans l'application pour améliorer la cohérence et la maintenabilité.
"""

from typing import TypedDict, Optional, List, Dict, Any, Callable, Union
from dataclasses import dataclass
from datetime import datetime


# ==================== TYPEDDICTS ====================

class ProductData(TypedDict):
    """Type pour les données de produit."""
    id: str
    name: str
    price: float
    original_price: Optional[float]
    url: str
    description: Optional[str]
    image_url: Optional[str]
    rating: Optional[float]
    reviews_count: Optional[int]
    in_stock: bool
    timestamp: datetime


class PriceHistory(TypedDict):
    """Type pour l'historique des prix."""
    timestamp: datetime
    price: float
    in_stock: bool


class SearchResult(TypedDict):
    """Type pour un résultat de recherche."""
    products: List[ProductData]
    total_found: int
    source: str  # "amazon" ou "fallback"
    timestamp: datetime


class UserProfile(TypedDict):
    """Type pour le profil utilisateur."""
    level: str  # "beginner", "intermediate", "advanced"
    budget: Dict[str, float]  # {"min": X, "max": Y}
    preferences: Dict[str, Any]
    search_history: List[str]


class AIAnalysis(TypedDict):
    """Type pour l'analyse IA."""
    intent: str
    confidence: float
    user_profile: str
    budget: Optional[Dict[str, float]]
    recommendations: List[str]
    context: Dict[str, Any]


# ==================== DATACLASSES ====================

@dataclass
class Mouse:
    """Représente une souris avec ses propriétés."""
    id: str
    name: str
    price: float
    url: str
    dpi: Optional[int] = None
    buttons: Optional[int] = None
    weight: Optional[float] = None
    wireless: bool = False
    rgb: bool = False
    brand: Optional[str] = None
    rating: Optional[float] = None
    in_stock: bool = True
    timestamp: datetime = None
    
    def __post_init__(self):
        """Initialise les valeurs par défaut."""
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def __str__(self) -> str:
        """Représentation en chaîne."""
        return f"{self.name} - {self.price}€"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit en dictionnaire."""
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'url': self.url,
            'dpi': self.dpi,
            'buttons': self.buttons,
            'weight': self.weight,
            'wireless': self.wireless,
            'rgb': self.rgb,
            'brand': self.brand,
            'rating': self.rating,
            'in_stock': self.in_stock,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }


@dataclass
class SearchQuery:
    """Représente une requête de recherche."""
    query: str
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    filters: Dict[str, Any] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        """Initialise les valeurs par défaut."""
        if self.filters is None:
            self.filters = {}
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def is_valid(self) -> bool:
        """Vérifie si la requête est valide."""
        return bool(self.query and len(self.query.strip()) > 0)
    
    def __str__(self) -> str:
        """Représentation en chaîne."""
        result = f"Recherche: {self.query}"
        if self.budget_min and self.budget_max:
            result += f" (Budget: {self.budget_min}€ - {self.budget_max}€)"
        return result


@dataclass
class CacheEntry:
    """Représente une entrée de cache."""
    key: str
    data: Any
    timestamp: datetime
    ttl: int  # Time to live en secondes
    
    def is_expired(self) -> bool:
        """Vérifie si l'entrée a expiré."""
        from datetime import datetime, timedelta
        return datetime.now() > (self.timestamp + timedelta(seconds=self.ttl))


@dataclass
class APIResponse:
    """Représente une réponse d'API."""
    status_code: int
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: datetime = None
    duration: float = 0.0  # Durée de la requête en secondes
    
    def __post_init__(self):
        """Initialise les valeurs par défaut."""
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def is_success(self) -> bool:
        """Vérifie si la réponse est un succès."""
        return 200 <= self.status_code < 300
    
    def is_error(self) -> bool:
        """Vérifie si la réponse est une erreur."""
        return self.status_code >= 400


# ==================== ALIASES ====================

# Aliases courants
JSONType = Union[Dict[str, Any], List[Any], str, int, float, bool, None]
CallbackFunction = Callable[..., None]
ValidationFunction = Callable[[Any], bool]
FormatterFunction = Callable[[Any], str]

# Alias pour les données
ProductList = List[ProductData]
PriceHistoryList = List[PriceHistory]
SearchResultList = List[SearchResult]

# Alias pour les fonctions communes
Filter = Callable[[Any], bool]
Transform = Callable[[Any], Any]
Validator = Callable[[Any], bool]


# ==================== UNIONS ====================

# Peut être une chaîne (simple) ou un dictionnaire (format complexe)
BudgetInput = Union[str, Dict[str, float]]

# Peut être une valeur unique ou une liste
PriceInput = Union[float, List[float]]

# Peut être un nom de fichier ou un chemin Path
FilePath = Union[str, "Path"]
