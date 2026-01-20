"""
Exceptions personnalisées pour Amazon Tracker Pro

Ce module définit toutes les exceptions spécifiques à l'application
pour une meilleure gestion des erreurs et du débogage.
"""

from typing import Optional


class AmazonTrackerException(Exception):
    """Exception de base pour Amazon Tracker Pro."""
    
    def __init__(self, message: str, error_code: int = 999):
        """Initialise l'exception.
        
        Args:
            message: Message d'erreur
            error_code: Code d'erreur
        """
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class SearchException(AmazonTrackerException):
    """Exception levée lors d'une erreur de recherche."""
    
    def __init__(self, message: str = "Erreur lors de la recherche", error_code: int = 101):
        super().__init__(message, error_code)


class NetworkException(AmazonTrackerException):
    """Exception levée lors d'un problème réseau."""
    
    def __init__(self, message: str = "Erreur réseau", error_code: int = 102):
        super().__init__(message, error_code)


class ParseException(AmazonTrackerException):
    """Exception levée lors d'une erreur de parsing."""
    
    def __init__(self, message: str = "Erreur de parsing", error_code: int = 103):
        super().__init__(message, error_code)


class ValidationException(AmazonTrackerException):
    """Exception levée lors d'une validation échouée."""
    
    def __init__(self, message: str = "Erreur de validation", error_code: int = 104):
        super().__init__(message, error_code)


class FileException(AmazonTrackerException):
    """Exception levée lors d'une erreur d'accès fichier."""
    
    def __init__(self, message: str = "Erreur d'accès fichier", error_code: int = 105):
        super().__init__(message, error_code)


class RateLimitException(AmazonTrackerException):
    """Exception levée lors du dépassement du rate limit."""
    
    def __init__(self, message: str = "Trop de requêtes", error_code: int = 106):
        super().__init__(message, error_code)


class InvalidInputException(AmazonTrackerException):
    """Exception levée lors d'une entrée invalide."""
    
    def __init__(self, message: str = "Entrée invalide", error_code: int = 104):
        super().__init__(message, error_code)


class DatabaseException(AmazonTrackerException):
    """Exception levée lors d'une erreur de base de données."""
    
    def __init__(self, message: str = "Erreur de base de données", error_code: int = 105):
        super().__init__(message, error_code)


class TimeoutException(AmazonTrackerException):
    """Exception levée lors d'un timeout."""
    
    def __init__(self, message: str = "Timeout", error_code: int = 107):
        super().__init__(message, error_code)


class ConfigException(AmazonTrackerException):
    """Exception levée lors d'une erreur de configuration."""
    
    def __init__(self, message: str = "Erreur de configuration", error_code: int = 108):
        super().__init__(message, error_code)


# ==================== CONTEXT MANAGERS ====================

class ExceptionContext:
    """Context manager pour capturer et logger les exceptions."""
    
    def __init__(self, logger, operation: str, reraise: bool = True):
        """Initialise le context manager.
        
        Args:
            logger: Logger à utiliser
            operation: Nom de l'opération
            reraise: Si True, lève à nouveau l'exception après logging
        """
        self.logger = logger
        self.operation = operation
        self.reraise = reraise
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Traite l'exception si elle s'est produite.
        
        Args:
            exc_type: Type de l'exception
            exc_val: Valeur de l'exception
            exc_tb: Traceback
            
        Returns:
            True pour supprimer l'exception, False pour la propager
        """
        if exc_type is not None:
            self.logger.error(
                f"Exception dans {self.operation}: {exc_type.__name__}: {exc_val}",
                exc_info=True
            )
            return not self.reraise
        return False


# ==================== DÉCORATEURS ====================

def handle_exceptions(logger, default_return=None):
    """Décorateur pour gérer les exceptions automatiquement.
    
    Args:
        logger: Logger à utiliser
        default_return: Valeur à retourner en cas d'exception
        
    Returns:
        Fonction décorée
        
    Example:
        @handle_exceptions(logger)
        def ma_fonction():
            raise ValueError("Erreur")
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(
                    f"Exception dans {func.__name__}: {type(e).__name__}: {str(e)}",
                    exc_info=True
                )
                return default_return
        return wrapper
    return decorator


def retry_on_exception(logger, max_attempts: int = 3, delay: float = 1.0):
    """Décorateur pour réessayer une fonction en cas d'exception.
    
    Args:
        logger: Logger à utiliser
        max_attempts: Nombre maximum de tentatives
        delay: Délai entre les tentatives (secondes)
        
    Returns:
        Fonction décorée
        
    Example:
        @retry_on_exception(logger, max_attempts=3)
        def appel_api():
            return requests.get("https://api.example.com")
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            import time
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        logger.error(f"Tous les essais ont échoué pour {func.__name__}")
                        raise
                    
                    logger.warning(
                        f"Tentative {attempt}/{max_attempts} échouée pour {func.__name__}: {str(e)}. "
                        f"Nouvelle tentative dans {delay}s..."
                    )
                    time.sleep(delay)
        
        return wrapper
    return decorator
