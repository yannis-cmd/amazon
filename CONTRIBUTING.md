# CONTRIBUTING.md - Guide de Contribution

## Bienvenue! 👋

Merci de vouloir contribuer à Amazon Tracker Pro. Ce document explique comment contribuer efficacement.

## Code of Conduct

- Soyez respectueux
- Soyez inclusif
- Signalez les problèmes de sécurité en privé
- Pas de harcèlement


## Comment Contribuer

### 1. Signaler un Bug

**Avant de signaler**:
- Vérifiez que le bug n'existe pas déjà
- Testez avec la dernière version
- Rassemblez les informations

**Inclure dans le rapport**:
```markdown
**Description**: 
Décrivez le bug clairement

**Étapes pour reproduire**:
1. Lancez l'app avec...
2. Cliquez sur...
3. Le problème apparaît

**Comportement attendu**:
Il devrait...

**Journaux d'erreur**:
```
[Collez les logs ici]
```

**Système**:
- OS: Windows 10 / macOS / Linux
- Python: 3.13
```

### 2. Proposer une Feature

**Avant de proposer**:
- Vérifiez qu'elle n'existe pas
- Assurez-vous qu'elle s'aligne avec le projet

**Template**:
```markdown
**Description**:
Bref résumé de la feature

**Motivation**:
Pourquoi c'est utile?

**Cas d'usage**:
Exemple d'utilisation

**Implémentation envisagée**:
Comment ferait-on techniquement?

**Alternatives envisagées**:
Autres approches?

**Complexité estimée**:
Facile / Moyen / Difficile
```

### 3. Soumettre du Code

#### Setup initial

```bash
# Clonez le repo
git clone https://github.com/votreusername/amazon_tracker.git
cd amazon_tracker

# Créez une branche
git checkout -b feature/ma-feature
```

#### Avant de commencer

1. **Comprenez l'architecture**: Lisez [ARCHITECTURE.md](ARCHITECTURE.md)
2. **Configurez l'environnement**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```
3. **Testez que c'est fonctionnel**:
   ```bash
   python amazon_tracker.py
   ```

#### Pendant le développement

**Conventions de codage**:

1. **Nommage**:
   ```python
   # Classes
   class AmazonTracker:
       pass
   
   # Fonctions
   def search_article(query: str) -> List[Dict]:
       pass
   
   # Constantes
   MAX_RESULTS = 10
   
   # Privé
   def _internal_method(self):
       pass
   ```

2. **Type Hints** (OBLIGATOIRE):
   ```python
   # ❌ Non
   def search(query):
       return results
   
   # ✅ Oui
   def search(query: str) -> List[Dict[str, Any]]:
       return results
   ```

3. **Docstrings** (Format Google):
   ```python
   def search_article(self, query: str) -> List[Dict[str, Any]]:
       """Recherche les articles sur Amazon.
       
       Args:
           query: Requête de recherche (ex: "souris gamer")
           
       Returns:
           Liste des produits trouvés avec prix, URL, etc.
           
       Raises:
           ValidationException: Si requête invalide
           SearchException: Si recherche échoue
           
       Example:
           >>> results = tracker.search_article("souris gamer")
           >>> print(f"Trouvé {len(results)} résultats")
       """
   ```

4. **Logging**:
   ```python
   from logger import logger
   
   logger.info("Action réussie")
   logger.warning("Avertissement")
   logger.error("Erreur", exc_info=True)  # Avec traceback
   ```

5. **Gestion d'erreurs**:
   ```python
   try:
       result = self.dangerous_operation()
   except SpecificException as e:
       logger.error(f"Erreur spécifique: {e.message}")
       raise
   except Exception as e:
       logger.error(f"Erreur inattendue: {e}", exc_info=True)
       raise
   ```

6. **Imports organisés**:
   ```python
   # 1. Stdlib
   import tkinter as tk
   from typing import Dict, List, Any
   import logging
   
   # 2. Third-party
   import requests
   from bs4 import BeautifulSoup
   
   # 3. Local
   from config import ui_config
   from logger import logger
   ```

#### Tests

Ajoutez des tests pour votre code:

```python
# tests/test_ma_feature.py
import pytest
from ma_feature import ma_fonction

def test_ma_fonction_succes():
    """Test cas de succès"""
    assert ma_fonction("input") == "expected_output"

def test_ma_fonction_erreur():
    """Test cas d'erreur"""
    with pytest.raises(ValueError):
        ma_fonction("")
```

Lancer les tests:
```bash
pytest tests/
```

#### Commits

**Messages de commit clairs**:

