"""
support_ui.py - Interface utilisateur pour le support client

Permet aux utilisateurs de créer des tickets d'assistance directement
depuis l'application.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import logging
from typing import Optional, Callable
from datetime import datetime
from support import ticket_manager, ticket_notifier, SupportTicket

logger = logging.getLogger("amazon_tracker.support_ui")


class SupportWindow:
    """Fenêtre de support client."""
    
    # Couleurs
    BG_DARK = "#1a1a1a"
    BG_MEDIUM = "#2d2d2d"
    BG_LIGHT = "#3a3a3a"
    FG_TEXT = "#ffffff"
    ACCENT_COLOR = "#FF9900"
    SUCCESS_COLOR = "#00AA00"
    ERROR_COLOR = "#FF0000"
    
    def __init__(self, parent: tk.Widget, email: str = ""):
        """Initialise la fenêtre support.
        
        Args:
            parent: Widget parent
            email: Email de l'utilisateur
        """
        self.parent = parent
        self.user_email = email
        self.window: Optional[tk.Toplevel] = None
        self.selected_category = tk.StringVar(value="bug")
        self.selected_priority = tk.StringVar(value="medium")
    
    def show(self) -> None:
        """Affiche la fenêtre de support."""
        # Créer la fenêtre
        self.window = tk.Toplevel(self.parent)
        self.window.title("Support Client - Créer un Ticket")
        self.window.geometry("700x600")
        self.window.configure(bg=self.BG_DARK)
        
        # Icône (si disponible)
        try:
            self.window.iconbitmap('default')
        except:
            pass
        
        # Frame principal
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Titre
        title = ttk.Label(
            main_frame,
            text="CRÉER UN TICKET D'ASSISTANCE",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=(0, 20))
        
        # Email
        self._create_field(main_frame, "Email:", self.user_email, "email_entry")
        
        # Titre du problème
        self._create_field(main_frame, "Titre du problème:", "", "title_entry")
        
        # Catégorie
        self._create_category_field(main_frame)
        
        # Priorité
        self._create_priority_field(main_frame)
        
        # Description
        self._create_description_field(main_frame)
        
        # Boutons
        self._create_buttons(main_frame)
    
    def _create_field(
        self,
        parent: tk.Widget,
        label: str,
        default: str,
        var_name: str
    ) -> None:
        """Crée un champ de texte."""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=(0, 15))
        
        # Label
        ttk.Label(frame, text=label).pack(anchor=tk.W)
        
        # Entry
        entry = ttk.Entry(frame)
        entry.pack(fill=tk.X, pady=(5, 0))
        entry.insert(0, default)
        
        # Sauvegarder
        setattr(self, var_name, entry)
    
    def _create_category_field(self, parent: tk.Widget) -> None:
        """Crée le champ catégorie."""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(frame, text="Catégorie:").pack(anchor=tk.W)
        
        options = ["bug", "feature", "crash", "performance", "other"]
        combo = ttk.Combobox(
            frame,
            textvariable=self.selected_category,
            values=options,
            state="readonly",
            width=20
        )
        combo.pack(anchor=tk.W, pady=(5, 0))
        
        self.category_combo = combo
    
    def _create_priority_field(self, parent: tk.Widget) -> None:
        """Crée le champ priorité."""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(frame, text="Priorité:").pack(anchor=tk.W)
        
        options = ["low", "medium", "high", "critical"]
        combo = ttk.Combobox(
            frame,
            textvariable=self.selected_priority,
            values=options,
            state="readonly",
            width=20
        )
        combo.pack(anchor=tk.W, pady=(5, 0))
        
        self.priority_combo = combo
    
    def _create_description_field(self, parent: tk.Widget) -> None:
        """Crée le champ description."""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        ttk.Label(frame, text="Description:").pack(anchor=tk.W)
        
        text = scrolledtext.ScrolledText(
            frame,
            height=10,
            width=70,
            wrap=tk.WORD
        )
        text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        self.description_text = text
    
    def _create_buttons(self, parent: tk.Widget) -> None:
        """Crée les boutons."""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=(10, 0))
        
        # Bouton créer
        create_btn = ttk.Button(
            frame,
            text="Créer le Ticket",
            command=self._submit_ticket
        )
        create_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Bouton mes tickets
        tickets_btn = ttk.Button(
            frame,
            text="Mes Tickets",
            command=self._show_my_tickets
        )
        tickets_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Bouton fermer
        close_btn = ttk.Button(
            frame,
            text="Fermer",
            command=self._close_window
        )
        close_btn.pack(side=tk.LEFT)
    
    def _submit_ticket(self) -> None:
        """Soumet le ticket."""
        try:
            # Récupérer les valeurs
            email = self.email_entry.get().strip()
            title = self.title_entry.get().strip()
            category = self.selected_category.get()
            priority = self.selected_priority.get()
            description = self.description_text.get("1.0", tk.END).strip()
            
            # Validation
            if not email:
                messagebox.showerror("Erreur", "Veuillez entrer votre email")
                return
            
            if not title:
                messagebox.showerror("Erreur", "Veuillez entrer un titre")
                return
            
            if not description:
                messagebox.showerror("Erreur", "Veuillez décrire votre problème")
                return
            
            # Créer le ticket
            ticket_id = ticket_manager.create_ticket(
                title=title,
                description=description,
                category=category,
                priority=priority,
                user_email=email
            )
            
            # Notifier
            ticket = ticket_manager.get_ticket(ticket_id)
            if ticket:
                ticket_notifier.notify(ticket)
            
            # Message de succès
            message = f"""Ticket créé avec succès!

