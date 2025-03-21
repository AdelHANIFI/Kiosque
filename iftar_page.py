from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QSpacerItem, QSizePolicy
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import requests

class IftarPage(QWidget):
    def __init__(self, parent=None, payment_page = None, translations=None, current_language="fr"):
        super().__init__(parent)
        # Stocker les traductions et la langue courante
        self.translations = translations if translations is not None else {}
        self.current_language = current_language
        self.payment_page = payment_page

        # Layout principal
        layout = QVBoxLayout()

        # Titre de la page, utilisant la traduction (clé "iftar_title")
        self.title = QLabel(
            self.translations.get(self.current_language, {}).get("iftar_title", "Faire une Sadaqa pour l'Iftar")
        )
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont("Arial", 60, QFont.Bold))

        # Message explicatif, utilisant la traduction (clé "iftar_explanation")
        self.explanation = QLabel(
            self.translations.get(self.current_language, {}).get("iftar_explanation", "Choisir un montant à donner pour l'Iftar.")
        )
        self.explanation.setAlignment(Qt.AlignCenter)
        self.explanation.setFont(QFont("Arial", 25))

        # Layout pour les montants (en grille)
        buttons_layout = QGridLayout()
        buttons_layout.setHorizontalSpacing(50)
        buttons_layout.setVerticalSpacing(50)

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
                    border-radius: 175px;
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
            if col == max_columns:
                col = 0
                row += 1
            button.clicked.connect(lambda _, m=montant: self.navigate_to_payment(m))

        # Bouton "Autre montant"
        other_amount_text = self.translations.get(self.current_language, {}).get("other_amount", "Autre\nmontant")
        self.other_amount_button = QPushButton(other_amount_text)
        self.other_amount_button.setFont(QFont("Arial", 40, QFont.Bold))
        self.other_amount_button.setFixedSize(350, 350)
        self.other_amount_button.setStyleSheet("""
            QPushButton {
                border: 2px solid #2b8c8c;
                border-radius: 175px;
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
        self.other_amount_button.clicked.connect(lambda: self.go_to_other_amount_page('iftar'))
        buttons_layout.addWidget(self.other_amount_button, row, col, Qt.AlignCenter)

        # Ajouter les widgets principaux dans le layout
        layout.addWidget(self.title)
        layout.addWidget(self.explanation)
        layout.addLayout(buttons_layout)
        layout.addSpacerItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Bouton "Retour"
        self.back_button = QPushButton(
            self.translations.get(self.current_language, {}).get("back", "Retour")
        )
        self.back_button.setFont(QFont("Arial", 20))
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
        """)
        self.back_button.clicked.connect(self.return_to_previous_page)
        layout.addWidget(self.back_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def update_translations(self, translations, language):
        """
        Met à jour les textes de la page Iftar selon la langue sélectionnée.
        """
        self.translations = translations
        self.current_language = language
        self.title.setText(
            self.translations.get(language, {}).get("iftar_title", "Faire une Sadaqa pour l'Iftar")
        )
        self.explanation.setText(
            self.translations.get(language, {}).get("iftar_explanation", "Choisir un montant à donner pour l'Iftar.")
        )
        self.other_amount_button.setText(
        self.translations.get(language, {}).get("other_amount", "Autre\nmontant")
        )
        self.back_button.setText(
            self.translations.get(language, {}).get("back", "Retour")
        )

    def go_to_other_amount_page(self, donation_type):
        """Navigue vers la page 'Autre montant' avec le type de don spécifié."""
        main_app = self.window()  # Accède à la fenêtre principale
        if hasattr(main_app, "otheramount_page"):
            main_app.otheramount_page.set_donation_type(donation_type)
            main_app.pages.setCurrentWidget(main_app.otheramount_page)


    def return_to_previous_page(self):
        """
        Retourne à la page précédente.
        """
        parent = self.parent()
        if parent:
            parent.setCurrentIndex(0)  # Par exemple, l'index de la page d'accueil

    def navigate_to_payment(self, montant):
        """Navigue vers la page de paiement et initie le paiement."""
        if self.payment_page:
            self.payment_page.set_amount(montant)
            self.payment_page.initiate_payment(montant, 'iftar')  # Appelle la méthode d'initiation de paiement
            parent = self.parent()
            if parent:
                parent.setCurrentIndex(2)