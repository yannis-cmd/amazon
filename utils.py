"""
Utilitaires générales pour Amazon Tracker Pro

Ce module contient les fonctions utilitaires réutilisables
pour améliorer la qualité et la maintenabilité du code.
"""

import json
import logging
import os
import re
import webbrowser
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path

from constants import MESSAGES, PATTERNS, SIZE_SUFFIXES
from config import data_config, amazon_config

logger = logging.getLogger(__name__)


# ==================== VALIDATION ====================

def validate_search_query(query: str) -> bool:
    """Valide une requête de recherche.
    
    Args:
        query: Requête à valider
        
    Returns:
        True si valide, False sinon
        
    Example:
        >>> validate_search_query("souris gamer")
        True
        >>> validate_search_query("")
        False
    """
    if not query or not isinstance(query, str):
        logger.warning(f"Requête invalide: {query}")
        return False
    
    if len(query.strip()) == 0:
        logger.warning("Requête vide")
        return False
    
    if len(query) > data_config.MAX_QUERY_LENGTH:
        logger.warning(f"Requête trop longue: {len(query)} > {data_config.MAX_QUERY_LENGTH}")
        return False
    
    return True


def validate_price(price: float) -> bool:
    """Valide un prix.
    
    Args:
        price: Prix à valider
        
    Returns:
        True si valide, False sinon
    """
    try:
        price_float = float(price)
        return 0 < price_float < 999999
    except (ValueError, TypeError):
        logger.warning(f"Prix invalide: {price}")
        return False


def validate_budget_range(budget_min: float, budget_max: float) -> bool:
    """Valide une plage de budget.
    
    Args:
        budget_min: Budget minimum
        budget_max: Budget maximum
        
    Returns:
        True si valide, False sinon
    """
    if not validate_price(budget_min) or not validate_price(budget_max):
        return False
    
    if budget_min > budget_max:
        logger.warning(f"Budget invalide: {budget_min} > {budget_max}")
        return False
    
    return True


# ==================== EXTRACTION ET PARSING ====================

def extract_budget_from_text(text: str) -> Optional[Dict[str, float]]:
    """Extrait le budget d'un texte donné.
    
    Args:
        text: Texte contenant le budget
        
    Returns:
        Dict avec min et max, ou None si non trouvé
        
    Example:
        >>> extract_budget_from_text("Je veux une souris pour 50€")
        {'min': 50.0, 'max': 50.0}
    """
    if not text:
        return None
    
    # Cherche d'abord un format "min-max"
    range_match = re.search(PATTERNS["budget_range"], text)
    if range_match:
        try:
            budget_min = float(range_match.group(1))
            budget_max = float(range_match.group(2))
            return {"min": budget_min, "max": budget_max}
        except (ValueError, IndexError):
            pass
    
    # Cherche un budget simple
    price_matches = re.findall(PATTERNS["price"], text)
    if price_matches:
        try:
            prices = [float(p.replace(',', '.')) for p in price_matches]
            return {"min": min(prices), "max": max(prices)}
        except ValueError:
            pass
    
    return None


def extract_amazon_links(text: str) -> List[str]:
    """Extrait tous les liens Amazon d'un texte.
    
    Args:
        text: Texte contenant les liens
        
    Returns:
        Liste des liens trouvés
    """
    if not text:
        return []
    
    links = re.findall(PATTERNS["link_amazon"], text)
    return [f"{amazon_config.BASE_URL}/dp/{link}" for link in links]


def extract_prices(text: str) -> List[float]:
    """Extrait tous les prix d'un texte.
    
    Args:
        text: Texte contenant les prix
        
    Returns:
        Liste des prix trouvés
    """
    if not text:
        return []
    
    prices = re.findall(PATTERNS["price"], text)
    try:
        return [float(p.replace(',', '.')) for p in prices]
    except ValueError:
        logger.warning(f"Impossible d'extraire les prix de: {text}")
        return []


# ==================== FORMATAGE ====================

def format_price(price: float, currency: str = "€") -> str:
    """Formate un prix avec devise.
    
    Args:
        price: Prix à formater
        currency: Devise (défaut: €)
        
    Returns:
        Prix formaté (ex: "29,99€")
    """
    if not validate_price(price):
        return "N/A"
    
    return f"{price:,.2f}".replace(',', ' ').replace('.', ',') + currency


def format_file_size(bytes_size: int) -> str:
    """Formate une taille de fichier.
    
    Args:
        bytes_size: Taille en octets
        
    Returns:
        Taille formatée (ex: "2.5 MB")
    """
    try:
        for suffix in SIZE_SUFFIXES:
            if bytes_size < 1024.0:
                return f"{bytes_size:.2f} {suffix}"
            bytes_size /= 1024.0
    except (ValueError, TypeError):
        logger.warning(f"Impossible de formater la taille: {bytes_size}")
    
    return "N/A"


def format_datetime(dt: datetime) -> str:
    """Formate une date et heure.
    
    Args:
        dt: Datetime à formater
        
    Returns:
        Date formatée
    """
    try:
        return dt.strftime("%d/%m/%Y %H:%M:%S")
    except (ValueError, AttributeError):
        logger.warning(f"Impossible de formater la date: {dt}")
        return "N/A"


