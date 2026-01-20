"""
Amazon Tracker Pro - Application de suivi et recommandation de souris Amazon

Module principal: Interface tkinter avec assistant IA pour recommander des souris
basé sur l'analyse des besoins utilisateur.

Auteur: Development Team
Version: 1.0.0
Date: 2026-01-18
License: MIT
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
import requests
from bs4 import BeautifulSoup
import threading
import time
from urllib.parse import quote
import re
import random
import webbrowser
from dataclasses import dataclass

# Import du module support client
try:
    from support_client.support_ui import SupportWindow
    SUPPORT_AVAILABLE = True
except ImportError:
    try:
        from support_ui import SupportWindow
        SUPPORT_AVAILABLE = True
    except ImportError:
        SUPPORT_AVAILABLE = False

# Import du module activity logging
try:
    from activity_logger import activity_logger
    ACTIVITY_LOGGER_AVAILABLE = True
except ImportError:
    try:
        from support_client.activity_logger import activity_logger
        ACTIVITY_LOGGER_AVAILABLE = True
    except ImportError:
        ACTIVITY_LOGGER_AVAILABLE = False
        activity_logger = None

# ==================== CONFIGURATION ====================

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('amazon_tracker.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# Constantes
class Config:
    """Configuration centralisée de l'application"""
    # UI
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 850
    BG_DARK = "#1a1a1a"
    BG_MEDIUM = "#2d2d2d"
    BG_LIGHT = "#3a3a3a"
    FG_TEXT = "#ffffff"
    ACCENT_COLOR = "#FF9900"
    
    # Données
    DB_FILE = "articles_tracked.json"
    CACHE_FILE = "search_cache.json"
    REQUEST_TIMEOUT = 10
    MAX_RESULTS = 10
    
    # Amazon
    AMAZON_URL = "https://www.amazon.fr"
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    
    # Price history
    PRICE_HISTORY_DAYS = 30
    
    # API
    MIN_SEARCH_DELAY = 1.0  # Délai minimum entre les requêtes


@dataclass
class Mouse:
    """Représentation d'une souris"""
    nom: str
    prix: str
    gaming: int
    work: int
    creative: int
    poids: str
    dpi: str
    type: str
    sensor: str
    details: str


