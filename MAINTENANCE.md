# MAINTENANCE.md - Guide de Maintenance

## Vue d'ensemble

Ce document décrit comment maintenir, tester et déployer Amazon Tracker Pro en production.

## Checks de Santé

### Avant chaque release

```bash
# 1. Vérifier la syntaxe Python
python -m py_compile amazon_tracker.py
python -m py_compile config.py
python -m py_compile *.py

# 2. Vérifier les imports
python -c "import amazon_tracker; print('OK')"

# 3. Tester en standalone
python amazon_tracker.py &
# Testez manuellement les fonctionnalités principales
# Ctrl+C pour arrêter

# 4. Vérifier les fichiers de log
ls -la logs/

# 5. Vérifier les fichiers de données
cat articles_tracked.json
cat search_cache.json
```

### Vérifications régulières

**Quotidiennes**:
- [ ] Pas de crash au démarrage
- [ ] Recherche fonctionne
- [ ] Chat IA répond
- [ ] Pas d'erreurs dans les logs

**Hebdomadaires**:
- [ ] Performance acceptable (< 5s recherche)
- [ ] Cache fonctionne
- [ ] BD n'est pas corrompue
- [ ] Mémoire stable (< 200MB)

**Mensuelles**:
- [ ] Liens Amazon toujours valides
- [ ] Parsing HTML pas cassé
- [ ] Pas de dépendances obsolètes
- [ ] Tests passent à 100%


## Performance et Monitoring

### Métriques à suivre

```python
# Temps de réponse
- Démarrage app: < 3s
- Recherche: < 5s
- Réponse IA: < 2s
- UI update: < 500ms

# Mémoire
- Démarrage: ~80MB
- Normal: ~150MB
- Max acceptable: 300MB

# Disque
- DB (articles_tracked.json): < 1MB
- Cache (search_cache.json): < 5MB
- Logs: < 50MB (archivés automatiquement)
```

### Outils de monitoring

```python
# En haut du amazon_tracker.py pour debug
import psutil
import os

def log_memory():
    """Log mémoire utilisée"""
    process = psutil.Process(os.getpid())
    memory = process.memory_info().rss / 1024 / 1024
    print(f"Mémoire utilisée: {memory:.1f}MB")

# Appelé périodiquement:
log_memory()
```

### Profiling

```bash
# Installez cProfile
python -m cProfile -s cumulative amazon_tracker.py

# Utilisez snakeviz pour visualiser
pip install snakeviz
python -m cProfile -o stats.prof amazon_tracker.py
snakeviz stats.prof
```


## Gestion des Logs

### Structure des logs

```
logs/
├── amazon_tracker_20260118_143022.log  # Log complet du jour
├── amazon_tracker_20260117_102015.log  # Ancien
├── errors.log                           # Erreurs uniquement (append)
└── ...
```

### Politique d'archivage

```python
# Automatique après 5MB par fichier
# Garder 5 fichiers historiques

logging.handlers.RotatingFileHandler(
    filename,
    maxBytes=5*1024*1024,  # 5MB
    backupCount=5          # 5 fichiers
)
```

### Lecture des logs

```bash
# Voir tous les logs aujourd'hui
tail -f logs/amazon_tracker_*.log

# Chercher erreurs
grep ERROR logs/*.log

# Voir dernières 100 lignes
tail -100 logs/amazon_tracker_*.log

# Chercher pattern spécifique
grep "SearchException" logs/*.log

# Voir timeline
cat logs/*.log | grep "2026-01-18"
```

### Nettoyage

```bash
# Supprimer logs vieux
find logs -name "*.log" -mtime +30 -delete

# Compresser
gzip logs/*.log

# Archiver
tar -czf logs_archive_2026_01.tar.gz logs/*.log.gz
```


## Debugging

### Activer mode debug

```python
# Dans amazon_tracker.py au démarrage:

import logging
logging.getLogger("amazon_tracker").setLevel(logging.DEBUG)

# Maintenant tous les debug messages s'affichent
logger.debug("Message de debug")
```

### Tracer une erreur

1. **Cherchez dans les logs**:
   ```bash
   grep "ERROR" logs/*.log | tail -20
   ```

2. **Lisez le traceback complet**:
   ```bash
   grep -A 10 "SearchException" logs/*.log
   ```

3. **Reproduisez le bug**:
   - Étapes exactes
   - Même input
   - Même OS/Python

4. **Fixez et testez**:
   ```bash
   python amazon_tracker.py
   # Testez reproduction
   ```

5. **Vérifiez les logs**:
   ```bash
   tail -20 logs/amazon_tracker_*.log
   ```

### Debug interactif

```python
# Ajoutez breakpoint temporaire
import pdb

# Dans le code:
def ma_fonction():
    x = 5
    pdb.set_trace()  # Pause ici
    y = x + 10
```

Commandes pdb:
```
n - Prochaine ligne
s - Rentre dans la fonction
c - Continue
p variable - Affiche variable
l - Liste le code
q - Quit
```


## Problèmes Courants

### Problème: App crash au démarrage

**Cause possible**: Import échoué

```bash
# Test imports
python -c "import tkinter; import requests; import bs4; print('OK')"

# Voir erreur
python -c "import amazon_tracker" 2>&1
```

