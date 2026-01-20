"""
amazon_tracker_mobile.py - Version Kivy pour Android/iOS

Application de suivi Amazon Tracker compatible mobile (Android & iOS)
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.uix.image import Image
import json
import os
from datetime import datetime

# Définir la taille de la fenêtre
Window.size = (500, 800)


class AmazonTrackerMobileApp(App):
    """Application mobile Amazon Tracker"""
    
    def build(self):
        """Construit l'interface Kivy"""
        self.title = "🛒 Amazon Tracker Pro"
        
        # Layout principal
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Titre
        title_label = Label(
            text="[b]🛒 Amazon Tracker Pro[/b]",
            markup=True,
            size_hint_y=0.08,
            font_size='20sp'
        )
        main_layout.add_widget(title_label)
        
        # Zone de recherche
        search_layout = BoxLayout(orientation='vertical', size_hint_y=0.15, spacing=5)
        search_layout.add_widget(Label(text="Rechercher un article:", size_hint_y=0.3))
        
        self.search_input = TextInput(
            multiline=False,
            hint_text="Entrez un produit...",
            size_hint_y=0.7
        )
        search_layout.add_widget(self.search_input)
        main_layout.add_widget(search_layout)
        
        # Boutons de recherche
        search_button_layout = BoxLayout(size_hint_y=0.1, spacing=5)
        search_button_layout.add_widget(
            Button(text="🔍 Rechercher", on_press=self.search_product)
        )
        search_button_layout.add_widget(
            Button(text="💬 Support", on_press=self.open_support)
        )
        main_layout.add_widget(search_button_layout)
        
        # Zone de résultats
        results_label = Label(text="Résultats / Articles suivis:", size_hint_y=0.05)
        main_layout.add_widget(results_label)
        
        scroll_view = ScrollView(size_hint_y=0.65)
        self.results_layout = GridLayout(
            cols=1,
            spacing=10,
            size_hint_y=None,
            padding=5
        )
        self.results_layout.bind(minimum_height=self.results_layout.setter('height'))
        scroll_view.add_widget(self.results_layout)
        main_layout.add_widget(scroll_view)
        
        # Boutons d'action
        action_layout = BoxLayout(size_hint_y=0.15, spacing=5)
        action_layout.add_widget(
            Button(text="📋 Mes Articles", on_press=self.show_tracked_articles)
        )
        action_layout.add_widget(
            Button(text="📊 Logs", on_press=self.show_logs)
        )
        action_layout.add_widget(
            Button(text="⚙️ Config", on_press=self.open_settings)
        )
        main_layout.add_widget(action_layout)
        
        return main_layout
    
    def search_product(self, instance):
        """Recherche un produit"""
        search_term = self.search_input.text.strip()
        
        if not search_term:
            self.show_popup("Erreur", "Veuillez entrer un terme de recherche")
            return
        
        # Simuler une recherche
        self.results_layout.clear_widgets()
        
        result_label = Label(
            text=f"[b]Recherche:[/b] {search_term}\n[i]Connexion au serveur...[/i]",
            markup=True,
            size_hint_y=None,
            height=100
        )
        self.results_layout.add_widget(result_label)
        
        self.show_popup(
            "✅ Recherche lancée",
            f"Recherche de: {search_term}\n\nLes résultats apparaîtront ici"
        )
    
    def show_tracked_articles(self, instance):
        """Affiche les articles suivis"""
        self.results_layout.clear_widgets()
        
        # Charger les articles suivis
        try:
            with open('articles_tracked.json', 'r', encoding='utf-8') as f:
                articles = json.load(f)
                
                if isinstance(articles, list):
                    count = 0
                    for article in articles[:5]:  # Afficher les 5 premiers
                        article_label = Label(
                            text=f"[b]{article.get('name', 'Sans nom')}[/b]\nPrix: {article.get('price', 'N/A')}",
                            markup=True,
                            size_hint_y=None,
                            height=80
                        )
                        self.results_layout.add_widget(article_label)
                        count += 1
                    
                    if len(articles) > 5:
                        more_label = Label(
                            text=f"... et {len(articles) - 5} articles supplémentaires",
                            size_hint_y=None,
                            height=50
                        )
                        self.results_layout.add_widget(more_label)
                    
                    self.show_popup(
                        "📋 Articles suivis",
                        f"Total: {len(articles)} articles"
                    )
        except Exception as e:
            self.show_popup("Erreur", f"Impossible de charger les articles: {e}")
    
    def show_logs(self, instance):
        """Affiche les logs d'activité"""
        try:
            with open('activity_logs.json', 'r', encoding='utf-8') as f:
                logs = json.load(f)
                
                if isinstance(logs, list):
                    recent_logs = logs[-10:] if len(logs) > 10 else logs
                    
                    self.results_layout.clear_widgets()
                    
                    for log in reversed(recent_logs):
                        log_label = Label(
                            text=f"[b]{log.get('action', 'action')}[/b]\n{log.get('user', 'unknown')}\n{log.get('timestamp', '')[:10]}",
                            markup=True,
                            size_hint_y=None,
                            height=80
                        )
                        self.results_layout.add_widget(log_label)
                    
                    self.show_popup(
                        "📊 Logs d'activité",
                        f"Affichage des {len(recent_logs)} dernières activités"
                    )
        except Exception as e:
            self.show_popup("Erreur", f"Impossible de charger les logs: {e}")
    
    def open_support(self, instance):
        """Ouvre le formulaire de support"""
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        popup_layout.add_widget(Label(text="Créer un Ticket de Support", size_hint_y=0.1))
        
        email_input = TextInput(
            hint_text="Votre email",
            multiline=False,
            size_hint_y=0.15
        )
        popup_layout.add_widget(email_input)
        
        title_input = TextInput(
            hint_text="Titre du problème",
            multiline=False,
            size_hint_y=0.15
        )
        popup_layout.add_widget(title_input)
        
        description_input = TextInput(
            hint_text="Description détaillée",
            multiline=True,
            size_hint_y=0.3
        )
        popup_layout.add_widget(description_input)
        
        button_layout = BoxLayout(size_hint_y=0.15, spacing=5)
        
        def submit_support():
            if not email_input.text or not title_input.text:
                self.show_popup("Erreur", "Veuillez remplir tous les champs")
                return
            
            self.show_popup(
                "✅ Ticket créé",
                f"ID: TKT-{datetime.now().strftime('%Y%m%d%H%M%S')}\nVotre demande a été enregistrée"
            )
            popup.dismiss()
        
        button_layout.add_widget(Button(text="Envoyer", on_press=lambda x: submit_support()))
        button_layout.add_widget(Button(text="Annuler", on_press=lambda x: popup.dismiss()))
        
        popup_layout.add_widget(button_layout)
        
        popup = Popup(
            title="💬 Support",
            content=popup_layout,
            size_hint=(0.9, 0.8)
        )
        popup.open()
    
    def open_settings(self, instance):
        """Ouvre les paramètres"""
        settings_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        settings_layout.add_widget(Label(
            text="[b]⚙️ Paramètres[/b]",
            markup=True,
            size_hint_y=0.1
        ))
        
        settings_layout.add_widget(Label(
            text="Version: 1.0.0\nPlatform: Kivy Mobile",
            size_hint_y=0.2
        ))
        
        settings_layout.add_widget(Label(
            text="Discord Webhook:",
            size_hint_y=0.1
        ))
        
        discord_input = TextInput(
            hint_text="Coller l'URL du webhook",
            multiline=False,
            size_hint_y=0.15
        )
        settings_layout.add_widget(discord_input)
        
        button_layout = BoxLayout(size_hint_y=0.15, spacing=5)
        button_layout.add_widget(Button(text="Sauvegarder"))
        button_layout.add_widget(Button(text="Fermer", on_press=lambda x: popup.dismiss()))
        
        settings_layout.add_widget(button_layout)
        
        popup = Popup(
            title="Paramètres",
            content=settings_layout,
            size_hint=(0.9, 0.7)
        )
        popup.open()
    
    def show_popup(self, title, message):
        """Affiche une popup de message"""
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_layout.add_widget(Label(text=message))
        popup_layout.add_widget(Button(
            text="OK",
            size_hint_y=0.3,
            on_press=lambda x: popup.dismiss()
        ))
        
        popup = Popup(
            title=title,
            content=popup_layout,
            size_hint=(0.8, 0.6)
        )
        popup.open()


if __name__ == '__main__':
    app = AmazonTrackerMobileApp()
    app.run()