ID du Ticket: {ticket_id}
Email de confirmation: {email}

Votre demande a été enregistrée.
Notre équipe support vous contactera dès que possible.
"""
            messagebox.showinfo("Succès", message)
            
            logger.info(f"Ticket {ticket_id} created by {email}")
            
            # Effacer le formulaire
            self.title_entry.delete(0, tk.END)
            self.description_text.delete("1.0", tk.END)
            self.selected_category.set("bug")
            self.selected_priority.set("medium")
        
        except Exception as e:
            logger.error(f"Error creating ticket: {e}")
            messagebox.showerror("Erreur", f"Erreur: {str(e)}")
    
    def _show_my_tickets(self) -> None:
        """Affiche les tickets de l'utilisateur."""
        try:
            email = self.email_entry.get().strip()
            if not email:
                messagebox.showwarning("Attention", "Veuillez entrer votre email")
                return
            
            # Récupérer les tickets
            tickets = ticket_manager.list_tickets(email=email)
            
            if not tickets:
                messagebox.showinfo("Mes Tickets", "Vous n'avez pas de ticket")
                return
            
            # Créer une fenêtre pour afficher
            tickets_window = tk.Toplevel(self.window)
            tickets_window.title("Mes Tickets")
            tickets_window.geometry("800x600")
            tickets_window.configure(bg=self.BG_DARK)
            
            # Frame avec scrollbar
            frame = ttk.Frame(tickets_window)
            frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Canvas avec scrollbar
            canvas = tk.Canvas(frame, bg=self.BG_MEDIUM, highlightthickness=0)
            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Afficher chaque ticket
            for ticket in tickets:
                self._display_ticket_item(scrollable_frame, ticket)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
        
        except Exception as e:
            logger.error(f"Error showing tickets: {e}")
            messagebox.showerror("Erreur", f"Erreur: {str(e)}")
    
    def _display_ticket_item(self, parent: tk.Widget, ticket: SupportTicket) -> None:
        """Affiche un ticket dans la liste."""
        # Frame pour le ticket
        item_frame = ttk.Frame(parent, relief=tk.RAISED, borderwidth=1)
        item_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Contenu
        info_text = f"{ticket.ticket_id} | {ticket.title}"
        status_color = self._get_status_color(ticket.status)
        
        ttk.Label(
            item_frame,
            text=f"{ticket.ticket_id} - {ticket.title}",
            font=("Arial", 10, "bold")
        ).pack(anchor=tk.W, padx=10, pady=(5, 0))
        
        ttk.Label(
            item_frame,
            text=f"Status: {ticket.status} | Priorité: {ticket.priority} | Catégorie: {ticket.category}"
        ).pack(anchor=tk.W, padx=10, pady=0)
        
        ttk.Label(
            item_frame,
            text=f"Créé: {ticket.created_at[:10]} | Mis à jour: {ticket.updated_at[:10]}"
        ).pack(anchor=tk.W, padx=10, pady=(0, 5))
    
    def _get_status_color(self, status: str) -> str:
        """Retourne la couleur selon le statut."""
        colors = {
            "open": "#FF6666",
            "in_progress": "#FF9900",
            "resolved": "#00AA00",
            "closed": "#666666"
        }
        return colors.get(status, "#FFFFFF")
    
    def _close_window(self) -> None:
        """Ferme la fenêtre."""
        if self.window:
            self.window.destroy()


def show_support_window(parent: tk.Widget, email: str = "") -> None:
    """Affiche la fenêtre de support.
    
    Args:
        parent: Widget parent
        email: Email de l'utilisateur
    """
    support_window = SupportWindow(parent, email)
    support_window.show()
