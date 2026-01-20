"""
INTEGRATION_SUPPORT.md - Guide d'Intégration du Support Client

Guide pour intégrer le système de support client dans amazon_tracker.py
"""

# 🔗 GUIDE D'INTÉGRATION DU SUPPORT CLIENT

## Intégration dans amazon_tracker.py

### 1. Imports

Ajoutez ces imports au début du fichier `amazon_tracker.py`:

```python
# Support Client
from support_ui import show_support_window
from cloud_sync import cloud_sync
```

### 2. Bouton Support dans le Menu

Ajoutez un bouton "Support Client" dans votre interface tkinter:

```python
# Dans la création du menu principal
support_button = tk.Button(
    menu_frame,
    text="Support Client",
    bg=Config.ACCENT_COLOR,
    fg="black",
    font=("Arial", 10, "bold"),
    command=lambda: show_support_window(root, user_email="")
)
support_button.pack(side=tk.LEFT, padx=10, pady=10)
```

### 3. Avec Menu Bar

Ou dans une barre de menu:

```python
menubar = tk.Menu(root)
root.config(menu=menubar)

# Menu Aide
help_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Aide", menu=help_menu)
help_menu.add_command(
    label="Support Client",
    command=lambda: show_support_window(root)
)
help_menu.add_separator()
help_menu.add_command(label="À Propos", command=show_about)
```

### 4. Configuration Cloud au Démarrage

```python
def setup_cloud_sync():
    """Configure la synchronisation cloud au démarrage."""
    from cloud_sync import cloud_sync
    
    # Les configurations seront chargées depuis cloud_config.json
    logger.info(f"Cloud sync services: {list(cloud_sync.config.keys())}")

# Dans __init__:
setup_cloud_sync()
```

### 5. Exemple Complet

Voici un exemple complet d'intégration:

```python
# ==================== SUPPORT CLIENT ====================

from support_ui import show_support_window
from support import ticket_manager
from cloud_sync import cloud_sync
import logging

logger = logging.getLogger("amazon_tracker.main")

class AmazonTrackerApp:
    def __init__(self, root: tk.Tk) -> None:
        # ... initialisation existante ...
        
        # Setup support client
        self._setup_support_client()
    
    def _setup_support_client(self) -> None:
        """Configure le système de support client."""
        try:
            # Charger les configurations cloud
            logger.info("Initializing support client...")
            
            # Vérifier les fichiers de tickets
            tickets = ticket_manager.list_tickets()
            logger.info(f"Support: {len(tickets)} tickets en base")
            
            logger.info("Support client initialized successfully")
        
        except Exception as e:
            logger.error(f"Error initializing support client: {e}")
    
    def _create_menu_bar(self) -> None:
        """Crée la barre de menu avec support client."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Fichier
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Fichier", menu=file_menu)
        file_menu.add_command(label="Quitter", command=self.root.quit)
        
        # Menu Aide
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Aide", menu=help_menu)
        help_menu.add_command(
            label="Support Client",
            command=self._open_support
        )
        help_menu.add_separator()
        help_menu.add_command(label="À Propos", command=self._show_about)
    
    def _open_support(self) -> None:
        """Ouvre la fenêtre de support client."""
        show_support_window(self.root, user_email="")
    
    def _show_about(self) -> None:
        """Affiche l'à propos."""
        messagebox.showinfo(
            "À Propos",
            "Amazon Tracker Pro v1.0.0\n"
            "Avec support client intégré\n"
            "© 2026"
        )

# ==================== FIN SUPPORT CLIENT ====================
```

## Accès au Support par l'Utilisateur

### Depuis le Bouton Menu

1. L'utilisateur clique sur "Support Client"
2. Une fenêtre s'ouvre avec le formulaire
3. Il remplit ses informations
4. Clique "Créer le Ticket"

### Flux Complet

```
Utilisateur clique "Support"
        ↓
Fenêtre de support s'ouvre (support_ui.py)
        ↓
Utilisateur remplit le formulaire
        ↓
Clique "Créer le Ticket"
        ↓
Ticket créé (support.py)
Sauvegardé dans support_tickets.json
        ↓
Notifications envoyées vers:
  - Discord (si configuré)
  - Telegram (si configuré)
  - Google Sheets (si configuré)
  - Email (si configuré)
        ↓
Utilisateur peut voir son ticket
depuis "Mes Tickets"
```

## Configuration Avant de Lancer

### 1. Configuration Cloud (Optionnel mais Recommandé)

```bash
# Lancer le wizard de configuration
python setup_support.py
```

Cela ouvrira une interface pour configurer:
- Discord Webhook
- Telegram Bot
- Google Sheets
- Email SMTP

### 2. Vérifier la Configuration

```python
from cloud_sync import cloud_sync

print("Services configurés:")
for service in cloud_sync.config:
    print(f"  - {service}")
```

## Fichiers Nécessaires

| Fichier | Description | Essentiel |
|---------|-------------|-----------|
| support.py | Système de tickets | ✅ OUI |
| support_ui.py | Interface utilisateur | ✅ OUI |
| cloud_sync.py | Synchronisation cloud | ✅ OUI |
| setup_support.py | Configuration | ❌ NON (mais recommandé) |
| test_support.py | Tests | ❌ NON |
| SUPPORT_CLIENT.md | Documentation | ❌ NON |
| cloud_config.json | Configuration cloud | ❌ NON (créé par setup) |
| cloud_config.example.json | Exemple | ❌ NON |
| support_tickets.json | Base de tickets | ❌ Créé automatiquement |

## Minimalism pour Déploiement

Si vous voulez déployer la version minimale:

1. Copiez `support.py`
2. Copiez `support_ui.py`
3. Copiez `cloud_sync.py`
4. Intégrez dans `amazon_tracker.py`

C'est tout! Le système fonctionnera sans configuration cloud.

## Avec Configuration Cloud

1. Copiez les 3 fichiers ci-dessus
2. Copiez `setup_support.py`
3. Copiez `cloud_config.example.json` → `cloud_config.json`
4. Remplissez `cloud_config.json` avec vos clés
5. Intégrez dans `amazon_tracker.py`

## Dépannage

### Les tickets ne s'enregistrent pas

Vérifiez que le fichier `support_tickets.json` est créé:

```python
from pathlib import Path
exists = Path("support_tickets.json").exists()
print(f"Tickets file exists: {exists}")
```

### Les notifications cloud ne marchent pas

Vérifiez la configuration:

```python
from cloud_sync import cloud_sync

print("Configuration chargée:")
print(cloud_sync.config)
```

Les services non configurés seront simplement ignorés.

### Erreurs d'import

Si vous avez des erreurs d'import:

```bash
# Assurez-vous que tous les fichiers sont dans le même dossier
cd c:\Users\eisbr\Nouveau dossier

# Testez les imports
python -c "from support import ticket_manager"
python -c "from cloud_sync import cloud_sync"
python -c "from support_ui import SupportWindow"
```

## Points Importants

1. **Sauvegardes**: Les tickets sont sauvegardés dans `support_tickets.json`
2. **Synchronisation**: Les tickets sont aussi envoyés vers les services cloud configurés
3. **Offline-First**: L'app fonctionne même sans connexion (stockage local)
4. **Sécurité**: Ne partagez pas le fichier `cloud_config.json` avec des vrais secrets

## Support Additionnel

Consultez:
- `SUPPORT_CLIENT.md` - Guide utilisateur complet
- Logs dans `logs/amazon_tracker_*.log`
- `test_support.py` - Pour tester le système

---

**Version:** 1.0.0
**Date:** 2026-01-19
