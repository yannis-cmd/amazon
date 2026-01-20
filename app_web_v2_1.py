"""
Amazon Tracker Pro - Application Web Universelle V2.1
Support client fiable + Graphique evolution des prix
Protection anti-bot (retry, headers varies)
Fonctionne sur: iPhone, Android, Windows, macOS, Linux
Intégration Discord webhook pour logs cloud
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests
import json
import os
import re
import time
from datetime import datetime
from activity_logger import ActivityLogger

# Configuration Discord Webhook
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1462917224154005647/eDTFaXGmuPFZlGJMLxJukL1f6qroMX7kDHGepF_WEaMw5cu0EHG9isxk8FclBcpum1_1"

def send_to_discord(title, message, color=3447003):
    """Envoyer un message sur Discord via webhook"""
    try:
        embed = {
            "title": title,
            "description": message,
            "color": color,
            "timestamp": datetime.now().isoformat()
        }
        payload = {"embeds": [embed]}
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5)
        if response.status_code not in [200, 204]:
            print(f"Discord error: {response.status_code}")
        return response.status_code
    except Exception as e:
        print(f"Discord send error: {str(e)}")
        return None

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['ENV'] = 'production'  # Désactiver le reloader automatique

# Activer CORS
CORS(app)

# Initialiser les modules
activity_logger = ActivityLogger()

# Fichiers de données
ARTICLES_FILE = "articles_tracked.json"
TICKETS_FILE = "support_tickets.json"
PRICE_HISTORY_FILE = "price_history.json"

def load_json(filename):
    """Charger JSON - retourne toujours une liste"""
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # S'assurer que c'est une liste
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict):
                    return []  # Si c'est un dict, retourner une liste vide
                return []
        except:
            return []
    return []

def save_json(filename, data):
    """Sauvegarder JSON"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def save_price_history(article_name, price):
    """Enregistrer le prix dans l'historique"""
    try:
        history = load_json(PRICE_HISTORY_FILE)
        if not isinstance(history, list):
            history = []
        
        # Ajouter une nouvelle entrée
        entry = {
            'nom': article_name,
            'prix': price,
            'date': datetime.now().isoformat()
        }
        history.append(entry)
        save_json(PRICE_HISTORY_FILE, history)
    except:
        pass

@app.route('/')
def index():
    """Page principale"""
    return render_template('index_improved.html')

@app.route('/api/search', methods=['POST'])
def search_product():
    """Rechercher un article en direct depuis Amazon"""
    log_file = "/tmp/search_debug.log" if os.path.exists('/tmp') else "search_debug.log"
    try:
        with open(log_file, 'a') as f:
            f.write(f"\n=== SEARCH REQUEST ===\n")
            query = request.json.get('query', '')
            user = request.json.get('user', 'Anonymous')
            page = request.json.get('page', 1)  # Pagination
            f.write(f"Query: {query}, User: {user}, Page: {page}\n")
            
            if not query:
                f.write("ERROR: Empty query\n")
                return jsonify({'error': 'Query vide'}), 400
            
            f.write(f"Calling search_amazon_all...\n")
            articles = search_amazon_all(query, page)
            f.write(f"Got {len(articles)} articles\n")
            
            # Logger l'action
            activity_logger.log_action(user, 'search', f'Recherche: {query} page {page} ({len(articles)} résultats)', 
                                       request.remote_addr or '0.0.0.0')
            
            # Discord désactivé - logs locaux uniquement
            # send_to_discord(
            #     "RECHERCHE AMAZON",
            #     f"**Utilisateur:** {user}\n**Requête:** {query}\n**Page:** {page}\n**Résultats:** {len(articles)} articles",
            #     color=3447003
            # )
            
            f.write(f"Returning response\n")
            return jsonify({'articles': articles, 'count': len(articles), 'page': page})
        
    except Exception as e:
        import traceback
        with open(log_file, 'a') as f:
            f.write(f"ERROR: {str(e)}\n")
            f.write(traceback.format_exc())
        return jsonify({'error': str(e), 'articles': []}), 500