```
# Format
type(scope): description courte

type peut être:
- feat: Nouvelle feature
- fix: Correction de bug
- docs: Documentation
- style: Formatage (pas de logique)
- refactor: Restructuration code
- test: Tests
- chore: Configuration, dépendances

scope: Partie du code affectée
description: Brève description (imperativ)

Exemples:
feat(search): ajouter filtrage par budget
fix(ai): corriger détection profil utilisateur
docs(readme): ajouter section installation
```

**Bonnes pratiques**:
- Commits logiques (une feature = plusieurs commits logiques)
- Messages clairs et concis
- Commits fréquents (pas de megacommit)

#### Pull Request

1. **Avant de pushcher**:
   ```bash
   # Vérifiez la syntaxe
   python -m py_compile *.py
   
   # Testez
   python amazon_tracker.py
   ```

2. **Créez le PR**:
   - Titre clair et concis
   - Description détaillée de ce qui change
   - Références les issues (fixes #123)
   - Screenshots si GUI change

3. **Template PR**:
   ```markdown
   ## Description
   Qu'est-ce que ce PR change?

   ## Type de changement
   - [ ] Bug fix
   - [ ] Nouvelle feature
   - [ ] Changement qui casse la compatibilité
   - [ ] Documentation

   ## Comment tester
   Pas à pas pour vérifier:
   1. Lancez app
   2. Allez sur...
   3. Vérifiez que...

   ## Checklist
   - [ ] Type hints ajoutés
   - [ ] Docstrings complètes
   - [ ] Tests ajoutés
   - [ ] Aucun import inutilisé
   - [ ] PEP 8 respecté
   - [ ] Logging approprié
   ```

4. **Répondez aux reviews**:
   - Restez respectueux
   - Acceptez les critiques constructives
   - Faites les changements demandés
   - Re-demandez une review


## Standards de Qualité

### Checklist avant de soumettre

- [ ] **Type Hints**: Tous les paramètres et retours sont typés
- [ ] **Docstrings**: Toutes les functions/classes documentées
- [ ] **Tests**: Coverage > 80%
- [ ] **Logs**: Logging approprié (pas de print())
- [ ] **Erreurs**: Gestion d'erreurs robuste
- [ ] **Performance**: Pas de boucles infinies, opérations rapides
- [ ] **Sécurité**: Input validation, sanitization
- [ ] **Code**: PEP 8, cohérent avec le reste
- [ ] **Git**: Commits logiques et clairs
- [ ] **Docs**: Mise à jour documentations si nécessaire

### Outils de qualité (optionnel)

```bash
# Formatter automatique
pip install black
black *.py

# Linter
pip install pylint
pylint --disable=all --enable=E,F *.py

# Type checking
pip install mypy
mypy *.py

# Complexité
pip install radon
radon cc *.py -a
```

### Métriques acceptées

```
Complexité cyclomatique: < 10 par fonction
Couverture tests: > 80%
Longueur ligne: max 88 caractères
Longueur fonction: max 50 lignes (idéalement < 30)
```


## Processus de Review

### Critères de review

Le mainteneur vérifiera:
1. Qualité du code
2. Tests adéquats
3. Documentation complète
4. Performance
5. Sécurité
6. Alignement avec le projet

### Feedbacks possibles

- **Approved** ✅: Prêt à merger
- **Changes Requested** 🔄: Modifications nécessaires
- **Comment**: Question ou suggestion (pas bloquant)

### Après approval

- Le mainteneur merge le PR
- Votre commit est dans la branche principale
- Remerciements sincères! 🎉


## Dépannage

### Erreurs couantes

**Q: "Permission denied" sur git**
```bash
# Générez une clé SSH
ssh-keygen -t ed25519 -C "votre_email@example.com"
# Puis ajoutez-la sur GitHub
```

**Q: Changements pas appliqués**
```bash
# Assurez-vous sur la bonne branche
git branch -a

# Ou créez une nouvelle
git checkout -b feature/ma-feature
```

**Q: Conflit de merge**
```bash
# Voyez les conflits
git status

# Résolvez-les manuellement
# Puis committez
git add .
git commit -m "Résolution conflit merge"
```

**Q: Besoin de revenir en arrière**
```bash
# Annulez dernier commit (local)
git reset --soft HEAD~1

# Annulez et supprimez changements
git reset --hard HEAD~1
```


## Communication

- **Issues**: Pour bugs et features
- **Discussions**: Pour questions générales
- **Email**: [email-du-mainteneur@example.com]

## Reconnaissance

Tous les contributeurs sont reconnus dans:
- [CONTRIBUTORS.md](CONTRIBUTORS.md)
- Release notes
- README.md

## Licence

En contribuant, vous acceptez que votre code soit sous licence MIT.

---

**Merci de contribuer! Ensemble on fait un meilleur produit. 🚀**
