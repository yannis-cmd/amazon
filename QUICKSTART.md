================================================================================
                   AMAZON TRACKER PRO - QUICKSTART
================================================================================

🎯 Démarrage en 5 minutes

================================================================================
1. INSTALLATION
================================================================================

Prérequis:
  - Python 3.10+ (vérifiez: python --version)
  - pip (gestionnaire de paquets)

Étapes:

  a) Ouvrez un terminal dans le répertoire du projet

  b) Installez les dépendances:
     Windows: pip install -r requirements.txt
     Mac/Linux: pip3 install -r requirements.txt

  c) Lancez l'application:
     Windows: python amazon_tracker.py
     Mac/Linux: python3 amazon_tracker.py

     Ou utilisez le point d'entrée principal:
     python main.py

================================================================================
2. UTILISATION DE BASE
================================================================================

RECHERCHER:
  1. Entrez votre requête (ex: "souris gamer")
  2. Cliquez sur "Rechercher"
  3. Attendez les résultats

AJOUTER AU TRACKING:
  1. Cliquez sur un produit dans les résultats
  2. Cliquez sur "Ajouter au tracking"
  3. Le produit s'ajoutera à la liste

PARLER À L'IA:
  1. Allez en bas dans la section "Chat IA"
  2. Tapez votre question (ex: "Quelle souris pour 50€?")
  3. L'IA vous répondra
  4. Si le lien s'affiche, cliquez sur "OUI" pour ouvrir le produit

VOIR LES GRAPHIQUES:
  1. Sélectionnez un produit
  2. Cliquez sur "Graphique"
  3. Voir l'historique des prix

================================================================================
3. EXEMPLES DE REQUÊTES
================================================================================

Recherche simple:
  "souris gamer"
  "clavier mécanique"
  "casque sans fil"

Avec budget:
  "souris pour 30 euros"
  "clavier gamer 50-100€"

Requête IA:
  "Je cherche une souris pour 40 euros avec RGB"
  "Quelle est la meilleure souris gamer pas chère?"
  "Recommande-moi une souris sérieuse"

================================================================================
4. FICHIERS IMPORTANTS
================================================================================

Données:
  articles_tracked.json   - Liste des articles trackés
  search_cache.json       - Cache des résultats (effacé auto après 1h)

Logs:
  logs/amazon_tracker_*.log  - Fichier de log (créé automatiquement)
  logs/errors.log            - Erreurs (si des bugs)

Config:
  config.py              - Configuration app (éditable)
  constants.py           - Constantes (messages, patterns, etc.)
  .env.example           - Modèle de configuration (optionnel)

Code:
  amazon_tracker.py      - Application principale
  main.py                - Point d'entrée
  utils.py              - Utilitaires
  validators.py         - Validateurs
  logger.py             - Logging
  exceptions.py         - Exceptions

Documentation:
  README.md             - Documentation complète
  ARCHITECTURE.md       - Architecture technique
  CONTRIBUTING.md       - Comment contribuer
  MAINTENANCE.md        - Maintenance et debugging
  SECURITY.md           - Politique de sécurité
  CHANGELOG.md          - Historique des versions

================================================================================
5. DÉPANNAGE COURANT
================================================================================

❌ "ModuleNotFoundError: No module named 'requests'"
   ✅ Installez les dépendances: pip install -r requirements.txt

❌ "Pas de résultats trouvés"
   ✅ Amazon peut bloquer les requêtes. Le fallback devrait chercher ailleurs.
   ✅ Attendez quelques secondes avant une nouvelle recherche.
   ✅ Vérifiez votre connexion internet.

❌ "Le chat IA ne répond pas"
   ✅ L'IA est localisée (pas d'API externe). Elle analyse votre texte.
   ✅ Vérifiez les logs: type "tail logs/amazon_tracker_*.log"

❌ "Le lien ne s'ouvre pas"
   ✅ Le produit peut être indisponible.
   ✅ Copiez-collez le lien manuellement.

❌ "L'app crash au démarrage"
   ✅ Vérifiez Python 3.10+: python --version
   ✅ Réinstallez les dépendances: pip install --force-reinstall -r requirements.txt

================================================================================
6. RACCOURCIS CLAVIER
================================================================================

Ctrl+C        - Arrêter l'application
Tab           - Naviguer entre les champs
Entrée        - Valider une recherche / envoyer un message chat
Esc           - Fermer les dialogues

================================================================================
7. TIPS & ASTUCES
================================================================================

🚀 Chercher plus vite:
   - Tapez "souris" au lieu du nom complet
   - Spécifiez le budget pour filtrer les résultats
   - Utilisez des termes simples

💡 Utiliser l'IA:
   - "Quelle souris pour gamer débutant?"
   - "Souris avec meilleur rapport qualité-prix?"
   - "J'ai 30 euros, quoi chercher?"
   - L'IA ajuste sa réponse selon votre profil

📊 Tracker les prix:
   - Cochez "Notifier si prix change" pour alertes
   - Utilisez les graphiques pour voir l'évolution
   - Les prix se mettent à jour quotidiennement

🔄 Optimiser les requêtes:
   - Les résultats sont en cache 1h (fast ⚡)
   - Pas de spam de requêtes (respecte Amazon)
   - Rate limit: minimum 1s entre 2 requêtes

================================================================================
8. STRUCTURE DE L'INTERFACE
================================================================================