def search_amazon(query):
    """
    Chercher TOUS les résultats sur Amazon.fr - PAGE 1
    Retourne jusqu'à 120 articles
    """
    return search_amazon_all(query, page=1)


def search_amazon_all(query, page=1):
    """
    Chercher TOUT le catalogue Amazon
    Retourne jusqu'à 120 articles par page
    Avec protection anti-bot (retry, headers variés, delays)
    """
    try:
        print(f"\n  [search_amazon_all] Début pour query={query}, page={page}")
        # Calculer le offset pour la pagination
        # Amazon utilise 'page' dans l'URL
        url = f"https://www.amazon.fr/s?k={query.replace(' ', '+')}&page={page}"
        print(f"  [search_amazon_all] URL: {url}")
        
        # Headers variés pour éviter les 503
        headers_list = [
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'fr-FR,fr;q=0.9',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            },
            {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'fr-FR,fr;q=0.9',
            },
            {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'fr-FR,fr;q=0.9',
            }
        ]
        
        # Requête avec retry
        print(f"🔍 Recherche en cours: {query} (page {page})")
        response = None
        
        for attempt in range(3):
            try:
                headers = headers_list[attempt % len(headers_list)]
                print(f"  Tentative {attempt + 1}/3...")
                
                # Ajouter un délai pour éviter les blocages
                if attempt > 0:
                    time.sleep(5 + attempt * 3)
                
                response = requests.get(url, headers=headers, timeout=20)
                
                if response.status_code == 200:
                    print(f"  ✅ Réponse reçue ({len(response.content)} bytes)")
                    break
                elif response.status_code == 503:
                    print(f"  ⚠️  503 Service Unavailable, attente longue...")
                    if attempt < 2:
                        time.sleep(8 + attempt * 4)
                    continue
                elif response.status_code == 429:
                    print(f"  ⚠️  429 Too Many Requests, attente très longue...")
                    if attempt < 2:
                        time.sleep(15 + attempt * 5)
                    continue
                else:
                    print(f"  ⚠️  Status {response.status_code}")
                    if attempt < 2:
                        time.sleep(3 + attempt * 2)
                    continue
                    
            except Exception as e:
                print(f"  ❌ Erreur requête: {e}")
                if attempt < 2:
                    time.sleep(3 + attempt * 2)
                continue
        
        if not response or response.status_code != 200:
            print(f"❌ Erreur: Amazon indisponible")
            return []
        
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = []
        
        # CHERCHER TOUS LES ARTICLES POSSIBLES
        print(f"📄 Parsing HTML (page {page})...")
        
        # Tous les types de divs contenant les produits
        items = soup.find_all('div', {'data-component-type': 's-search-result'})
        print(f"  Trouvé {len(items)} items avec s-search-result")
        
        if len(items) < 10:
            items2 = soup.find_all('div', {'data-component-type': 's-result-item'})
            print(f"  Trouvé {len(items2)} items avec s-result-item")
            items.extend(items2)
        
        # EXTRAIRE LES ARTICLES (MAX 120 par page)
        for item in items[:120]:
            try:
                # ====== TITRE ======
                title = 'Titre indisponible'
                
                title_elem = item.find('h2')
                if title_elem:
                    span = title_elem.find('span')
                    if span:
                        title = span.text.strip()
                    else:
                        title = title_elem.text.strip()
                
                if not title or title == 'Titre indisponible':
                    link = item.find('a', {'class': 'a-link-normal'})
                    if link:
                        title = link.text.strip() if link.text else 'Titre indisponible'
                
                # ====== PRIX ======
                price = 'Prix indisponible'
                
                price_elem = item.find('span', {'class': 'a-price-whole'})
                if price_elem:
                    price = price_elem.text.strip()
                
                if not price or price == 'Prix indisponible':
                    price_spans = item.find_all('span')
                    for ps in price_spans:
                        cls = ps.get('class', [])
                        if isinstance(cls, list):
                            cls_str = ' '.join(cls)
                        else:
                            cls_str = str(cls) if cls else ''
                        
                        if 'a-price' in cls_str:
                            text = ps.text.strip()
                            if text and any(c.isdigit() for c in text):
                                price = text
                                break
                
                # ====== IMAGE ======
                img_url = ''
                img_elem = item.find('img')
                if img_elem and 'src' in img_elem.attrs:
                    img_url = img_elem['src']
                
                # ====== URL PRODUIT ======
                url_produit = '#'
                
                link_elem = item.find('a', {'class': 'a-link-normal'})
                if link_elem and 'href' in link_elem.attrs:
                    url_produit = link_elem['href']
                
                if url_produit.startswith('/'):
                    if '/dp/' in url_produit:
                        parts = url_produit.split('/')
                        if 'dp' in parts:
                            idx = parts.index('dp')
                            if idx + 1 < len(parts):
                                product_id = parts[idx + 1]
                                url_produit = f'https://www.amazon.fr/dp/{product_id}'
                    else:
                        url_produit = 'https://www.amazon.fr' + url_produit
                
                # ====== RATING ======
                rating = '0'
                rating_elem = item.find('span', {'class': lambda x: x and 'a-icon-star' in str(x) if x else False})
                if rating_elem:
                    text = rating_elem.text.strip()
                    if text:
                        rating = text.split()[0]
                
                # Créer l'article
                if title and title != 'Titre indisponible' and price and price != 'Prix indisponible':
                    article = {
                        'titre': title[:150],
                        'nom': title[:150],
                        'prix': price,
                        'url': url_produit,
                        'image': img_url,
                        'rating': rating,
                        'page': page,
                        'date': datetime.now().isoformat()
                    }
                    
                    articles.append(article)
                    if len(articles) % 10 == 0:
                        print(f"  ✅ {len(articles)} articles trouvés...")
                
            except Exception as e:
                continue
        
        print(f"\n✅ Page {page}: {len(articles)} articles trouvés\n")
        return articles
    
    except Exception as e:
        print(f"❌ Erreur recherche Amazon: {str(e)}")
        import traceback
        traceback.print_exc()
        return []