def format_message(message_key: str, **kwargs) -> str:
    """Récupère et formate un message prédéfini.
    
    Args:
        message_key: Clé du message dans MESSAGES
        **kwargs: Variables pour formater le message
        
    Returns:
        Message formaté
    """
    message = MESSAGES.get(message_key, "Erreur inconnue")
    try:
        return message.format(**kwargs) if kwargs else message
    except KeyError:
        logger.warning(f"Clé manquante dans le message: {message_key}")
        return message


# ==================== FICHIERS ET DONNÉES ====================

def ensure_file_exists(filepath: str) -> bool:
    """S'assure qu'un fichier existe, le crée s'il n'existe pas.
    
    Args:
        filepath: Chemin du fichier
        
    Returns:
        True si créé ou existant, False en cas d'erreur
    """
    try:
        path = Path(filepath)
        if not path.exists():
            path.touch()
            logger.info(f"Fichier créé: {filepath}")
        return True
    except Exception as e:
        logger.error(f"Erreur lors de la création du fichier {filepath}: {e}")
        return False


def load_json(filepath: str) -> Dict[str, Any]:
    """Charge un fichier JSON en toute sécurité.
    
    Args:
        filepath: Chemin du fichier JSON
        
    Returns:
        Dictionnaire chargé, {} si erreur
    """
    try:
        if not os.path.exists(filepath):
            logger.info(f"Fichier non trouvé: {filepath}")
            return {}
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            logger.info(f"Données chargées depuis {filepath}")
            return data
    except json.JSONDecodeError:
        logger.error(f"Erreur de décodage JSON: {filepath}")
        return {}
    except Exception as e:
        logger.error(f"Erreur lors du chargement de {filepath}: {e}")
        return {}


def save_json(data: Dict[str, Any], filepath: str) -> bool:
    """Sauvegarde les données en JSON en toute sécurité.
    
    Args:
        data: Données à sauvegarder
        filepath: Chemin de destination
        
    Returns:
        True si succès, False sinon
    """
    try:
        # Crée le répertoire s'il n'existe pas
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"Données sauvegardées dans {filepath}")
        return True
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde dans {filepath}: {e}")
        return False


# ==================== WEB ET NAVIGATION ====================

def open_link(url: str) -> bool:
    """Ouvre un lien dans le navigateur par défaut.
    
    Args:
        url: URL à ouvrir
        
    Returns:
        True si succès, False sinon
    """
    try:
        if not url or not isinstance(url, str):
            logger.warning(f"URL invalide: {url}")
            return False
        
        webbrowser.open(url)
        logger.info(f"Lien ouvert: {url}")
        return True
    except Exception as e:
        logger.error(f"Erreur lors de l'ouverture du lien {url}: {e}")
        return False


def validate_url(url: str) -> bool:
    """Valide un URL.
    
    Args:
        url: URL à valider
        
    Returns:
        True si valide, False sinon
    """
    try:
        return url.startswith(('http://', 'https://'))
    except AttributeError:
        return False


# ==================== STATISTIQUES ====================

def calculate_price_change(old_price: float, new_price: float) -> Tuple[float, str]:
    """Calcule la variation de prix en pourcentage.
    
    Args:
        old_price: Ancien prix
        new_price: Nouveau prix
        
    Returns:
        Tuple (pourcentage, tendance)
    """
    try:
        if old_price <= 0:
            return 0.0, "N/A"
        
        percentage = ((new_price - old_price) / old_price) * 100
        tendency = "↑ hausse" if percentage > 0 else "↓ baisse" if percentage < 0 else "→ stable"
        
        return round(percentage, 2), tendency
    except (ValueError, ZeroDivisionError):
        logger.warning(f"Erreur de calcul: {old_price} -> {new_price}")
        return 0.0, "N/A"


def get_average_price(prices: List[float]) -> float:
    """Calcule le prix moyen.
    
    Args:
        prices: Liste des prix
        
    Returns:
        Prix moyen
    """
    try:
        if not prices:
            return 0.0
        return sum(prices) / len(prices)
    except (ValueError, ZeroDivisionError):
        return 0.0


# ==================== SÉCURITÉ ====================

def sanitize_string(text: str, max_length: int = 1000) -> str:
    """Nettoie une chaîne de caractères.
    
    Args:
        text: Texte à nettoyer
        max_length: Longueur maximum
        
    Returns:
        Texte nettoyé
    """
    if not isinstance(text, str):
        return ""
    
    # Supprime les caractères de contrôle
    text = ''.join(char for char in text if ord(char) >= 32)
    
    # Limite la longueur
    return text[:max_length].strip()


def escape_html(text: str) -> str:
    """Échappe les caractères HTML spéciaux.
    
    Args:
        text: Texte à échapper
        
    Returns:
        Texte échappé
    """
    if not isinstance(text, str):
        return ""
    
    replacements = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;'
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text
