from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QSpacerItem, QSizePolicy
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import requests

class WorksPage(QWidget):
    def __init__(self, parent=None, payment_page=None, translations=None, current_language="fr"):
        super().__init__(parent)
        # Stocker le dictionnaire de traductions et la langue courante
        self.translations = translations if translations is not None else {}
        self.current_language = current_language
        self.payment_page = payment_page

        # Initialisation de l'interface
        self.setup_ui()
    
    def setup_ui(self):
        # Layout principal
        layout = QVBoxLayout()

        # Titre de la page
        title_text = self.translations.get(self.current_language, {}).get(
            "works", "Travaux de la Mosquée"
        )
        self.title = QLabel(title_text)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont("Arial", 60, QFont.Bold))  # Taille du titre augmentée

        # Message explicatif
        explanation_text = self.translations.get(self.current_language, {}).get(
            "works_help", "Choisissez un montant à donner pour soutenir les travaux de la mosquée."
        )
        self.explanation = QLabel(explanation_text)
        self.explanation.setAlignment(Qt.AlignCenter)
        self.explanation.setFont(QFont("Arial", 25))

        # Layout pour les montants (en grille)
        buttons_layout = QGridLayout()
        buttons_layout.setHorizontalSpacing(50)  # Espacement horizontal entre les boutons
        buttons_layout.setVerticalSpacing(50)    # Espacement vertical entre les boutons

        # Montants prédéfinis
        amounts = [5, 10, 20, 50, 100]
        row = 0
        col = 0
        max_columns = 3  # Nombre maximum de colonnes par ligne
        for montant in amounts:
            button = QPushButton(f"{montant} €")
            button.setFont(QFont("Arial", 60, QFont.Bold))
            button.setFixedSize(350, 350)
            button.setStyleSheet(f"""
                QPushButton {{
                    border: 2px solid #2b8c8c;
                    border-radius: 175px; /* Bords arrondis pour un cercle */
                    background-color: #e8f8f8;
                    color: #2b8c8c;
                }}
                QPushButton:hover {{
                    background-color: #d1f1f1;
                }}
                QPushButton:pressed {{
                    background-color: #a8e4e4;
                }}
            """)
            buttons_layout.addWidget(button, row, col, Qt.AlignCenter)
            col += 1
            if col == max_columns:  # Passage à la ligne suivante après max_columns boutons
                col = 0
                row += 1
            button.clicked.connect(lambda _, m=montant: self.navigate_to_payment(m))

        # Bouton "Autre montant"
        other_amount_text = self.translations.get(self.current_language, {}).get(
            "other_amount", "Autre\nmontant"
        )
        self.other_amount_button = QPushButton(other_amount_text)
        self.other_amount_button.setFont(QFont("Arial", 40, QFont.Bold))
        self.other_amount_button.setFixedSize(350, 350)
        self.other_amount_button.setStyleSheet("""
            QPushButton {
                border: 2px solid #2b8c8c;
                border-radius: 175px; /* Bords arrondis pour un cercle */
                background-color: #ffe6e0;
                color: #2b8c8c;
            }
            QPushButton:hover {
                background-color: #ffd6cc;
            }
            QPushButton:pressed {
                background-color: #ffc2b3;
            }
        """)
        self.other_amount_button.clicked.connect(lambda: self.go_to_other_amount_page('travaux'))
        buttons_layout.addWidget(self.other_amount_button, row, col, Qt.AlignCenter)

        # Ajouter un espacement flexible avant le bouton retour
        layout.addWidget(self.title)
        layout.addWidget(self.explanation)
        layout.addLayout(buttons_layout)
        layout.addSpacerItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Bouton retour
        back_text = self.translations.get(self.current_language, {}).get("back", "Retour")
        self.back_button = QPushButton(back_text)
        self.back_button.setFont(QFont("Arial", 22, QFont.Bold))  # Police plus grande pour "Retour"
        self.back_button.setMinimumHeight(60)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #f9f9f9;
                border: 2px solid #2b8c8c;
                border-radius: 10px;
                color: #2b8c8c;
            }
            QPushButton:hover {
                background-color: #e0f7f7;
            }
            QPushButton:pressed {
                background-color: #b0d6d6;
            }
        """)
        self.back_button.clicked.connect(self.return_to_home)
        layout.addWidget(self.back_button, alignment=Qt.AlignBottom)

        self.setLayout(layout)

    def update_translations(self, translations, current_language):
        """
        Met à jour les textes de la page Works selon la langue sélectionnée.
        """
        self.translations = translations
        self.current_language = current_language
        self.title.setText(
            self.translations.get(current_language, {}).get("works", "Travaux de la Mosquée")
        )
        self.explanation.setText(
            self.translations.get(current_language, {}).get("works_help", "Choisissez un montant à donner pour soutenir les travaux de la mosquée.")
        )
        self.other_amount_button.setText(
            self.translations.get(current_language, {}).get("other_amount", "Autre\nmontant")
        )
        self.back_button.setText(
            self.translations.get(current_language, {}).get("back", "Retour")
        )
    def navigate_to_payment(self, montant):
        """Navigue vers la page de paiement et initie le paiement."""
        if self.payment_page:
            self.payment_page.set_amount(montant)
            self.payment_page.initiate_payment(montant,'travaux')  # Appelle la méthode d'initiation de paiement
            parent = self.parent()
            if parent:
                parent.setCurrentIndex(2)
    def go_to_other_amount_page(self, donation_type):
        """Navigue vers la page 'Autre montant' avec le type de don spécifié."""
        main_app = self.window()  # Accède à la fenêtre principale
        if hasattr(main_app, "otheramount_page"):
            main_app.otheramount_page.set_donation_type(donation_type)
            main_app.pages.setCurrentWidget(main_app.otheramount_page)


    def return_to_home(self):
        """
        Retourne à la page d'accueil.
        """
        parent = self.parent()
        if parent:
            parent.setCurrentIndex(0)  # Affiche la page d'accueil
