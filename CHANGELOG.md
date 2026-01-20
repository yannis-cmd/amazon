# CHANGELOG.md - Historique des Versions

Tous les changements notables dans ce projet seront documentés dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-18

### ✨ Ajouté
- ✅ Interface GUI sombre professionnelle avec tkinter
- ✅ Recherche Amazon réelle avec BeautifulSoup4 et requests
- ✅ Recherche fallback en cas d'erreur réseau
- ✅ Tracking automatique des prix avec historique
- ✅ Graphiques de prix avec matplotlib
- ✅ Assistant IA 5-étapes intelligent et conversationnel
- ✅ Détection automatique du profil utilisateur (débutant/intermediate/avancé)
- ✅ Détection du budget (simple: "20€", range: "20-50€")
- ✅ Ouverture de liens Amazon dans navigateur
- ✅ Feature "Veux-tu le lien?" - le chat propose le lien
- ✅ Recherche de lien automatique quand utilisateur dit "OUI"
- ✅ Mise en cache locale (1h) pour éviter requêtes répétées
- ✅ Persistance de la BD en JSON
- ✅ Logging structuré (fichier + console)
- ✅ Gestion d'erreurs robuste avec exceptions personnalisées
- ✅ Type hints complets sur tous les paramètres
- ✅ Docstrings Google-style
- ✅ Rate limiting respectueux du serveur
- ✅ Mode sombre avec couleurs Amazon (#FF9900)
- ✅ Configuration centralisée
- ✅ Utilitaires réutilisables
- ✅ Documentation complète

### 📚 Modules Professionnels
- ✅ `config.py` - Configuration centralisée
- ✅ `constants.py` - Constantes et messages
- ✅ `utils.py` - Utilitaires réutilisables  
- ✅ `logger.py` - Logging configuré
- ✅ `exceptions.py` - Exceptions personnalisées
- ✅ `types.py` - Type hints personnalisés

### 📖 Documentation
- ✅ README.md - Guide utilisateur complet
- ✅ QUICKSTART.txt - Démarrage rapide
- ✅ ARCHITECTURE.md - Architecture détaillée
- ✅ CONTRIBUTING.md - Guide de contribution
- ✅ MAINTENANCE.md - Guide de maintenance
- ✅ SECURITY.md - Politique de sécurité
- ✅ LICENSE - MIT License
- ✅ .gitignore - Fichiers à ignorer
- ✅ requirements.txt - Dépendances

### 🔒 Sécurité
- ✅ Input validation sur toutes les entrées
- ✅ Sanitization des chaînes (XSS prevention)
- ✅ Rate limiting (respect serveur Amazon)
- ✅ Pas de données sensibles stockées
- ✅ Erreurs loggées pour audit

### ⚡ Performance
- ✅ Opérations bloquantes en threads
- ✅ Cache local des résultats (1h TTL)
- ✅ UI responsive (< 500ms update)
- ✅ Recherche < 5s en moyenne
- ✅ Réponse IA < 2s

### 🐛 Corrections
- ✅ Budget "20" = 20€ (pas 200€)
- ✅ Réponses IA courtes (~10 lignes)
- ✅ Chat input fiable (sans délai)
- ✅ Liens Amazon détectés correctement
- ✅ Pas de messages redondants

## [0.9.0] - 2026-01-15

### ⚠️ Pre-Release
- Prototype fonctionnel
- Interface basique
- Recherche manuelle
- Chat IA en développement
- Documentation partielle

---

## Notes de Version

### Pour migrer de 0.9.0 → 1.0.0

1. **Mises à jour requises**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configuration**:
   - Copiez `.env.example` en `.env` (optionnel)
   - Aucune configuration requise pour démarrer

3. **Données existantes**:
   - Compatible avec `articles_tracked.json` v0.9
   - Aucune migration nécessaire
   - `search_cache.json` sera régénéré automatiquement

4. **Nouvelles fonctionnalités**:
   - Logging automatique dans `logs/` folder
   - Consultez README.md pour guide complet

---

## Roadmap

### V1.1 (Q2 2026)
- [ ] Support multi-marchands (eBay, Rakuten, etc.)
- [ ] Notifications email pour alertes prix
- [ ] Export données (CSV, PDF)
- [ ] Mode clair (Light theme)
- [ ] Paramètres utilisateur
- [ ] Historique de recherche

### V1.2 (Q3 2026)
- [ ] Support multi-produits (pas juste souris)
- [ ] Dashboard avec statistiques
- [ ] Prédiction prix (ML)
- [ ] API REST pour intégration
- [ ] Sync cloud optionnel

### V2.0 (Q4 2026)
- [ ] Application web
- [ ] Application mobile (iOS/Android)
- [ ] Base de données serveur
- [ ] Collaborative tracking (partage listes)
- [ ] Webhooks et notifications Slack

---

## Types de Changements

- **✨ Ajouté**: Nouvelle fonctionnalité
- **🔄 Changé**: Fonctionnalité existante modifiée
- **🗑️ Supprimé**: Fonctionnalité supprimée
- **🐛 Corrigé**: Bug corrigé
- **⚡ Optimisé**: Performance améliorée
- **📚 Docs**: Documentation ajoutée/modifiée
- **🔒 Sécurité**: Correctif de sécurité
- **⚠️ Deprecated**: Feature dépréciée

---

## Guide de Compatibility

| Version | Python | tkinter | requests | bs4 |
|---------|--------|---------|----------|-----|
| 1.0.x   | 3.10+  | Stdlib  | 2.31+    | 4.12+ |
| 0.9.x   | 3.9+   | Stdlib  | 2.28+    | 4.10+ |

---

## Contribution

Consultez [CONTRIBUTING.md](CONTRIBUTING.md) pour les directives de contribution.

---

## Remerciements

Un grand merci à:
- Communauté Python
- BeautifulSoup4
- Requests library
- tkinter contributors

---

**Dernière mise à jour**: 18 Janvier 2026  
**Version actuelle**: 1.0.0