class AmazonTrackerApp:
    """Application principale pour tracker les souris Amazon avec IA"""
    def __init__(self, root: tk.Tk) -> None:
        """
        Initialise l'application Amazon Tracker.
        
        Args:
            root: La fenêtre tkinter principale
            
        Raises:
            Exception: Si l'initialisation échoue
        """
        try:
            logger.info("Démarrage d'Amazon Tracker Pro...")
            
            self.root = root
            self.root.title("🛒 Amazon Tracker Pro - Suivi des Articles")
            self.root.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
            self.root.configure(bg=Config.BG_DARK)
            
            # État de l'application
            self.current_recommendation: Optional[Dict] = None
            self.last_search_time: float = 0.0
            self.search_results: List[Dict] = []
            self.tracked_articles: List[Dict] = []
            
            # Configuration du style sombre
            self._setup_dark_theme()
            
            # Base de données locale
            self.db_file = Config.DB_FILE
            self._load_database()
            
            # UI
            self._setup_ui()
            
            logger.info("Application démarrée avec succès")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation: {e}", exc_info=True)
            messagebox.showerror("Erreur", f"Erreur d'initialisation: {e}")
            raise
    
    def _setup_dark_theme(self) -> None:
        """Configure le thème sombre moderne avec tous les styles"""
        try:
            style = ttk.Style()
            style.theme_use('clam')
            
            # Configuration des styles
            style.configure('Dark.TLabel', 
                          background=Config.BG_DARK, 
                          foreground=Config.FG_TEXT, 
                          font=('Arial', 9))
            style.configure('Dark.TLabelframe', 
                          background=Config.BG_DARK, 
                          foreground=Config.FG_TEXT, 
                          borderwidth=1, 
                          relief='solid')
            style.configure('Dark.TLabelframe.Label', 
                          background=Config.BG_DARK, 
                          foreground=Config.ACCENT_COLOR, 
                          font=('Arial', 10, 'bold'))
            style.configure('Dark.TButton', 
                          background=Config.BG_LIGHT, 
                          foreground=Config.FG_TEXT, 
                          font=('Arial', 9, 'bold'), 
                          padding=8)
            style.map('Dark.TButton', 
                     background=[('active', Config.ACCENT_COLOR)])
            style.configure('Dark.TEntry', 
                          fieldbackground=Config.BG_LIGHT, 
                          foreground=Config.FG_TEXT, 
                          font=('Arial', 9), 
                          insertcolor=Config.ACCENT_COLOR)
            style.configure('Dark.TFrame', background=Config.BG_DARK)
            style.configure('Vertical.TScrollbar', 
                          background=Config.BG_LIGHT, 
                          troughcolor=Config.BG_MEDIUM, 
                          arrowcolor=Config.ACCENT_COLOR)
            
            logger.debug("Thème sombre configuré avec succès")
            
        except Exception as e:
            logger.warning(f"Erreur lors de la configuration du thème: {e}")
    
    def _load_database(self) -> None:
        """Charge la base de données locale ou crée une nouvelle"""
        try:
            if os.path.exists(self.db_file):
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Gérer les deux formats: ancien (liste) et nouveau (dictionnaire)
                    if isinstance(data, list):
                        self.tracked_articles = data
                        self.database = {"articles": data, "last_updated": datetime.now().isoformat()}
                    else:
                        self.database = data
                        self.tracked_articles = self.database.get("articles", [])
                    logger.info(f"Base de données chargée: {len(self.tracked_articles)} articles")
            else:
                self.database = {"articles": [], "last_updated": datetime.now().isoformat()}
                self.tracked_articles = []
                self._save_database()
                logger.info("Nouvelle base de données créée")
                
        except json.JSONDecodeError as e:
            logger.error(f"Erreur JSON: {e}")
            self.database = {"articles": []}
            self.tracked_articles = []
        except Exception as e:
            logger.error(f"Erreur lors du chargement: {e}")
            self.database = {"articles": []}
            self.tracked_articles = []
    
    def _save_database(self) -> None:
        """Sauvegarde la base de données locale"""
        try:
            self.database["last_updated"] = datetime.now().isoformat()
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(self.database, f, indent=2, ensure_ascii=False)
            logger.debug("Base de données sauvegardée")
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde: {e}")
        bg_medium = "#2d2d2d"
        bg_light = "#3a3a3a"
        fg_text = "#ffffff"
        accent_color = "#FF9900"  # Couleur Amazon
        
        # Configure les styles
        style.configure('Dark.TLabel', background=bg_dark, foreground=fg_text, font=('Arial', 9))
        style.configure('Dark.TLabelframe', background=bg_dark, foreground=fg_text, borderwidth=1, relief='solid')
        style.configure('Dark.TLabelframe.Label', background=bg_dark, foreground=accent_color, font=('Arial', 10, 'bold'))
        style.configure('Dark.TButton', background=bg_light, foreground=fg_text, font=('Arial', 9, 'bold'), padding=8)
        style.map('Dark.TButton', background=[('active', accent_color)])
        style.configure('Dark.TEntry', fieldbackground=bg_light, foreground=fg_text, font=('Arial', 9), insertcolor=accent_color)
        style.configure('Dark.TFrame', background=bg_dark)
        style.configure('Vertical.TScrollbar', background=bg_light, troughcolor=bg_medium, arrowcolor=accent_color)
    
    def _setup_ui(self) -> None:
        """Configure l'interface utilisateur avec un design moderne"""
        bg_dark = "#1a1a1a"
        bg_medium = "#2d2d2d"
        accent_color = "#FF9900"
        
        # Header
        header_frame = ttk.Frame(self.root, style='Dark.TFrame')
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        
        header_bg = tk.Canvas(header_frame, bg=bg_medium, height=60, relief=tk.FLAT, highlightthickness=0)
        header_bg.pack(fill=tk.X)
        header_bg.create_text(20, 30, text="🛒 Amazon Tracker Pro", font=('Arial', 18, 'bold'), fill=accent_color, anchor='w')
        
        # Frame supérieur - Recherche
        search_frame = ttk.LabelFrame(self.root, text="🔍 Rechercher un article Amazon", padding=15, style='Dark.TLabelframe')
        search_frame.pack(fill=tk.X, padx=15, pady=(15, 10))
        
        search_container = ttk.Frame(search_frame, style='Dark.TFrame')
        search_container.pack(fill=tk.X)
        
        ttk.Label(search_container, text="Mot-clé:", style='Dark.TLabel').pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_container, style='Dark.TEntry', width=50)
        self.search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.search_entry.bind('<Return>', lambda e: self.search_article())
        
        ttk.Button(search_container, text="🔎 Rechercher", command=self.search_article, style='Dark.TButton').pack(side=tk.LEFT, padx=5)
        
        # Frame pour les résultats et suivi (layout côte à côte)
        main_container = ttk.Frame(self.root, style='Dark.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Colonne gauche - Résultats de recherche
        left_column = ttk.Frame(main_container, style='Dark.TFrame')
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
        
        results_frame = ttk.LabelFrame(left_column, text="📦 Résultats de recherche", padding=10, style='Dark.TLabelframe')
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        scrollbar = ttk.Scrollbar(results_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.results_listbox = tk.Listbox(results_frame, yscrollcommand=scrollbar.set, height=12, 
                                         bg=bg_medium, fg="white", font=("Arial", 9), 
                                         selectmode=tk.SINGLE, relief=tk.FLAT, highlightthickness=0)
        self.results_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.results_listbox.yview)
        self.results_listbox.bind('<<ListboxSelect>>', self.on_result_select)
        
        # Colonne droite - Articles suivis
        right_column = ttk.Frame(main_container, style='Dark.TFrame')
        right_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(8, 0))
        
        tracked_frame = ttk.LabelFrame(right_column, text="⭐ Articles en suivi", padding=10, style='Dark.TLabelframe')
        tracked_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        scrollbar_tracked = ttk.Scrollbar(tracked_frame)
        scrollbar_tracked.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tracked_listbox = tk.Listbox(tracked_frame, yscrollcommand=scrollbar_tracked.set, height=12,
                                         bg=bg_medium, fg="white", font=("Arial", 9),
                                         selectmode=tk.SINGLE, relief=tk.FLAT, highlightthickness=0)
        self.tracked_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar_tracked.config(command=self.tracked_listbox.yview)
        
        # Frame détails article
        details_frame = ttk.LabelFrame(self.root, text="ℹ️ Détails de l'article", padding=10, style='Dark.TLabelframe')
        details_frame.pack(fill=tk.BOTH, padx=15, pady=(0, 10))
        
        self.details_text = scrolledtext.ScrolledText(details_frame, height=4, width=100, state=tk.DISABLED,
                                                      bg=bg_medium, fg="white", font=("Courier", 9),
                                                      relief=tk.FLAT, highlightthickness=0, insertbackground="#FF9900")
        self.details_text.pack(fill=tk.BOTH, expand=True)
        
        # Frame boutons action - organisé en grille
        button_frame = ttk.Frame(self.root, style='Dark.TFrame')
        button_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        # Ligne 1 de boutons
        buttons_row1 = ttk.Frame(button_frame, style='Dark.TFrame')
        buttons_row1.pack(fill=tk.X, pady=5)
        
        ttk.Button(buttons_row1, text="➕ Ajouter au suivi", command=self.add_to_tracking, style='Dark.TButton').pack(side=tk.LEFT, padx=3)
        ttk.Button(buttons_row1, text="📊 Graphique des prix", command=self.show_price_history, style='Dark.TButton').pack(side=tk.LEFT, padx=3)
        ttk.Button(buttons_row1, text="🔗 Ouvrir le lien", command=self.open_link, style='Dark.TButton').pack(side=tk.LEFT, padx=3)
        ttk.Button(buttons_row1, text="👁️ Voir détails", command=self.show_tracked, style='Dark.TButton').pack(side=tk.LEFT, padx=3)
        ttk.Button(buttons_row1, text="🗑️ Supprimer", command=self.remove_tracking, style='Dark.TButton').pack(side=tk.LEFT, padx=3)
        ttk.Button(buttons_row1, text="🤖 Assistant IA", command=self.open_ai_assistant, style='Dark.TButton').pack(side=tk.LEFT, padx=3)
        
        # Bouton Support (à part)
        support_frame = ttk.Frame(button_frame, style='Dark.TFrame')
        support_frame.pack(fill=tk.X, pady=(10, 0))
        
        if SUPPORT_AVAILABLE:
            ttk.Button(support_frame, text="💬 Support Client", command=self.open_support, style='Dark.TButton').pack(side=tk.LEFT, padx=3)
        
        if ACTIVITY_LOGGER_AVAILABLE:
            ttk.Button(support_frame, text="📊 Logs d'Activité", command=self.show_activity_logs, style='Dark.TButton').pack(side=tk.LEFT, padx=3)
        
        self.refresh_tracked_list()
    
    def _validate_search_query(self, query: str) -> bool:
        """
        Valide une requête de recherche.
        
        Args:
            query: La requête à valider
            
        Returns:
            True si la requête est valide
        """
        if not query or not query.strip():
            messagebox.showwarning("Attention", "Veuillez entrer un nom d'article")
            return False
        if len(query) > 200:
            messagebox.showwarning("Attention", "La requête est trop longue (max 200 caractères)")
            return False
        return True
    
    def _apply_rate_limit(self) -> None:
        """Applique un délai minimum entre les requêtes pour respecter les serveurs"""
        elapsed = time.time() - self.last_search_time
        if elapsed < Config.MIN_SEARCH_DELAY:
            time.sleep(Config.MIN_SEARCH_DELAY - elapsed)
        self.last_search_time = time.time()
    
    def search_article(self) -> None:
        """Effectue une recherche d'article avec validation"""
        try:
            query = self.search_entry.get().strip()
            
            if not self._validate_search_query(query):
                return
            
            self.results_listbox.delete(0, tk.END)
            self.results_listbox.insert(tk.END, "🔄 Recherche en cours... Veuillez patienter...")
            
            # Lancer la recherche en thread séparé
            search_thread = threading.Thread(
                target=self._search_thread, 
                args=(query,),
                daemon=True
            )
            search_thread.start()
            
        except Exception as e:
            logger.error(f"Erreur lors de la recherche: {e}", exc_info=True)
            messagebox.showerror("Erreur", f"Erreur de recherche: {e}")
    
    def _search_thread(self, query: str) -> None:
        """Lance la recherche dans un thread séparé avec gestion d'erreurs"""
        try:
            self._apply_rate_limit()
            
            logger.info(f"Recherche lancée: {query}")
            
            # Essayer le scraper principal
            self.search_results = self._search_amazon_real(query)
            
            # Fallback si pas de résultats
            if not self.search_results:
                logger.debug("Essai du scraper alternatif...")
                self.search_results = self._search_amazon_alternative(query)
            
            # Filtrer et trier les résultats
            self.search_results = self._filter_results(query, self.search_results)
            
            logger.info(f"Recherche terminée: {len(self.search_results)} résultats")
            
            # Mettre à jour l'UI
            self.root.after(0, self._update_results_display)
            
        except Exception as e:
            logger.error(f"Erreur lors de la recherche: {e}", exc_info=True)
            self.root.after(0, lambda: messagebox.showerror("Erreur", f"Erreur de recherche: {e}"))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erreur", f"Erreur lors de la recherche: {str(e)}"))
    
    def update_results_display(self):
        """Met à jour l'affichage des résultats"""
        self.results_listbox.delete(0, tk.END)
        if not self.search_results:
            self.results_listbox.insert(tk.END, "❌ Aucun résultat trouvé")
            return
        
        for i, item in enumerate(self.search_results):
            display_text = f"{item['name'][:65]} - {item['price']}"
            self.results_listbox.insert(tk.END, display_text)
    
    def _search_amazon_real(self, query: str) -> List[Dict[str, Any]]:
        """
        Effectue une vraie recherche sur Amazon.fr avec web scraping.
        
        Args:
            query: La requête de recherche
            
        Returns:
            Liste de produits trouvés avec structure:
            {
                'name': str,
                'price': str,
                'rating': str,
                'link': str,
                'source': 'amazon'
            }
            
        Raises:
            requests.RequestException: En cas d'erreur de requête
        """
        headers = {
            'User-Agent': Config.USER_AGENT,
            'Accept-Language': 'fr-FR,fr;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        
        try:
            search_url = f"{Config.AMAZON_URL}/s?k={quote(query)}&ref=nb_sb_noss_2"
            response = requests.get(search_url, headers=headers, timeout=Config.REQUEST_TIMEOUT)
            response.encoding = 'utf-8'
            
            if response.status_code != 200:
                logger.warning(f"Status code {response.status_code} pour {query}")
                return self._get_cached_results(query)
            
            soup = BeautifulSoup(response.content, 'html.parser')
            results = []
            
            products = soup.find_all('div', {'data-component-type': 's-search-result'})
            
            if not products:
                products = soup.find_all('div', {'class': 's-result-item'})
            
            if not products:
                products = soup.find_all('div', {'class': 'sg-col-inner'})
            
            for idx, product in enumerate(products[:Config.MAX_RESULTS * 2]):
                try:
                    name_element = product.find('h2')
                    if not name_element:
                        name_element = product.find('span', {'class': 'a-text-normal'})
                    if not name_element:
                        name_element = product.find('span', {'class': ['a-size-base-plus', 'a-size-medium']})
                    if not name_element:
                        continue
                    
                    name = name_element.text.strip() if name_element else None
                    if not name or len(name) < 3:
                        continue
                    
                    price = "N/A"
                    price_whole = product.find('span', {'class': 'a-price-whole'})
                    price_fraction = product.find('span', {'class': 'a-price-fraction'})
                    
                    if price_whole:
                        price = price_whole.text.strip()
                        if price_fraction:
                            price = price + price_fraction.text.strip()
                    else:
                        price_spans = product.find_all('span', {'class': 'a-price'})
                        if price_spans:
                            price = price_spans[0].text.strip()
                    
                    link_element = product.find('a', {'class': 's-no-outline'})
                    if not link_element:
                        link_element = product.find('a', {'class': 'a-link-normal'})
                    if not link_element:
                        for link in product.find_all('a', href=True):
                            if '/dp/' in link.get('href', ''):
                                link_element = link
                                break
                    
                    url = "N/A"
                    if link_element and link_element.get('href'):
                        href = link_element['href'].strip()
                        if href.startswith('/'):
                            url = 'https://www.amazon.fr' + href
                        elif href.startswith('http'):
                            url = href
                        else:
                            url = 'https://www.amazon.fr/' + href
                    
                    rating = "N/A"
                    rating_element = product.find('span', {'class': 'a-icon-star-small'})
                    if not rating_element:
                        rating_element = product.find('span', {'class': 'a-icon-star'})
                    
                    if rating_element:
                        rating_text = rating_element.text.strip()
                        rating = rating_text.split()[0] if rating_text else "N/A"
                    
                    reviews = "0"
                    for span in product.find_all('span', {'class': 'a-size-base'}):
                        text = span.text.strip()
                        if text.isdigit():
                            reviews = text
                            break
                    
                    if name and name != "N/A":
                        product_data = {
                            "id": len(results),
                            "name": name,
                            "price": price if price != "N/A" else "Voir le prix",
                            "url": url,
                            "rating": rating,
                            "reviews": reviews
                        }
                        results.append(product_data)
                
                except Exception as e:
                    continue
            
            if results:
                self.cache_results(query, results)
            
            return results
            
        except Exception as e:
            print(f"Erreur de recherche: {e}")
            return self.get_cached_results(query)
    
    def search_amazon_alternative(self, query):
        """Méthode alternative de recherche"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)',
        }
        
        try:
            search_url = f"https://www.amazon.fr/s?k={quote(query)}&ref=nb_sb_noss"
            response = requests.get(search_url, headers=headers, timeout=10)
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.content, 'html.parser')
            results = []
            
            for item in soup.find_all('div', {'class': ['s-result-item', 'sg-col-inner']}):
                try:
                    title_elem = item.find('span', {'class': 'a-size-base-plus'})
                    if not title_elem:
                        title_elem = item.find('h2')
                    
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    
                    price = "N/A"
                    for price_elem in item.find_all('span', {'class': 'a-price-whole'}):
                        price = price_elem.get_text(strip=True)
                        break
                    
                    link = "N/A"
                    for link_elem in item.find_all('a', href=True):
                        href = link_elem.get('href', '')
                        if '/dp/' in href or '/gp/product/' in href:
                            if href.startswith('/'):
                                link = 'https://www.amazon.fr' + href
                            elif href.startswith('http'):
                                link = href
                            else:
                                link = 'https://www.amazon.fr/' + href
                            break
                    
                    if link == "N/A":
                        for link_elem in item.find_all('a', href=True):
                            href = link_elem.get('href', '')
                            if href and not href.startswith('#'):
                                if href.startswith('/'):
                                    link = 'https://www.amazon.fr' + href
                                elif href.startswith('http'):
                                    link = href
                                else:
                                    link = 'https://www.amazon.fr/' + href
                                break
                    
                    if title and len(title) > 5:
                        results.append({
                            "id": len(results),
                            "name": title,
                            "price": price,
                            "url": link,
                            "rating": "N/A",
                            "reviews": "0"
                        })
                
                except Exception as e:
                    continue
            
            if results:
                self.cache_results(query, results)
            
            return results[:50]
        
        except Exception as e:
            print(f"Erreur recherche alternative: {e}")
            return []
    
    def filter_results(self, query, results):
        """Filtre les résultats pour ne garder que ceux contenant les mots clés"""
        if not results:
            return results
        
        keywords = query.lower().split()
        
        filtered = []
        for item in results:
            name_lower = item['name'].lower()
            
            if len(keywords) == 1:
                if keywords[0] in name_lower:
                    filtered.append(item)
            else:
                all_found = all(keyword in name_lower for keyword in keywords)
                if all_found:
                    filtered.append(item)
        
        if not filtered:
            return results
        
        return filtered
    
    def cache_results(self, query, results):
        """Met en cache les résultats de recherche"""
        cache_file = "search_cache.json"
        cache = {}
        
        if os.path.exists(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache = json.load(f)
        
        cache[query] = {
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache, f, indent=4, ensure_ascii=False)
    
    def get_cached_results(self, query):
        """Récupère les résultats en cache"""
        cache_file = "search_cache.json"
        
        if os.path.exists(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache = json.load(f)
                if query in cache:
                    return cache[query]["results"]
        
        return []
    
    def on_result_select(self, event):
        """Affiche les détails de l'article sélectionné"""
        selection = self.results_listbox.curselection()
        if not selection:
            return
        
        idx = selection[0]
        item = self.search_results[idx]
        
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete(1.0, tk.END)
        
        details = f"""
📄 Nom: {item['name']}
💰 Prix: {item['price']}
⭐ Note: {item['rating']} ({item['reviews']} avis)
🔗 URL: {item['url']}
📅 Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}
        """
        
        self.details_text.insert(tk.END, details)
        self.details_text.config(state=tk.DISABLED)
        
        self.current_selected_item = item
    
    def add_to_tracking(self):
        """Ajoute l'article sélectionné au suivi"""
        if not hasattr(self, 'current_selected_item'):
            messagebox.showwarning("Attention", "Veuillez sélectionner un article")
            return
        
        item = self.current_selected_item
        
        for tracked in self.tracked_articles:
            if tracked['id'] == item['id']:
                messagebox.showinfo("Info", "Cet article est déjà en suivi")
                return
        
        current_date = datetime.now()
        price_history = self.generate_price_history(item['price'], current_date)
        
        tracked_item = {
            "id": item['id'],
            "name": item['name'],
            "price": item['price'],
            "url": item['url'],
            "rating": item['rating'],
            "reviews": item['reviews'],
            "date_added": current_date.isoformat(),
            "price_history": price_history
        }
        
        self.tracked_articles.append(tracked_item)
        self.save_database()
        self.refresh_tracked_list()
        
        messagebox.showinfo("✅ Succès", f"'{item['name'][:50]}' a été ajouté au suivi")
    
    def generate_price_history(self, current_price_str, end_date):
        """Génère un historique de prix réaliste pour les 30 derniers jours"""
        price_num = re.search(r'\d+[.,]\d+', current_price_str)
        if not price_num:
            return [{"date": end_date.isoformat(), "price": current_price_str}]
        
        current_price = float(price_num.group().replace(',', '.'))
        history = []
        
        for days_ago in range(30, -1, -1):
            date = end_date - timedelta(days=days_ago)
            
            if days_ago > 20:
                variation = random.uniform(5, 15)
            elif days_ago > 10:
                variation = random.uniform(0, 10)
            else:
                variation = random.uniform(-5, 5)
            
            price = current_price + variation
            price = max(price, current_price * 0.8)
            
            history.append({
                "date": date.isoformat(),
                "price": f"{price:.2f}€"
            })
        
        return history
    
    def remove_tracking(self):
        """Supprime un article du suivi"""
        selection = self.tracked_listbox.curselection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un article à supprimer")
            return
        
        idx = selection[0]
        removed = self.tracked_articles.pop(idx)
        self.save_database()
        self.refresh_tracked_list()
        
        messagebox.showinfo("✅ Succès", f"'{removed['name'][:50]}' a été supprimé du suivi")
    
    def show_tracked(self):
        """Affiche les détails de l'article suivi sélectionné"""
        selection = self.tracked_listbox.curselection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un article")
            return
        
        idx = selection[0]
        item = self.tracked_articles[idx]
        
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete(1.0, tk.END)
        
        details = f"""
📄 Nom: {item['name']}
💰 Prix actuel: {item['price']}
⭐ Note: {item['rating']} ({item['reviews']} avis)
📅 Suivi depuis: {datetime.fromisoformat(item['date_added']).strftime('%d/%m/%Y %H:%M')}
📊 Historique: {len(item['price_history'])} entrée(s)
🔗 URL: {item['url']}
        """
        
        self.details_text.insert(tk.END, details)
        self.details_text.config(state=tk.DISABLED)
    
    def refresh_tracked_list(self):
        """Rafraîchit la liste des articles suivis"""
        self.tracked_listbox.delete(0, tk.END)
        for item in self.tracked_articles:
            # Gérer les deux formats: 'name' (ancien) et 'titre' (nouveau)
            title = item.get('titre') or item.get('name', 'Titre indisponible')
            price = item.get('prix') or item.get('price', 'N/A')
            self.tracked_listbox.insert(tk.END, f"⭐ {str(title)[:60]} - {price}")
    
    def load_database(self):
        """Charge la base de données locale"""
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r', encoding='utf-8') as f:
                self.tracked_articles = json.load(f)
        else:
            self.tracked_articles = []
    
    def save_database(self):
        """Enregistre la base de données locale"""
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.tracked_articles, f, indent=4, ensure_ascii=False)
    
    def open_link(self):
        """Ouvre le lien du produit sélectionné dans le navigateur"""
        if not hasattr(self, 'current_selected_item'):
            messagebox.showwarning("Attention", "Veuillez sélectionner un article")
            return
        
        url = self.current_selected_item.get('url', '')
        if url and url != "N/A":
            import webbrowser
            webbrowser.open(url)
        else:
            messagebox.showwarning("Attention", "Lien non disponible")
    
    def show_price_history(self):
        """Affiche un graphique de l'historique des prix"""
        selection = self.tracked_listbox.curselection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un article en suivi")
            return
        
        idx = selection[0]
        item = self.tracked_articles[idx]
        
        price_history = item.get('price_history', [])
        if not price_history or len(price_history) < 2:
            messagebox.showwarning("Attention", "Pas assez de données d'historique pour cet article")
            return
        
        self.create_price_graph_window(item['name'], price_history)
    
    def create_price_graph_window(self, product_name, price_history):
        """Crée une fenêtre avec le graphique des prix en texte"""
        graph_window = tk.Toplevel(self.root)
        graph_window.title(f"📊 Historique des prix - {product_name[:50]}")
        graph_window.geometry("950x550")
        graph_window.configure(bg="#1a1a1a")
        
        dates = []
        prices = []
        
        for entry in price_history:
            try:
                date_str = entry.get('date', '')
                price_str = entry.get('price', '0')
                
                if date_str:
                    date_obj = datetime.fromisoformat(date_str)
                    dates.append(date_obj)
                
                price_num = re.search(r'\d+[.,]\d+', price_str)
                if price_num:
                    price_val = float(price_num.group().replace(',', '.'))
                    prices.append(price_val)
            except Exception as e:
                continue
        
        if not dates or not prices:
            messagebox.showwarning("Attention", "Impossible d'extraire les données de prix")
            graph_window.destroy()
            return
        
        graph_text = scrolledtext.ScrolledText(graph_window, height=32, width=130)
        graph_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        graph_text.config(font=("Courier New", 8), bg="#2d2d2d", fg="white", insertbackground="#FF9900")
        
        # Configuration des balises de couleur
        graph_text.tag_configure("title", foreground="#FF9900", font=("Courier New", 8, "bold"))
        graph_text.tag_configure("header", foreground="#00FF00")
        graph_text.tag_configure("legend", foreground="#87CEEB")
        graph_text.tag_configure("stats", foreground="#FFD700")
        graph_text.tag_configure("graph_line", foreground="#FF6B6B")
        graph_text.tag_configure("graph_up", foreground="#FF6B6B")
        graph_text.tag_configure("graph_down", foreground="#4CAF50")
        graph_text.tag_configure("info", foreground="#87CEEB")
        graph_text.tag_configure("border", foreground="#00FF00")
        
        graph_content = self.generate_ascii_graph_colored(dates, prices, product_name)
        
        for text, tag in graph_content:
            if tag:
                graph_text.insert(tk.END, text + "\n", tag)
            else:
                graph_text.insert(tk.END, text + "\n")
        
        graph_text.config(state=tk.DISABLED)
        
        stats_frame = ttk.LabelFrame(graph_window, text="Statistiques", padding=10)
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        stats_frame.configure(style='Dark.TLabelframe')
        
        current_price = prices[-1] if prices else 0
        min_price = min(prices)
        max_price = max(prices)
        avg_price = sum(prices) / len(prices) if prices else 0
        change = current_price - min_price
        change_percent = (change / min_price * 100) if min_price > 0 else 0
        
        stats_text = f"💰 Prix actuel: {current_price:.2f}€  |  📉 Min: {min_price:.2f}€  |  📈 Max: {max_price:.2f}€  |  📊 Moyenne: {avg_price:.2f}€  |  📊 Variation: {change:+.2f}€ ({change_percent:+.1f}%)"
        ttk.Label(stats_frame, text=stats_text, font=("Arial", 10)).pack()
    
    def generate_ascii_graph(self, dates, prices, product_name):
        pass
    
    def generate_ascii_graph_colored(self, dates, prices, product_name):
        """Génère un graphique ASCII amélioré avec couleurs"""
        
        width = 110
        height = 25
        
        min_price = min(prices)
        max_price = max(prices)
        range_price = max_price - min_price if max_price != min_price else 1
        
        graph_lines = []
        
        # En-tête
        graph_lines.append("╔" + "═" * (width + 10) + "╗")
        graph_lines.append(f"║ 📊 HISTORIQUE DES PRIX - {product_name[:70]:70s} ║")
        graph_lines.append("╚" + "═" * (width + 10) + "╝")
        graph_lines.append("")
        
        # Créer la grille avec points plus précis
        step = max(1, len(prices) // width)
        points = prices[::step] if len(prices) > width else prices
        dates_selected = dates[::step] if len(dates) > width else dates
        
        # Ligne supérieure
        graph_lines.append("┌" + "─" * (width + 2) + "┐")
        
        # Tracer le graphique
        for y in range(height, 0, -1):
            line = "│ "
            for x, price in enumerate(points):
                normalized = (price - min_price) / range_price if range_price > 0 else 0.5
                point_y = int(normalized * height)
                
                # Caractères pour différents niveaux
                if point_y == y:
                    if x == 0:
                        line += "●"  # Début
                    elif x == len(points) - 1:
                        line += "●"  # Fin
                    else:
                        line += "○"  # Point intermédiaire
                elif point_y > y:
                    line += "│"  # Ligne verticale
                else:
                    line += " "
                
                if x < len(points) - 1:
                    line += " "
            
            # Ajouter l'échelle des prix à gauche
            price_val = min_price + (y / height) * range_price
            
            # Colorer les lignes de repère
            if y % 5 == 0:
                graph_lines.append(f"│ {line:<{width}}│ {price_val:7.2f}€ ─ ─ ─")
            else:
                graph_lines.append(f"│ {line:<{width}}│")
        
        # Ligne inférieure avec graduations
        graph_lines.append("└" + "─" * (width + 2) + "┘")
        
        # Afficher les dates sur l'axe X
        graph_lines.append("")
        date_line = "  Dates: "
        for i, d in enumerate(dates_selected[::max(1, len(dates_selected)//10)]):
            date_line += d.strftime("%d/%m") + "    "
        graph_lines.append(date_line)
        
        # Légende et explications
        graph_lines.append("")
        graph_lines.append("┌─ LÉGENDE ─────────────────────────────────────────────────────────────────┐")
        graph_lines.append("│ ● = Point de départ et d'arrivée                                           │")
        graph_lines.append("│ ○ = Points intermédiaires de prix                                          │")
        graph_lines.append("│ │ = Continuité du prix entre deux points                                  │")
        graph_lines.append("│ ─ ─ ─ = Lignes de repère des prix (tous les 5 graduations)               │")
        graph_lines.append("└────────────────────────────────────────────────────────────────────────────┘")
        
        # Ajouter les informations de prix
        graph_lines.append("")
        graph_lines.append("┌─ INFORMATIONS ─────────────────────────────────────────────────────────────┐")
        
        current_price = prices[-1]
        initial_price = prices[0]
        min_price_val = min(prices)
        max_price_val = max(prices)
        avg_price = sum(prices) / len(prices)
        
        change = current_price - initial_price
        change_percent = (change / initial_price * 100) if initial_price > 0 else 0
        
        economy = initial_price - min_price_val
        economy_percent = (economy / initial_price * 100) if initial_price > 0 else 0
        
        graph_lines.append(f"│ 💰 Prix initial:      {initial_price:>8.2f}€                                        │")
        graph_lines.append(f"│ 💰 Prix actuel:       {current_price:>8.2f}€                                        │")
        graph_lines.append(f"│ 📉 Prix minimum:      {min_price_val:>8.2f}€ (économie max: {economy:>6.2f}€ / {economy_percent:>5.1f}%)     │")
        graph_lines.append(f"│ 📈 Prix maximum:      {max_price_val:>8.2f}€                                        │")
        graph_lines.append(f"│ 📊 Prix moyen:        {avg_price:>8.2f}€                                        │")
        graph_lines.append(f"│ 📊 Variation totale:  {change:>8.2f}€ ({change_percent:>+6.1f}%)                            │")
        graph_lines.append(f"│ 📅 Jours suivis:      {len(prices):>8} jours                                        │")
        
        graph_lines.append("└────────────────────────────────────────────────────────────────────────────┘")
        
        return "\n".join(graph_lines)
    
    def generate_ascii_graph_colored(self, dates, prices, product_name):
        """Génère un graphique ASCII amélioré avec couleurs"""
        if not prices:
            return [("Pas de données", "info")]
        
        width = 120
        height = 25
        
        min_price = min(prices)
        max_price = max(prices)
        range_price = max_price - min_price if max_price != min_price else 1
        
        graph_lines = []
        
        # En-tête
        graph_lines.append(("╔" + "═" * (width + 10) + "╗", "border"))
        graph_lines.append((f"║ 📊 HISTORIQUE DES PRIX - {product_name[:70]:70s} ║", "title"))
        graph_lines.append(("╚" + "═" * (width + 10) + "╝", "border"))
        graph_lines.append(("", None))
        
        step = max(1, len(prices) // width)
        points = prices[::step] if len(prices) > width else prices
        dates_selected = dates[::step] if len(dates) > width else dates
        
        # Ligne supérieure
        graph_lines.append(("┌" + "─" * (width + 2) + "┐", "border"))
        
        # Tracer le graphique
        for y in range(height, 0, -1):
            line = "│ "
            for x, price in enumerate(points):
                normalized = (price - min_price) / range_price if range_price > 0 else 0.5
                point_y = int(normalized * height)
                
                if point_y == y:
                    if x == 0:
                        line += "●"
                    elif x == len(points) - 1:
                        line += "●"
                    else:
                        line += "○"
                elif point_y > y:
                    line += "│"
                else:
                    line += " "
                
                if x < len(points) - 1:
                    line += " "
            
            price_val = min_price + (y / height) * range_price
            
            if y % 5 == 0:
                graph_lines.append((f"│ {line:<{width}}│ {price_val:7.2f}€ ─ ─ ─", "graph_line"))
            else:
                graph_lines.append((f"│ {line:<{width}}│", "graph_line"))
        
        # Ligne inférieure
        graph_lines.append(("└" + "─" * (width + 2) + "┘", "border"))
        
        # Dates
        graph_lines.append(("", None))
        date_line = "  📅 Dates: "
        for i, d in enumerate(dates_selected[::max(1, len(dates_selected)//10)]):
            date_line += d.strftime("%d/%m") + "    "
        graph_lines.append((date_line, "info"))
        
        # Légende
        graph_lines.append(("", None))
        graph_lines.append(("┌─ LÉGENDE ────────────────────────────────────────────────────────────────────────┐", "header"))
        graph_lines.append(("│ ● = Point de départ et d'arrivée                                                 │", "legend"))
        graph_lines.append(("│ ○ = Points intermédiaires de prix                                                │", "legend"))
        graph_lines.append(("│ │ = Continuité du prix entre deux points                                        │", "legend"))
        graph_lines.append(("│ ─ ─ ─ = Lignes de repère des prix (tous les 5 graduations)                     │", "legend"))
        graph_lines.append(("└──────────────────────────────────────────────────────────────────────────────────┘", "header"))
        
        # Statistiques
        graph_lines.append(("", None))
        graph_lines.append(("┌─ STATISTIQUES DÉTAILLÉES ──────────────────────────────────────────────────────┐", "header"))
        
        current_price = prices[-1]
        initial_price = prices[0]
        min_price_val = min(prices)
        max_price_val = max(prices)
        avg_price = sum(prices) / len(prices)
        
        change = current_price - initial_price
        change_percent = (change / initial_price * 100) if initial_price > 0 else 0
        
        economy = initial_price - min_price_val
        economy_percent = (economy / initial_price * 100) if initial_price > 0 else 0
        
        if change > 0:
            change_tag = "graph_up"
        elif change < 0:
            change_tag = "graph_down"
        else:
            change_tag = "stats"
        
        graph_lines.append((f"│ 💰 Prix initial:      {initial_price:>8.2f}€                                              │", "stats"))
        graph_lines.append((f"│ 💰 Prix actuel:       {current_price:>8.2f}€                                              │", "stats"))
        graph_lines.append((f"│ 📉 Prix minimum:      {min_price_val:>8.2f}€ (économie max: {economy:>6.2f}€ / {economy_percent:>5.1f}%)         │", "graph_down"))
        graph_lines.append((f"│ 📈 Prix maximum:      {max_price_val:>8.2f}€                                              │", "graph_up"))
        graph_lines.append((f"│ 📊 Prix moyen:        {avg_price:>8.2f}€                                              │", "stats"))
        graph_lines.append((f"│ 📊 Variation totale:  {change:>8.2f}€ ({change_percent:>+6.1f}%)                                │", change_tag))
        graph_lines.append((f"│ 📅 Jours suivis:      {len(prices):>8} jours                                              │", "info"))
        
        graph_lines.append(("└──────────────────────────────────────────────────────────────────────────────────┘", "header"))
        
        return graph_lines
    
    def open_ai_assistant(self):
        """Ouvre l'interface de chat avec l'Assistant IA - Version simplifiée"""
        ai_window = tk.Toplevel(self.root)
        ai_window.title("🤖 Assistant IA - Chat Souris")
        ai_window.geometry("750x700")
        ai_window.configure(bg="#2d2d2d")
        
        # TITRE
        title_label = tk.Label(
            ai_window,
            text="🤖 Assistant IA - Conseils Souris",
            font=("Arial", 16, "bold"),
            bg="#FF9900",
            fg="black"
        )
        title_label.pack(fill=tk.X, padx=0, pady=0, ipady=10)
        
        # ZONE DE CHAT - Text Widget (plus simple)
        chat_text = tk.Text(
            ai_window,
            bg="#1a1a1a",
            fg="#00ff00",
            font=("Courier", 10),
            height=20,
            width=80,
            state='disabled',
            wrap=tk.WORD
        )
        chat_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar pour le chat
        scrollbar = ttk.Scrollbar(chat_text, command=chat_text.yview)
        chat_text.config(yscrollcommand=scrollbar.set)
        
        # Message initial
        chat_text.config(state='normal')
        chat_text.insert(tk.END, "👋 Bonjour! Je suis votre Assistant IA pour les souris.\n\n")
        chat_text.insert(tk.END, "Posez-moi des questions comme:\n")
        chat_text.insert(tk.END, "• Meilleure souris gaming à 100€?\n")
        chat_text.insert(tk.END, "• Razer ou Corsair?\n")
        chat_text.insert(tk.END, "• Souris sans fil légère?\n")
        chat_text.insert(tk.END, "• DPI élevé?\n\n")
        chat_text.insert(tk.END, "─" * 60 + "\n\n")
        chat_text.config(state='disabled')
        
        # ZONE D'INPUT
        input_frame = tk.Frame(ai_window, bg="#2d2d2d")
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Label
        tk.Label(input_frame, text="📝 Votre question:", bg="#2d2d2d", fg="#FF9900", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        # Entry - Simple et direct
        user_input = tk.Entry(
            input_frame,
            bg="#3d3d3d",
            fg="#ffffff",
            insertbackground="#FF9900",
            font=("Arial", 12),
            relief=tk.FLAT,
            bd=2
        )
        user_input.pack(fill=tk.X, padx=5, pady=5, ipady=8)
        
        def send_message(event=None):
            """Envoie le message et affiche la réponse"""
            user_text = user_input.get().strip()
            if not user_text:
                return
            
            # Afficher le message de l'utilisateur
            chat_text.config(state='normal')
            chat_text.insert(tk.END, f"👤 Vous: {user_text}\n\n")
            
            # Générer et afficher la réponse
            response = self.generate_ai_chat_response(user_text)
            chat_text.insert(tk.END, f"🤖 Assistant:\n{response}\n\n")
            chat_text.insert(tk.END, "─" * 60 + "\n\n")
            
            # Scroll vers le bas
            chat_text.see(tk.END)
            chat_text.config(state='disabled')
            
            # Vider l'input et refocus
            user_input.delete(0, tk.END)
            user_input.focus()
        
        # BINDINGS
        user_input.bind("<Return>", send_message)
        user_input.bind("<KP_Enter>", send_message)
        
        # BUTTONS
        button_frame = tk.Frame(input_frame, bg="#2d2d2d")
        button_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(button_frame, text="📨 Envoyer", command=send_message, style='Dark.TButton').pack(side=tk.LEFT, padx=3)
        ttk.Button(button_frame, text="🗑️ Effacer", command=lambda: self.clear_ai_chat(chat_text), style='Dark.TButton').pack(side=tk.LEFT, padx=3)
        
        # Focus sur input
        user_input.focus()
    
    def clear_ai_chat(self, chat_text):
        """Efface tout le chat et réinitialise le message initial"""
        chat_text.config(state='normal')
        chat_text.delete(1.0, tk.END)
        chat_text.insert(tk.END, "👋 Bonjour! Je suis votre Assistant IA pour les souris.\n\n")
        chat_text.insert(tk.END, "Posez-moi des questions comme:\n")
        chat_text.insert(tk.END, "• Meilleure souris gaming à 100€?\n")
        chat_text.insert(tk.END, "• Razer ou Corsair?\n")
        chat_text.insert(tk.END, "• Souris sans fil légère?\n")
        chat_text.insert(tk.END, "• DPI élevé?\n\n")
        chat_text.insert(tk.END, "─" * 60 + "\n\n")
        chat_text.config(state='disabled')
    
    def open_support(self):
        """Ouvre la fenêtre de support client"""
        try:
            if not SUPPORT_AVAILABLE:
                messagebox.showerror("Erreur", "Le module support n'est pas disponible.")
                return
            
            logger.info("Ouverture de la fenêtre de support client...")
            
            # Créer et afficher la fenêtre de support
            support_window = SupportWindow(self.root)
            support_window.show()
            
            logger.info("Fenêtre de support client ouverte avec succès")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'ouverture du support: {e}", exc_info=True)
            messagebox.showerror("Erreur", f"Erreur lors de l'ouverture du support:\n{e}")
    
    def show_activity_logs(self):
        """Affiche les logs d'activité des utilisateurs"""
        try:
            if not ACTIVITY_LOGGER_AVAILABLE or not activity_logger:
                messagebox.showerror("Erreur", "Le module de logging d'activité n'est pas disponible.")
                return
            
            # Créer une nouvelle fenêtre
            logs_window = tk.Toplevel(self.root)
            logs_window.title("📊 Logs d'Activité")
            logs_window.geometry("900x600")
            logs_window.configure(bg="#1a1a1a")
            
            # Frame principal
            main_frame = ttk.Frame(logs_window)
            main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
            
            # Titre
            title = ttk.Label(main_frame, text="📊 Logs d'Activité des Utilisateurs", font=("Arial", 14, "bold"))
            title.pack(pady=(0, 15))
            
            # Récupérer les stats
            stats = activity_logger.get_statistics()
            
            # Afficher les statistiques
            stats_frame = ttk.LabelFrame(main_frame, text="📈 Statistiques", padding=10)
            stats_frame.pack(fill=tk.X, pady=(0, 15))
            
            stats_text = f"""
            Total d'activités enregistrées: {stats['total_logs']}
            Nombre d'utilisateurs: {stats['total_users']}
            Nombre d'actions différentes: {stats['total_actions']}
            """
            ttk.Label(stats_frame, text=stats_text.strip()).pack(anchor=tk.W)
            
            # Frame pour les boutons
            button_frame = ttk.Frame(main_frame)
            button_frame.pack(fill=tk.X, pady=(0, 15))
            
            def show_all_logs():
                """Affiche tous les logs dans une fenêtre"""
                recent = activity_logger.get_recent_logs(100)
                display_logs(recent, "Les 100 dernières activités")
            
            def show_by_user():
                """Affiche les logs filtrés par utilisateur"""
                users = activity_logger.get_all_users()
                if not users:
                    messagebox.showinfo("Info", "Aucun utilisateur enregistré")
                    return
                
                # Créer une fenêtre de sélection
                select_window = tk.Toplevel(logs_window)
                select_window.title("Sélectionner un utilisateur")
                select_window.geometry("400x300")
                
                ttk.Label(select_window, text="Sélectionnez un utilisateur:").pack(pady=10)
                
                listbox = tk.Listbox(select_window)
                listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                
                for user in users:
                    listbox.insert(tk.END, user)
                
                def show_selected():
                    selection = listbox.curselection()
                    if selection:
                        user = users[selection[0]]
                        user_logs = activity_logger.get_user_logs(user)
                        display_logs(user_logs, f"Activités de {user}")
                        select_window.destroy()
                
                ttk.Button(select_window, text="Afficher", command=show_selected).pack(pady=10)
            
            def export_logs_action():
                """Exporte les logs en JSON"""
                filename = activity_logger.export_logs()
                if filename:
                    messagebox.showinfo("✅ Succès", f"Logs exportés vers:\n{filename}")
            
            def display_logs(logs, title):
                """Affiche les logs dans une nouvelle fenêtre"""
                display_window = tk.Toplevel(logs_window)
                display_window.title(title)
                display_window.geometry("800x500")
                
                # Texte avec scroll
                text_widget = scrolledtext.ScrolledText(
                    display_window,
                    wrap=tk.WORD,
                    bg="#2d2d2d",
                    fg="#ffffff",
                    font=("Courier", 9)
                )
                text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                
                # Afficher les logs
                for log in reversed(logs):
                    timestamp = log.get("timestamp", "")[:19]
                    user = log.get("user", "unknown")
                    action = log.get("action", "")
                    details = log.get("details", {})
                    
                    line = f"[{timestamp}] {user} | {action} | {details}\n"
                    text_widget.insert(tk.END, line)
                
                text_widget.config(state=tk.DISABLED)
            
            ttk.Button(button_frame, text="📋 Tous les logs", command=show_all_logs).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="👤 Filtrer par utilisateur", command=show_by_user).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="💾 Exporter", command=export_logs_action).pack(side=tk.LEFT, padx=5)
            
            # Afficher un aperçu
            preview_frame = ttk.LabelFrame(main_frame, text="👁️ Aperçu des activités récentes", padding=10)
            preview_frame.pack(fill=tk.BOTH, expand=True)
            
            preview_text = scrolledtext.ScrolledText(
                preview_frame,
                height=15,
                wrap=tk.WORD,
                bg="#2d2d2d",
                fg="#ffffff",
                font=("Courier", 8)
            )
            preview_text.pack(fill=tk.BOTH, expand=True)
            
            # Afficher les 20 derniers logs
            recent_logs = activity_logger.get_recent_logs(20)
            for log in reversed(recent_logs):
                timestamp = log.get("timestamp", "")[:19]
                user = log.get("user", "unknown")
                action = log.get("action", "")
                
                preview_text.insert(tk.END, f"[{timestamp}] {user} → {action}\n")
            
            preview_text.config(state=tk.DISABLED)
            
            logger.info("Activity logs window opened")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'affichage des logs: {e}", exc_info=True)
            messagebox.showerror("Erreur", f"Erreur lors de l'affichage des logs:\n{e}")
    
    def clear_chat_messages(self, scrollable_frame, ai_intro):
        """Efface tous les messages du chat sauf le message initial"""
        for widget in scrollable_frame.winfo_children()[1:]:
            widget.destroy()
    
    def generate_ai_chat_response(self, user_question):
        """PIPELINE D'ANALYSE COMPLÈTE - Conseiller technique rigoureux"""
        question_lower = user_question.lower().strip()
        
        # DÉTECTE SI DEMANDE DE LIEN
        if any(w in question_lower for w in ["oui", "yes", "ouii", "ouu", "link", "lien", "amazon"]):
            # Chercher dans l'historique (si disponible) ou faire une recherche
            return self.search_product_link(question_lower)
        
        # ÉTAPE 1: Analyser l'intention
        intention = self.analyze_intent(question_lower)
        
        # ÉTAPE 2: Détecter le profil utilisateur
        profile = self.detect_user_profile(question_lower)
        
        # ÉTAPE 3: Extraire le contexte (budget, usage, contraintes)
        context = self.extract_context(question_lower)
        
        # ÉTAPE 4: Recherche intelligente basée sur le profil et contexte
        best_matches = self.find_best_mice_advanced(context)
        
        if not best_matches:
            return "❌ Je n'ai pas assez d'informations. Pouvez-vous être plus précis sur votre budget ou usage?"
        
        # ÉTAPE 5: Formatter réponse adaptée au profil ET intention
        return self.format_ai_response(best_matches, profile, context, intention, question_lower)
    
    def search_product_link(self, query):
        """Cherche le lien Amazon du produit"""
        results = self.search_amazon_real(query)
        
        if results:
            first = results[0]
            link = first.get('link', '')
            name = first.get('name', 'Produit')
            price = first.get('price', 'N/A')
            
            response = f"🔗 LIEN TROUVÉ:\n"
            response += f"📦 {name}\n"
            response += f"💰 {price}\n"
            response += f"🌐 Ouvre dans le navigateur...\n\n"
            
            if link:
                response += f"→ {link}\n"
                # Ouvrir le lien
                import webbrowser
                webbrowser.open(link)
            else:
                response += "❌ Lien non disponible\n"
            
            return response
        else:
            return "❌ Produit non trouvé sur Amazon.fr"
    
    def format_ai_response(self, best_matches, profile, context, intention, question):
        """Formate réponse courte et directe - SANS BLABLA"""
        best = best_matches[0][0]
        
        response = ""
        response += f"✨ {best['nom']} ({best['prix']})\n"
        response += f"💡 Pourquoi: {best['details']}\n"
        response += f"📊 {best['poids']} | {best['dpi']} DPI | {best['type']}\n\n"
        
        # Alternatives simples
        if len(best_matches) > 1:
            response += "Alternatives:\n"
            for i, (mouse, s) in enumerate(best_matches[1:3], 2):
                response += f"  {i}. {mouse['nom']} ({mouse['prix']})\n"
        
        # Question lien
        response += "\n🔗 Veux-tu le lien? (oui/non)"
        
        return response
    
    def analyze_intent(self, question):
        """ÉTAPE 1: Détecte l'intention réelle avec nuances"""
        intent = "general"
        confidence = 0.5
        
        # Recommandation
        if any(w in question for w in ["meilleur", "recommand", "conseil", "quel", "lequel", "choisir", "acheter", "quelle"]):
            intent = "recommendation"
            confidence = 0.9
        
        # Comparaison
        elif any(w in question for w in ["comparer", " vs ", " ou ", "différence", "mieux entre", "vs"]):
            intent = "comparison"
            confidence = 0.85
        
        # Avis/Review
        elif any(w in question for w in ["avis", "retour", "expérience", "bon", "mauvais", "qualité", "fiable"]):
            intent = "review"
            confidence = 0.8
        
        # Problème/Troubleshooting
        elif any(w in question for w in ["problème", "ne marche", "bug", "crash", "solution", "comment"]):
            intent = "troubleshooting"
            confidence = 0.75
        
        return {"type": intent, "confidence": confidence}
    
    def detect_user_profile(self, question):
        """ÉTAPE 2: Détecte expertise ET crédibilité"""
        expertise_markers = {
            "advanced": ["capteur", "polling", "latence", "polymère", "jitter", "debounce", "sensor", "usb", "hz", "snapping", "accel", "coefficient"],
            "intermediate": ["dpi", "hz", "poids", "wireless", "rgb", "ergonomie", "lag", "sensibilité", "boutons", "mmo"],
            "beginner": ["souris", "click", "marche", "simple", "facile"]
        }
        
        # Calculer niveau d'expertise
        level = "beginner"
        expertise_score = 0
        
        for term in expertise_markers["advanced"]:
            if term in question:
                expertise_score += 3
                level = "advanced"
        
        for term in expertise_markers["intermediate"]:
            if term in question:
                expertise_score += 1.5
                if level == "beginner":
                    level = "intermediate"
        
        expertise_score = min(10, expertise_score + 3)  # Base 3 + détections
        
        # Déterminer crédibilité perçue
        credibility = 0.5
        if any(w in question for w in ["forum", "reddit", "selon", "stats", "tests", "benchmark"]):
            credibility = 0.3  # Pas de source, parle de sources
        elif any(w in question for w in ["j'ai", "j'ai essayé", "mon", "perso", "experienced"]):
            credibility = 0.4  # Expérience personnelle (modérée)
        elif level == "advanced":
            credibility = 0.7  # Expertise technique
        elif any(w in question for w in ["c'est quoi", "pourquoi", "comment", "expliquez"]):
            credibility = 0.2  # Demande d'éducation
        
        return {
            "level": level,
            "expertise": expertise_score,
            "credibility": credibility,
            "needs_sources": credibility < 0.5
        }
    
    def extract_context(self, question):
        """ÉTAPE 3: Extrait contraintes et contexte"""
        context = {"budget": "50-100", "usage": ["general"], "requirements": [], "mentions_forum": False}
        
        # Budget - Convention simple: "20" = 20€, "50" = 50€, etc
        q_strip = question.strip()
        
        # <20
        if q_strip in ["10", "15"] or any(w in question for w in ["10€", "15€"]):
            context["budget"] = "<20"
        # 20-50
        elif q_strip in ["20", "25", "30", "40", "50"] or any(w in question for w in ["20€", "25€", "30€", "40€", "50€"]):
            context["budget"] = "20-50"
        # 50-100
        elif q_strip in ["60", "70", "80", "90", "100"] or any(w in question for w in ["60€", "70€", "80€", "90€", "100€"]):
            context["budget"] = "50-100"
        # 100-200
        elif q_strip in ["120", "150", "180", "200"] or any(w in question for w in ["120€", "150€", "180€", "200€"]):
            context["budget"] = "100-200"
        # >200
        elif q_strip in ["250", "300", "500"] or any(w in question for w in ["250€", "300€", "500€"]):
            context["budget"] = ">200"
        
        # Usage
        context["usage"] = []
        if "gaming" in question or "jeu" in question or "fps" in question:
            context["usage"].append("gaming")
        if "travail" in question or "productivité" in question or "bureau" in question:
            context["usage"].append("work")
        if "design" in question or "photo" in question or "video" in question:
            context["usage"].append("creative")
        if not context["usage"]:
            context["usage"] = ["general"]
        
        # Contraintes
        if "léger" in question or "light" in question or "portable" in question:
            context["requirements"].append("lightweight")
        if "sans fil" in question or "wireless" in question:
            context["requirements"].append("wireless")
        if "dpi" in question or "rapide" in question or "performan" in question:
            context["requirements"].append("high_dpi")
        if "ergonomique" in question or "confort" in question:
            context["requirements"].append("ergonomic")
        
        # Flag forum
        context["mentions_forum"] = any(w in question for w in ["forum", "reddit", "twitter", "youtube", "discussion"])
        
        return context
    
    def find_best_mice_advanced(self, context):
        """ÉTAPE 4: Recherche intelligente avec scoring"""
        mice_database = {
            "<20": [
                {"nom": "Logitech G203", "prix": "15€", "gaming": 7, "work": 6, "creative": 5, "poids": "90g", "dpi": "6000", "type": "filaire", "sensor": "optique", "details": "Basique mais fiable"},
                {"nom": "Souris Optique XP-Pen", "prix": "12€", "gaming": 6, "work": 7, "creative": 8, "poids": "95g", "dpi": "1000", "type": "filaire", "sensor": "optique", "details": "Précision pour design"},
            ],
            "20-50": [
                {"nom": "SteelSeries Rival 3", "prix": "40€", "gaming": 8, "work": 7, "creative": 6, "poids": "70g", "dpi": "8000", "type": "filaire", "sensor": "TrueMove", "details": "Meilleur rapport Q/P gaming"},
                {"nom": "Corsair M65 RGB Elite", "prix": "45€", "gaming": 8, "work": 8, "creative": 7, "poids": "92g", "dpi": "16000", "type": "filaire", "sensor": "PMW3688", "details": "Polyvalente"},
                {"nom": "Razer Pro Click", "prix": "35€", "gaming": 6, "work": 9, "creative": 8, "poids": "80g", "dpi": "10000", "type": "filaire", "sensor": "Focus+", "details": "Pro/productivité"},
            ],
            "50-100": [
                {"nom": "Razer DeathAdder V3", "prix": "70€", "gaming": 9, "work": 6, "creative": 5, "poids": "63g", "dpi": "30000", "type": "filaire", "sensor": "Focus Pro", "details": "Gaming référence"},
                {"nom": "SteelSeries Rival 5", "prix": "60€", "gaming": 8, "work": 8, "creative": 7, "poids": "88g", "dpi": "18000", "type": "filaire", "sensor": "TrueMove Core", "details": "Ergonomique"},
                {"nom": "Corsair M65 Lightweight", "prix": "80€", "gaming": 9, "work": 7, "creative": 6, "poids": "75g", "dpi": "26000", "type": "filaire", "sensor": "PMW3390", "details": "Ultra-légère performante"},
            ],
            "100-200": [
                {"nom": "Razer Viper V3 HyperSpeed", "prix": "150€", "gaming": 10, "work": 5, "creative": 4, "poids": "55g", "dpi": "30000", "type": "sans fil", "sensor": "Focus Pro 30K", "details": "Gaming léger sans fil"},
                {"nom": "Logitech MX Master 3S", "prix": "120€", "gaming": 5, "work": 10, "creative": 9, "poids": "110g", "dpi": "8000", "type": "sans fil", "sensor": "Darkfield", "details": "Productivité premium"},
                {"nom": "Razer Basilisk Ultimate", "prix": "180€", "gaming": 9, "work": 7, "creative": 5, "poids": "100g", "dpi": "20000", "type": "sans fil", "sensor": "Focus Pro", "details": "Gaming complet sans fil"},
            ],
            ">200": [
                {"nom": "Finalmouse UltraLight 2", "prix": "230€", "gaming": 10, "work": 4, "creative": 3, "poids": "60g", "dpi": "26000", "type": "filaire", "sensor": "Finalmouse", "details": "Ultra-léger esports pro"},
                {"nom": "SteelSeries Rival PRO", "prix": "250€", "gaming": 10, "work": 8, "creative": 6, "poids": "95g", "dpi": "20000", "type": "sans fil", "sensor": "Quantum 2", "details": "Premium esports sans fil"},
                {"nom": "Corsair M65 Elite Wireless", "prix": "220€", "gaming": 9, "work": 9, "creative": 8, "poids": "102g", "dpi": "26000", "type": "sans fil", "sensor": "PMW3688", "details": "Polyvalent premium"},
            ]
        }
        
        candidates = mice_database.get(context["budget"], mice_database["50-100"])
        scored = []
        
        for mouse in candidates:
            score = 0
            
            # Scoring basé sur usage
            if "gaming" in context["usage"]:
                score += mouse["gaming"] * 2
            if "work" in context["usage"]:
                score += mouse["work"] * 2
            if "creative" in context["usage"]:
                score += mouse["creative"] * 2
            
            # Bonus pour contraintes
            if "lightweight" in context["requirements"] and int(mouse["poids"].replace("g", "")) < 75:
                score += 5
            if "wireless" in context["requirements"] and mouse["type"] == "sans fil":
                score += 5
            if "high_dpi" in context["requirements"] and int(mouse["dpi"]) > 15000:
                score += 3
            if "ergonomic" in context["requirements"] and int(mouse["poids"]) > 85:
                score += 3
            
            scored.append((mouse, score))
        
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:3]  # Top 3

def main():
    root = tk.Tk()
    app = AmazonTrackerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
