"""
Gestion des utilisateurs et des comptes
"""

import json
import os
import hashlib
from datetime import datetime

USERS_FILE = "users.json"

def load_users():
    """Charger les utilisateurs"""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                return []
        except:
            return []
    return []

def save_users(users):
    """Sauvegarder les utilisateurs"""
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

def hash_password(password):
    """Hacher le mot de passe"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, email, password):
    """Créer un nouvel utilisateur"""
    users = load_users()
    
    # Vérifier si l'utilisateur existe
    if any(u['username'].lower() == username.lower() for u in users):
        return {'success': False, 'error': 'Utilisateur existe deja'}
    
    if any(u['email'].lower() == email.lower() for u in users):
        return {'success': False, 'error': 'Email existe deja'}
    
    # Créer l'utilisateur
    user = {
        'id': len(users) + 1,
        'username': username,
        'email': email,
        'password': hash_password(password),
        'created_at': datetime.now().isoformat(),
        'articles': [],
        'settings': {}
    }
    
    users.append(user)
    save_users(users)
    
    return {'success': True, 'user_id': user['id']}

def authenticate_user(username, password):
    """Authentifier un utilisateur"""
    users = load_users()
    
    user = next((u for u in users if u['username'].lower() == username.lower()), None)
    if not user:
        return {'success': False, 'error': 'Utilisateur non trouve'}
    
    if user['password'] != hash_password(password):
        return {'success': False, 'error': 'Mot de passe incorrect'}
    
    # Retourner les données utilisateur (sans le mot de passe)
    user_data = {k: v for k, v in user.items() if k != 'password'}
    return {'success': True, 'user': user_data}

def get_user(user_id):
    """Obtenir les données d'un utilisateur"""
    users = load_users()
    user = next((u for u in users if u['id'] == user_id), None)
    
    if not user:
        return None
    
    return {k: v for k, v in user.items() if k != 'password'}

def add_article_to_user(user_id, article):
    """Ajouter un article à la liste d'un utilisateur"""
    users = load_users()
    
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return {'success': False, 'error': 'Utilisateur non trouve'}
    
    # Ajouter un ID et une date
    article['id'] = len(user['articles']) + 1
    article['date_added'] = datetime.now().isoformat()
    
    user['articles'].append(article)
    save_users(users)
    
    return {'success': True, 'article_id': article['id']}

def get_user_articles(user_id):
    """Obtenir les articles d'un utilisateur"""
    user = get_user(user_id)
    if not user:
        return []
    
    return user.get('articles', [])

def remove_article_from_user(user_id, article_id):
    """Supprimer un article de la liste d'un utilisateur"""
    users = load_users()
    
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return {'success': False, 'error': 'Utilisateur non trouve'}
    
    user['articles'] = [a for a in user['articles'] if a.get('id') != article_id]
    save_users(users)
    
    return {'success': True}