@app.route('/api/articles', methods=['GET'])
def get_articles():
    """Obtenir les articles suivis"""
    try:
        articles = load_json(ARTICLES_FILE)
        return jsonify({'articles': articles})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/articles/add', methods=['POST'])
def add_article():
    """Ajouter un article à suivre"""
    try:
        article = request.json
        articles = load_json(ARTICLES_FILE)
        
        # S'assurer que c'est une liste
        if not isinstance(articles, list):
            articles = []
        
        # Créer l'article
        new_article = {
            'id': len(articles) + 1,
            'titre': article.get('titre', 'Sans titre'),
            'nom': article.get('titre', 'Sans titre'),
            'prix': article.get('prix', 'N/A'),
            'date_ajout': datetime.now().isoformat(),
            'user': article.get('user', 'Web User')
        }
        
        articles.append(new_article)
        save_json(ARTICLES_FILE, articles)
        
        # Enregistrer le prix dans l'historique
        save_price_history(new_article['titre'], new_article['prix'])
        
        # Logger
        activity_logger.log_action(new_article['user'], 'add_article', f'Article: {new_article["titre"]}', '0.0.0.0')
        
        # Discord désactivé - logs locaux uniquement
        # send_to_discord(
        #     "ARTICLE AJOUTE",
        #     f"**Utilisateur:** {new_article['user']}\n**Article:** {new_article['titre']}\n**Prix:** {new_article['prix']}",
        #     color=65280
        # )
        
        return jsonify({'success': True, 'id': new_article['id']})
    
    except Exception as e:
        print(f"❌ Erreur add_article: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/articles/delete/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
    """Supprimer un article"""
    try:
        articles = load_json(ARTICLES_FILE)
        
        # S'assurer que c'est une liste
        if not isinstance(articles, list):
            articles = []
        
        articles = [a for a in articles if a.get('id') != article_id]
        save_json(ARTICLES_FILE, articles)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/support', methods=['POST'])
def create_ticket():
    """Créer un ticket support"""
    try:
        data = request.json
        email = data.get('email', '').strip()
        title = data.get('titre', '').strip()
        description = data.get('description', '').strip()
        priority = data.get('priorite', 'normale').strip()
        
        # Validation
        if not email:
            return jsonify({'error': 'Email requis'}), 400
        
        # Email validation regex
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return jsonify({'error': 'Email invalide'}), 400
        
        if not title:
            return jsonify({'error': 'Titre requis'}), 400
        
        if not description:
            return jsonify({'error': 'Description requise'}), 400
        
        # Créer le ticket
        tickets = load_json(TICKETS_FILE)
        
        # S'assurer que c'est une liste
        if not isinstance(tickets, list):
            tickets = []
        
        ticket_id = f"TKT-{len(tickets):06d}"
        
        ticket = {
            'id': ticket_id,
            'titre': title,
            'description': description,
            'email': email,
            'priorite': priority,
            'statut': 'ouvert',
            'date': datetime.now().isoformat()
        }
        
        tickets.append(ticket)
        save_json(TICKETS_FILE, tickets)
        
        # Logger
        activity_logger.log_action(email, 'support_ticket', f'Ticket {ticket_id}: {title}', request.remote_addr or '0.0.0.0')
        
        # Discord désactivé - logs locaux uniquement
        # priority_colors = {'critique': 15158332, 'urgente': 16711680, 'normale': 3447003}
        # send_to_discord(
        #     f"TICKET SUPPORT - {ticket_id}",
        #     f"**Email:** {email}\n**Titre:** {title}\n**Priorité:** {priority}\n**Description:** {description[:200]}...",
        #     color=priority_colors.get(priority, 3447003)
        # )
        
        print(f"OK Ticket créé: {ticket_id}")
        
        return jsonify({
            'success': True,
            'id': ticket_id,
            'message': f'OK Ticket {ticket_id} créé avec succès!'
        })
    
    except Exception as e:
        print(f"❌ Erreur création ticket: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/support/list', methods=['GET'])
def get_tickets():
    """Lister les tickets support"""
    try:
        tickets = load_json(TICKETS_FILE)
        # S'assurer que c'est une liste
        if not isinstance(tickets, list):
            tickets = []
        return jsonify({'tickets': tickets})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/logs', methods=['GET', 'POST'])
def get_logs():
    """Obtenir les logs d'activité - Authentification requise"""
    try:
        # Récupérer le mot de passe depuis les paramètres ou le JSON
        password = request.args.get('password') or (request.json.get('password') if request.json else None)
        
        # Verifier mot de passe = "tg"
        if password != 'tg':
            return jsonify({'error': 'Mot de passe incorrect'}), 401
        
        # Password OK - retourner les logs
        logs = activity_logger.get_all_logs()
        stats = activity_logger.get_statistics()
        return jsonify({'logs': logs, 'stats': stats})
        
    except Exception as e:
        return jsonify({'error': 'Internal error', 'details': str(e)}), 500


@app.route('/api/price-history/<article_name>', methods=['GET'])
def get_price_history(article_name):
    """Obtenir l'historique des prix pour un article"""
    try:
        history = load_json(PRICE_HISTORY_FILE)
        article_history = [h for h in history if h.get('nom').lower() == article_name.lower()]
        
        if not article_history:
            return jsonify({'dates': [], 'prix': []})
        
        # Trier par date
        article_history = sorted(article_history, key=lambda x: x.get('date', ''))
        
        dates = [h.get('date', '')[:10] for h in article_history]  # YYYY-MM-DD
        prix = [float(re.sub(r'[^\d,.]', '', h.get('prix', '0')).replace(',', '.')) for h in article_history]
        
        return jsonify({'dates': dates, 'prix': prix, 'nombre': len(article_history)})
    
    except Exception as e:
        print(f"Erreur: {e}")
        return jsonify({'dates': [], 'prix': []}), 500


if __name__ == '__main__':
    print("\nSOURI Server Amazon Tracker Pro V2.1")
    print("WEB Access at: http://localhost:3000")
    print("STOP: Ctrl+C\n")
    app.run(host='0.0.0.0', port=3000, debug=False, use_reloader=False)
