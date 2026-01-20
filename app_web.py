"""
📱 Amazon Tracker Pro - Application Web Universelle
✅ Fonctionne sur: iPhone, Android, Windows, macOS, Linux
✅ Aucune installation requise - Juste ouvrir dans le navigateur
"""

from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import requests
import json
import os
from datetime import datetime
from activity_logger import ActivityLogger

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Initialiser les modules
activity_logger = ActivityLogger()

# Fichiers de données
ARTICLES_FILE = "articles_tracked.json"
TICKETS_FILE = "support_tickets.json"

def load_json(filename):
    """Charger JSON"""
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_json(filename, data):
    """Sauvegarder JSON"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

@app.route('/')
def index():
    """Page principale"""
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search_product():
    """Rechercher un article en direct depuis Amazon"""
    try:
        query = request.json.get('query', '')
        user = request.json.get('user', 'Anonymous')
        
        if not query:
            return jsonify({'error': 'Query vide'}), 400
        
        articles = search_amazon(query)
        
        # Logger l'action
        activity_logger.log_action(user, 'search', f'Recherche: {query} ({len(articles)} résultats)', 
                                   request.remote_addr or '0.0.0.0')
        
        return jsonify({'articles': articles, 'count': len(articles)})
    
    except Exception as e:
        import traceback
        print(f"❌ Erreur recherche: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e), 'articles': []}), 500


def search_amazon(query):
    """
    Chercher TOUS les résultats sur Amazon.fr
    Retourne jusqu'à 60 articles avec titre, prix, URL et image
    """
    try:
        # URL de recherche Amazon
        url = f"https://www.amazon.fr/s?k={query.replace(' ', '+')}"
        
        # Headers pour se faire passer pour un navigateur
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
        
        # Requête avec timeout
        print(f"🔍 Recherche en cours: {query}")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = []
        
        # CHERCHER TOUS LES ARTICLES POSSIBLES
        print(f"📄 Taille réponse: {len(response.content)} bytes")
        
        # Méthode 1: data-component-type='s-search-result' (PRIMARY)
        items = soup.find_all('div', {'data-component-type': 's-search-result'})
        print(f"  Trouvé {len(items)} items avec data-component-type")
        
        # Méthode 2: Chercher aussi par data-component-type='s-result-item'
        if len(items) < 10:
            items2 = soup.find_all('div', {'data-component-type': 's-result-item'})
            print(f"  Trouvé {len(items2)} items avec s-result-item")
            items.extend(items2)
        
        # EXTRAIRE LES ARTICLES (MAX 60)
        for item in items[:60]:
            try:
                # ====== TITRE ======
                title = 'Titre indisponible'
                
                # Chercher h2
                title_elem = item.find('h2')
                if title_elem:
                    span = title_elem.find('span')
                    if span:
                        title = span.text.strip()
                    else:
                        title = title_elem.text.strip()
                
                # Si vide, chercher le lien
                if title == 'Titre indisponible':
                    link = item.find('a', {'class': lambda x: x and 'a-link-normal' in (x if isinstance(x, str) else ' '.join(x) if isinstance(x, list) else '')})
                    if link:
                        title = link.text.strip() if link.text else 'Titre indisponible'
                
                # ====== PRIX ======
                price = 'Prix indisponible'
                
                # Chercher span avec classe a-price-whole
                price_elem = item.find('span', {'class': 'a-price-whole'})
                if price_elem:
                    price = price_elem.text.strip()
                
                # Sinon chercher tout span a-price
                if price == 'Prix indisponible':
                    price_spans = item.find_all('span', {'class': lambda x: x and 'a-price' in (x if isinstance(x, str) else ' '.join(x) if isinstance(x, list) else '')})
                    if price_spans:
                        for ps in price_spans:
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
                
                # Chercher le lien principal
                link_elem = item.find('a', {'class': lambda x: x and 'a-link-normal' in (x if isinstance(x, str) else ' '.join(x) if isinstance(x, list) else '')})
                if link_elem and 'href' in link_elem.attrs:
                    url_produit = link_elem['href']
                
                # Compléter l'URL si nécessaire
                if url_produit.startswith('/'):
                    # Extraire le vrai URL de produit
                    if '/dp/' in url_produit:
                        # Extraire juste le /dp/XXXXX
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
                rating_elem = item.find('span', {'class': lambda x: x and 'a-icon-star' in (x if isinstance(x, str) else ' '.join(x) if isinstance(x, list) else '')})
                if rating_elem:
                    text = rating_elem.text.strip()
                    if text:
                        rating = text.split()[0]  # Prendre le premier nombre
                
                # Créer l'article
                if title != 'Titre indisponible' and price != 'Prix indisponible':
                    article = {
                        'titre': title[:150],  # Limiter longueur
                        'nom': title[:150],
                        'prix': price,
                        'url': url_produit,
                        'image': img_url,
                        'rating': rating,
                        'date': datetime.now().isoformat()
                    }
                    
                    articles.append(article)
                    print(f"  ✅ {title[:60]}... | {price}")
                
            except Exception as e:
                print(f"  ⚠️  Erreur item: {str(e)}")
                continue
        
        print(f"\n✅ Total: {len(articles)} articles trouvés\n")
        return articles
    
    except Exception as e:
        print(f"❌ Erreur recherche Amazon: {str(e)}")
        import traceback
        traceback.print_exc()
        return []
    
    except Exception as e:
        print(f"❌ Erreur recherche Amazon: {str(e)}")
        return []

@app.route('/api/articles', methods=['GET'])
def get_articles():
    """Récupérer les articles suivis"""
    articles = load_json(ARTICLES_FILE)
    return jsonify({'articles': articles})

@app.route('/api/articles/add', methods=['POST'])
def add_article():
    """Ajouter un article suivi"""
    try:
        article = request.json
        user = request.json.get('user', 'Anonymous')
        
        articles = load_json(ARTICLES_FILE)
        article['id'] = len(articles) + 1
        article['date_ajout'] = datetime.now().isoformat()
        articles.append(article)
        
        save_json(ARTICLES_FILE, articles)
        
        # Logger
        activity_logger.log_action(user, 'add_article', f'Ajout: {article.get("titre")}', '0.0.0.0')
        
        return jsonify({'success': True, 'id': article['id']})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/articles/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
    """Supprimer un article"""
    try:
        user = request.json.get('user', 'Anonymous') if request.json else 'Anonymous'
        articles = load_json(ARTICLES_FILE)
        articles = [a for a in articles if a.get('id') != article_id]
        
        save_json(ARTICLES_FILE, articles)
        
        # Logger
        activity_logger.log_action(user, 'delete_article', f'Suppression article {article_id}', '0.0.0.0')
        
        return jsonify({'success': True})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/support', methods=['POST'])
def create_ticket():
    """Créer un ticket support"""
    try:
        ticket = request.json
        email = ticket.get('email', '')
        
        # Validation email
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return jsonify({'error': 'Email invalide'}), 400
        
        tickets = load_json(TICKETS_FILE)
        
        ticket_id = f"TKT-{len(tickets):06d}"
        ticket['id'] = ticket_id
        ticket['date'] = datetime.now().isoformat()
        ticket['statut'] = 'ouvert'
        
        tickets.append(ticket)
        save_json(TICKETS_FILE, tickets)
        
        # Logger
        activity_logger.log_action(email, 'support_ticket', f'Ticket {ticket_id}', '0.0.0.0')
        
        return jsonify({'success': True, 'id': ticket_id})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/logs', methods=['GET'])
def get_logs():
    """Récupérer les logs"""
    try:
        user = request.args.get('user', '')
        
        if user:
            logs = activity_logger.get_user_logs(user)
        else:
            logs = activity_logger.logs
        
        stats = activity_logger.get_statistics()
        
        return jsonify({
            'logs': logs,
            'stats': stats
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/logs/export', methods=['GET'])
def export_logs():
    """Exporter les logs"""
    try:
        activity_logger.export_logs()
        return jsonify({'success': True, 'message': 'Logs exportés'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # ✅ Démarrer le serveur
    print("═" * 70)
    print("🌐 Amazon Tracker Pro - Application Web")
    print("═" * 70)
    print("📱 Accédez à: http://localhost:3000")
    print("📱 Sur votre téléphone: http://<votre-ip>:3000")
    print("═" * 70)
    
    app.run(host='0.0.0.0', port=3000, debug=True)
