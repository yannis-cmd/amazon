"""
ARCHITECTURE.md - Documentation d'architecture

Amazon Tracker Pro - Architecture et Design Patterns
====================================================

## Vue d'ensemble

Amazon Tracker Pro est une application Python avec interface tkinter pour tracker
les prix des produits Amazon, notamment les souris gamer, avec assistance IA.

### Stack Technologique
- **Langage**: Python 3.13
- **GUI**: tkinter + ttk
- **Web Scraping**: requests + BeautifulSoup4
- **Threading**: threading (opérations non-bloquantes)
- **Data**: JSON (stockage local)
- **Logging**: logging (stdlib)
- **Type Hints**: typing (Python 3.13+)


## Structure des Modules

```
amazon_tracker/
├── amazon_tracker.py       # Application principale (GUI + logique)
├── config.py               # Configuration centralisée
├── constants.py            # Constantes et messages
├── utils.py               # Utilitaires réutilisables
├── types.py               # Type hints personnalisés
├── logger.py              # Configuration du logging
├── exceptions.py          # Exceptions personnalisées
├── validators.py          # (À créer) Validateurs
├── scrapers.py            # (À créer) Scrapers web séparés
├── ai_engine.py           # (À créer) Moteur IA séparé
├── database.py            # (À créer) Gestion base de données
├── requirements.txt       # Dépendances
├── .gitignore            # Fichiers à ignorer
├── .env.example           # Exemple de configuration
├── LICENSE                # MIT License
├── README.md              # Documentation utilisateur
├── ARCHITECTURE.md        # Cette documentation
├── SECURITY.md            # Politique de sécurité
├── CONTRIBUTING.md        # Guide de contribution
└── logs/                  # (Créé au runtime) Fichiers de log
```


## Patterns d'Architecture

### 1. Configuration Centralisée (Config Pattern)

**Fichier**: `config.py`

Toutes les constantes sont centralisées dans des dataclasses `frozen`:

```python
@dataclass(frozen=True)
class UIConfig:
    WINDOW_WIDTH: int = 1200
    WINDOW_HEIGHT: int = 850
    # ...

ui_config = UIConfig()
```

**Avantages**:
- Facile à modifier
- Type-safe
- Centralisé
- Pas de magic numbers dans le code

### 2. Logging Structuré (Logger Pattern)

**Fichier**: `logger.py`

```python
from logger import setup_logging, logger

logger = setup_logging("amazon_tracker")
logger.info("Message")
logger.error("Erreur", exc_info=True)
```

**Niveaux**:
- DEBUG: Informations détaillées
- INFO: Événements normaux
- WARNING: Situations anormales
- ERROR: Erreurs graves
- CRITICAL: Erreurs très graves

### 3. Gestion d'Erreurs Personnalisée (Exception Pattern)

**Fichier**: `exceptions.py`

```python
try:
    validate_search_query(query)
except ValidationException as e:
    logger.error(f"Validation échouée: {e.message} (code: {e.error_code})")
```

### 4. Type Hints Stricts

**Fichier**: `types.py`

```python
def search_article(self, query: str) -> List[Dict[str, Any]]:
    """Recherche un article."""
    pass
```

Tous les paramètres et retours sont typés.

### 5. Utilitaires Réutilisables

**Fichier**: `utils.py`

Fonctions générales utilisées partout:
- `validate_*()` - Validations
- `extract_*()` - Extraction de données
- `format_*()` - Formatage
- `load_json()` / `save_json()` - I/O
- `open_link()` - Navigation web

### 6. Constants Centralisées

**Fichier**: `constants.py`

Messages, regex patterns, codes d'erreur, délais, limites

```python
MESSAGES["search_start"]
PATTERNS["budget_simple"]
ERROR_CODES["SEARCH_FAILED"]
```


## Flux de Données

### Flux de Recherche

```
Utilisateur tape requête
         ↓
GUI valide la requête (utils.validate_search_query)
         ↓
Lancement thread non-bloquant (threading)
         ↓
Recherche Amazon réelle avec requests + BeautifulSoup4
         ↓
Fallback si erreur (alternative search)
         ↓
Filtrage des résultats
         ↓
Cache local (search_cache.json)
         ↓
Affichage dans GUI (update_results_display)
         ↓
Persistence DB (articles_tracked.json)
```

### Flux de Chat IA

```
Utilisateur tape message
         ↓
Analyse d'intent (5 étapes)
         ↓
Détection profil utilisateur
         ↓
Extraction contexte (budget, produit, etc.)
         ↓
Génération réponse IA (customisée)
         ↓
Format réponse courte (~10 lignes)
         ↓
Ask pour lien si pertinent
         ↓
Affichage dans GUI
```

### Flux de Tracking Prix

```
Produit ajouté au tracking
         ↓
Stocké dans articles_tracked.json
         ↓
Recherche périodique (polling)
         ↓
Comparaison prix ancien/nouveau
         ↓
Alerte si prix change
         ↓
Historique prix mis à jour (price_history)
         ↓
Graphique actualisé
```


## Conventions de Codage

### Nommage

- **Classes**: PascalCase (`AmazonTracker`, `UIConfig`)
- **Fonctions/Méthodes**: snake_case (`search_article`, `validate_query`)
- **Constantes**: UPPER_SNAKE_CASE (`MAX_RESULTS`, `BASE_URL`)
- **Méthodes privées**: `_private_method()`
- **Variables temporaires**: `_tmp`, `_temp`

### Docstrings

Format Google:

```python
def search_article(self, query: str) -> List[Dict[str, Any]]:
    """Recherche les articles correspondant à la requête.
    
    Utilise la scraping Amazon réelle ou fallback en cas d'erreur.
    Résultats mis en cache pour éviter requêtes répétées.
    
    Args:
        query: Requête de recherche (ex: "souris gamer")
        
    Returns:
        Liste de dictionnaires avec: id, name, price, url, etc.
        
    Raises:
        ValidationException: Si requête invalide
        SearchException: Si recherche échoue
        
    Example:
        >>> results = tracker.search_article("souris gamer")
        >>> print(results[0]['name'])
        "Souris Gamer RGB 16000 DPI"
        
    Note:
        Les résultats sont limités à MAX_RESULTS (10 par défaut).
        Cache automatique pendant 1h.
    """
```

### Imports

Ordre standard:
1. Imports stdlib
2. Imports third-party
3. Imports locaux

```python
# Stdlib
import tkinter as tk
from typing import Dict, List, Any
import logging

# Third-party
import requests
from bs4 import BeautifulSoup

# Local
from config import ui_config
from utils import validate_search_query
from logger import logger
```

### Type Hints

Toujours typer les paramètres et retours:

```python
# ❌ Mauvais
def search(query):
    return results

# ✅ Bon
def search(query: str) -> List[Dict[str, Any]]:
    return results
```


## Gestion des Erreurs

### Pattern Try-Except

```python
try:
    results = self._search_amazon_real(query)
except NetworkException as e:
    logger.error(f"Erreur réseau: {e.message}")
    results = self._search_amazon_alternative(query)
except SearchException as e:
    logger.error(f"Erreur recherche: {e.message}")
    raise
except Exception as e:
    logger.error(f"Erreur inattendue: {str(e)}", exc_info=True)
    raise
```

### Rate Limiting

```python
def _apply_rate_limit(self) -> None:
    """Applique délai minimum entre requêtes."""
    if hasattr(self, '_last_request_time'):
        elapsed = time.time() - self._last_request_time
        if elapsed < amazon_config.MIN_SEARCH_DELAY:
            time.sleep(amazon_config.MIN_SEARCH_DELAY - elapsed)
```


## Testing

### Futurs tests à ajouter

```python
# tests/
├── test_utils.py          # Tests des utilitaires
├── test_validators.py     # Tests des validateurs
├── test_search.py         # Tests de recherche
├── test_ai.py            # Tests IA
├── test_database.py      # Tests base de données
└── test_integration.py   # Tests intégration
```

Exemple:

```python
def test_validate_search_query():
    assert validate_search_query("souris gamer") == True
    assert validate_search_query("") == False
    assert validate_search_query("x" * 300) == False
```


## Performance

### Optimisations actuelles

1. **Caching**: Résultats recherche en cache (1h)
2. **Threading**: Interface non-bloquante
3. **Rate Limiting**: Respect du serveur AWS
4. **Lazy Loading**: Graphiques générés à demande

### Métriques à suivre

- Temps de recherche < 5s
- Temps de réponse IA < 2s
- Mémoire < 200MB
- Temps démarrage < 3s


## Sécurité

### Points d'attention

1. **Input Validation**: Toutes les entrées utilisateur validées
2. **XSS Prevention**: Échappement HTML/caractères spéciaux
3. **Path Traversal**: Chemins validés
4. **SQL Injection**: JSON, pas SQL (safe)
5. **Rate Limiting**: Délai minimum entre requêtes

Voir [SECURITY.md](SECURITY.md) pour détails.


## Dépendances

```
requests>=2.31.0          # HTTP client
beautifulsoup4>=4.12.0   # Web scraping
lxml>=4.9.0              # Parser XML/HTML
```

Aucune dépendance pour tkinter (stdlib).


## Roadmap

### V1.0 (Actuel)
- ✅ Recherche Amazon
- ✅ Tracking prix
- ✅ Assistant IA
- ✅ Graphiques prix
- ✅ Interface sombre

### V1.1
- ⏳ Recherche multi-marchands
- ⏳ Notifications email
- ⏳ Export données (CSV, PDF)
- ⏳ Mode clair

### V2.0
- ⏳ Application mobile
- ⏳ Base de données serveur
- ⏳ ML pour prédictions
- ⏳ API REST


## Contribution

Voir [CONTRIBUTING.md](CONTRIBUTING.md) pour les guidelines.

### Code Quality Checklist

- [ ] Type hints complets
- [ ] Docstrings Google format
- [ ] Tests unitaires
- [ ] Logging approprié
- [ ] Gestion d'erreurs robuste
- [ ] Pas d'imports inutilisés
- [ ] PEP 8 respecté
- [ ] Pas de TODO comments

### Pre-commit Checklist

```bash
# Vérifier syntaxe
python -m py_compile *.py

# Vérifier imports
python -m pylint --errors-only *.py

# Formater (optionnel)
python -m black *.py --line-length 88
```


## Support et Debug

### Fichiers de log

```
logs/
├── amazon_tracker_20260118_143022.log  # Log principal
├── errors.log                           # Erreurs uniquement
└── ...
```

### Debug mode

```python
# Dans amazon_tracker.py (en haut)
import logging
logging.getLogger("amazon_tracker").setLevel(logging.DEBUG)
```

### Common Issues

| Problème | Cause | Solution |
|----------|-------|----------|
| Pas de résultats | Blogging Amazon | Utiliser fallback |
| Lent | Réseau lent | Augmenter timeout |
| Crash IA | Parsing error | Vérifier input |
| DB corrompue | Corruption JSON | Supprimer .json |


## Ressources

- [Python Docs](https://docs.python.org/3/)
- [tkinter Reference](https://docs.python.org/3/library/tkinter.html)
- [BeautifulSoup Docs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests Library](https://requests.readthedocs.io/)


---

**Dernière mise à jour**: 18 Janvier 2026
**Version**: 1.0.0
**Auteur**: Development Team
"""