╔═══════════════════════════════════════════════════════════════════════════╗
║                        AMAZON TRACKER PRO                                ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  [📌 Rechercher]  [Budget Min: ___]  [Budget Max: ___]  [🔍 Chercher]   ║
║                                                                           ║
║  ┌───────────────────────────────────────────────────────────────────┐  ║
║  │ RÉSULTATS (Top 10)                                               │  ║
║  │ • Souris Gamer RGB - 49€ - ⭐ 4.5 (120 avis)                     │  ║
║  │ • Souris Logitech - 59€ - ⭐ 4.8 (500 avis)                      │  ║
║  │ • Souris SteelSeries - 79€ - ⭐ 4.9 (250 avis)                   │  ║
║  │ ...                                                              │  ║
║  └───────────────────────────────────────────────────────────────────┘  ║
║                                                                           ║
║  ┌───────────────────────────────────────────────────────────────────┐  ║
║  │ ARTICLES TRACKÉS                                                 │  ║
║  │ • Souris Gamer RGB - 49€ (↓ 5€ depuis hier)                      │  ║
║  │ • Clavier Mécanique - 99€ (stable)                               │  ║
║  └───────────────────────────────────────────────────────────────────┘  ║
║                                                                           ║
║  ┌───────────────────────────────────────────────────────────────────┐  ║
║  │ [📊 Graphique] [➕ Ajouter] [🗑️  Supprimer] [🔗 Lien Amazon]     │  ║
║  └───────────────────────────────────────────────────────────────────┘  ║
║                                                                           ║
║  CHAT IA                                                                 ║
║  Vous: Je cherche une souris pour 30€                                   ║
║  IA: Je vous recommande... [Veux-tu le lien?] [OUI] [NON]              ║
║                                                                           ║
║  Vous: OUI                                                               ║
║  IA: Voici: https://amazon.fr/dp/B08ABC... ✅ Lien ouvert!             ║
║                                                                           ║
║  [Message...                                    ] [📤 Envoyer]          ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝

================================================================================
9. ARCHITECTURE LOGIQUE
================================================================================

Flux de recherche:
  Utilisateur tape requête
         ↓
  Validation (min 3 caractères, etc.)
         ↓
  Recherche Amazon réelle (requests + BeautifulSoup)
         ↓
  Fallback si erreur (recherche alternative)
         ↓
  Mise en cache (1 heure)
         ↓
  Affichage résultats
         ↓
  Sauvegarde en BD

Flux de chat IA:
  Utilisateur tape message
         ↓
  Analyse d'intent (5 étapes)
         ↓
  Détection profil utilisateur
         ↓
  Extraction du budget
         ↓
  Génération réponse personnalisée
         ↓
  Demande du lien (si pertinent)
         ↓
  Affichage réponse

================================================================================
10. RESSOURCES
================================================================================

📖 Documentation:
   - README.md - Guide utilisateur complet
   - ARCHITECTURE.md - Design technique
   - CONTRIBUTING.md - Comment contribuer

🐛 Problèmes:
   - MAINTENANCE.md - Guide de debugging
   - logs/ folder - Fichiers de log

🔒 Sécurité:
   - SECURITY.md - Politique et bonnes pratiques

❓ Questions:
   - Consultez la FAQ dans README.md
   - Vérifiez les logs: logs/amazon_tracker_*.log

================================================================================
11. COMMANDES UTILES
================================================================================

Démarrer l'app:
  python amazon_tracker.py
  
  Ou:
  python main.py

Voir les dépendances:
  pip list

Mettre à jour les dépendances:
  pip install --upgrade -r requirements.txt

Vérifier la syntaxe:
  python -m py_compile amazon_tracker.py

Voir les logs:
  tail -f logs/amazon_tracker_*.log

Nettoyer les caches:
  rm search_cache.json

Réinitialiser la BD:
  rm articles_tracked.json

================================================================================
12. CONFIGURATION AVANCÉE
================================================================================

Pour utilisateurs avancés, voir config.py:

- Changer les couleurs (ACCENT_COLOR, BG_DARK, etc.)
- Augmenter délai entre requêtes (respect serveur)
- Modifier le timeout (pour connexions lentes)
- Changer le pays (AMAZON_COUNTRY: fr, en, de, etc.)
- Configurer le logging (niveau DEBUG vs INFO)

================================================================================
13. NOTES IMPORTANTES
================================================================================

✅ L'application est complètement offline une fois lancée
✅ Aucun compte requis
✅ Données stockées localement (JSON)
✅ Respecte les termes de service d'Amazon (rate limiting)
✅ Code sécurisé et validé
✅ Logs complets pour debugging

⚠️  Amazon peut bloquer les requêtes (c'est pour ça qu'il y a un fallback)
⚠️  Les prix peuvent pas s'afficher si produit indisponible
⚠️  Internet requis pour rechercher (local seulement sinon)

================================================================================
14. SUPPORT ET CONTRIBUTION
================================================================================

Vous trouvez un bug?
  1. Consultez les logs: logs/*.log
  2. Lisez MAINTENANCE.md#Debugging
  3. Signalez sur GitHub (si public)

Vous avez une idée?
  1. Lisez CONTRIBUTING.md
  2. Proposez sur GitHub Discussions

Vous voulez contribuer?
  1. Fork le repo
  2. Lisez CONTRIBUTING.md
  3. Créez une branche (feature/ma-feature)
  4. Faites un Pull Request

================================================================================

Prêt? 🚀

  python amazon_tracker.py

Amusez-vous bien et bonne traque! 🎯

================================================================================
Version: 1.0.0
Dernière mise à jour: 18 Janvier 2026
License: MIT
================================================================================