**Solution**:
```bash
# Vérifiez requirements
pip install -r requirements.txt

# Vérifiez Python version
python --version  # Doit être 3.10+
```

### Problème: Pas de résultats Amazon

**Cause possible**: Amazon bloque les requêtes

**Solution**:
```python
# Augmentez delai entre requêtes
MIN_SEARCH_DELAY = 3.0  # au lieu de 1.0

# Changez User-Agent
USER_AGENT = "Mozilla/5.0..."  # Ou autre
```

### Problème: Chat IA ne répond pas

**Cause possible**: Parsing erreur ou input malformé

**Logs**:
```bash
grep "ai\|chat" logs/*.log
```

**Debug**:
```python
# Testez parsing
from utils import extract_budget_from_text
result = extract_budget_from_text("20 euros")
print(result)

# Testez intent detection
from amazon_tracker import AmazonTracker
tracker = AmazonTracker(root)
result = tracker.analyze_intent("Je veux une souris pour 50€")
print(result)
```

### Problème: BD corrompue (JSON invalide)

**Symptômes**: Erreur JSON decode

**Recovery**:
```bash
# Sauvegardez l'ancienne
cp articles_tracked.json articles_tracked.json.backup

# Créez une neuve vide
echo "{}" > articles_tracked.json

# Vérifiez
python -c "import json; json.load(open('articles_tracked.json'))"
```

### Problème: Lent / Freeze

**Cause**: Opération longue qui bloque l'interface

**Solution**:
```python
# Vérifiez threading
# Toutes les opérations longues doivent être dans un thread:

import threading

def operation_longue():
    # Celle-ci est bloquante
    pass

# ✅ Bon:
thread = threading.Thread(target=operation_longue)
thread.start()

# ❌ Mauvais:
operation_longue()  # Bloque l'UI
```


## Mises à jour des dépendances

### Vérifier versions

```bash
# Voir versions instalées
pip list

# Chercher outdated
pip list --outdated

# Vérifier spécifique
pip show requests
```

### Mettre à jour

```bash
# Mettre à jour une dépendance
pip install --upgrade requests

# Ou mettre à jour toutes
pip install --upgrade -r requirements.txt

# Ou spécifier version
pip install requests==2.32.0
```

### Vérifier compatibilité

Après mise à jour:
```bash
# Test imports
python -c "import amazon_tracker; print('OK')"

# Test app
python amazon_tracker.py

# Test recherche et chat
# Puis vérifiez logs
```

### Updater requirements.txt

```bash
# Générer depuis env actuel
pip freeze > requirements.txt

# Ou garder versions compatibles min
# requirements.txt: requests>=2.31.0
```


## Backup et Restauration

### Backup automatique

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p backups

# Sauvegardez les données
cp articles_tracked.json backups/articles_${DATE}.json
cp search_cache.json backups/cache_${DATE}.json

# Compressez
tar -czf backups/backup_${DATE}.tar.gz backups/*.json

echo "Backup créé: backups/backup_${DATE}.tar.gz"
```

Ajouter à cron (Linux/Mac):
```bash
crontab -e

# Tous les jours à 2h du matin
0 2 * * * /chemin/vers/backup.sh
```

### Restaurer

```bash
# Lister backups
ls -la backups/

# Restaurer spécifique
cp backups/articles_20260118.json articles_tracked.json
cp backups/cache_20260118.json search_cache.json

# Ou depuis archive
tar -xzf backups/backup_20260118_020000.tar.gz
```


## Déploiement

### Checklist avant release

- [ ] Tests passent
- [ ] Logs propres (pas d'erreurs)
- [ ] Performance acceptable
- [ ] Documentation à jour
- [ ] CHANGELOG.md mis à jour
- [ ] Version bumped (semver)
- [ ] Tous les commits squashés

### Créer release

```bash
# 1. Vérifiez version
cat README.md | grep "Version"

# 2. Taggez
git tag -a v1.0.1 -m "Release 1.0.1"
git push origin v1.0.1

# 3. Créez release sur GitHub
# Allez sur GitHub > Releases > Draft new release
# Sélectionnez le tag et remplissez le formulaire
```

### Update utilisateurs

```markdown
# Version 1.0.1 - 18 Janvier 2026

## Nouveautés
- Feature X
- Amélioration Y

## Corrections
- Bug Z corrigé

## Installation
```bash
pip install --upgrade amazon-tracker
```

## Remerciements
...
```


## Rollback

### Si version cassée

```bash
# Retour à version précédente
git revert HEAD
git push origin main

# Ou reset à tag précédent
git reset --hard v1.0.0
git push -f origin main
```


## Support et SLA

### Priorités

| Priorité | Temps Réponse | Exemple |
|----------|----------------|---------|
| CRITICAL | < 1h | App ne démarre pas |
| HIGH | < 24h | Feature cassée |
| MEDIUM | < 1 semaine | Bug mineur |
| LOW | < 1 mois | Amélioration |

### Résolution

1. Diagnostiquez
2. Isolez le problème
3. Fixez
4. Testez
5. Documentez
6. Communiquez


## Ressources

- Logs: `logs/` folder
- Configs: `config.py`
- Erreurs: `logs/errors.log`
- Données: `articles_tracked.json`

---

**Dernière mise à jour**: 18 Janvier 2026  
**Mainteneur**: Development Team
