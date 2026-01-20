# 🖱️ Amazon Tracker Pro - Assistant IA pour Souris

Une application Python complète pour chercher et tracker les souris Amazon avec **Assistant IA intégré** qui recommande les meilleures souris selon votre budget et besoins.

## ✨ Fonctionnalités

- 🔍 **Recherche Amazon.fr** - Cherchez des souris en temps réel
- 🤖 **Assistant IA intelligent** - Recommande les meilleures souris selon:
  - Votre budget (10€ à 500€)
  - Votre usage (gaming, travail, design)
  - Vos contraintes (poids, sans-fil, DPI)
- 📊 **Graphiques prix** - Visualisez l'historique des prix (30 jours)
- 📈 **Suivi personnalisé** - Sauvegardez vos articles préférés
- 🌙 **Mode sombre** - Interface élégante dark theme
- 🔗 **Liens directs** - Ouvrez les produits Amazon immédiatement

## 🚀 Installation

### Prérequis
- Python 3.10+
- pip

```bash
pip install -r requirements.txt
python amazon_tracker.py
```

## 💬 Assistant IA - Exemples

```
Vous: 50
→ IA recommande une souris 50€ + alternatives

Vous: oui
→ IA ouvre Amazon.fr automatiquement
```

## 🔒 Sécurité

**Inclus:**
✅ Code source complet
✅ Base données souris
✅ Web scraping

**Ignoré (`.gitignore`):**
❌ `articles_tracked.json` - Données personnelles
❌ `search_cache.json` - Cache
❌ `__pycache__/` - Python compilé
❌ `.venv/` - Virtual env

**Pas de données sensibles:**
✅ Pas de clés API
✅ Pas de credentials
✅ Code public-safe

## 📊 Pipeline IA (5 Étapes)

1. **INTENT** - Détecte l'intention (recommendation/comparison)
2. **PROFILE** - Détecte expertise (beginner/intermediate/advanced)
3. **CONTEXT** - Parse budget, usage, constraints
4. **SEARCH** - Scoring intelligent des souris
5. **RESPONSE** - Formatée selon le profil

## 🔧 Dépendances

```
requests==2.31.0          # HTTP
beautifulsoup4==4.12.2    # Web scraping
tkinter                   # GUI (inclus)
```

## 📝 License

MIT - Libre d'utilisation

---

**Bon shopping! 🛒**
