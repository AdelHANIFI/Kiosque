from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import requests  # Pour gérer le paiement via l'API myPOS

class ZakatPage(QWidget):
    def __init__(self, parent=None, payment_page=None, translations=None, current_language="fr"):
        super().__init__(parent)
        # Stocker les traductions et la langue courante
        self.translations = translations if translations is not None else {}
        self.current_language = current_language
        self.payment_page = payment_page

        # Créer le layout principal
        layout = QVBoxLayout()

        # Titre de la page
        title_text = self.translations.get(self.current_language, {}).get("zakat_title", "Zakât al-Fitr")
        self.title = QLabel(title_text)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont("Arial", 60, QFont.Bold))  # Taille du titre augmentée

        # Message explicatif
        explanation_text = self.translations.get(self.current_language, {}).get(
            "zakat_explanation", 
            "La Zakât al-Fitr est fixée à 7 € par personne.\nVeuillez appuyer sur le bouton ci-dessous pour la payer."
        )
        self.explanation = QLabel(explanation_text)
        self.explanation.setAlignment(Qt.AlignCenter)
        self.explanation.setFont(QFont("Arial", 25))

        # Bouton pour payer la Zakât al-Fitr
        zakat_button_text = self.translations.get(self.current_language, {}).get("zakat", "Payer 7 €")
        self.zakat_button = QPushButton(zakat_button_text)
        self.zakat_button.setFont(QFont("Arial", 40, QFont.Bold))
        self.zakat_button.setFixedSize(300, 300)
        self.zakat_button.setStyleSheet("""
            QPushButton {
                border: 2px solid #2b8c8c;
                border-radius: 150px; /* Bouton circulaire */
                background-color: #e8f8f8;
                color: #2b8c8c;
            }
            QPushButton:hover {
                background-color: #d1f1f1;
            }
            QPushButton:pressed {
                background-color: #a8e4e4;
            }
        """)
        self.zakat_button.clicked.connect(lambda _, m=7: self.navigate_to_payment(m))

        # Ajout des widgets en haut de la page
        layout.addWidget(self.title)
        layout.addWidget(self.explanation)
        layout.addWidget(self.zakat_button, alignment=Qt.AlignCenter)

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
        self.back_button.clicked.connect(self.return_to_previous_page)
        layout.addWidget(self.back_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def update_translations(self, translations, current_language):
        """
        Met à jour les textes de la page selon la langue sélectionnée.
        """
        self.translations = translations
        self.current_language = current_language

        self.title.setText(
            self.translations.get(current_language, {}).get("zakat_title", "Zakât al-Fitr")
        )
        self.explanation.setText(
            self.translations.get(current_language, {}).get(
                "zakat_explanation",
                "La Zakât al-Fitr est fixée à 7 € par personne.\nVeuillez appuyer sur le bouton ci-dessous pour la payer."
            )
        )
        self.zakat_button.setText(
            self.translations.get(current_language, {}).get("zakat", "Payer 7 €")
        )
        self.back_button.setText(
            self.translations.get(current_language, {}).get("back", "Retour")
        )

    def navigate_to_payment(self, montant):
        """Navigue vers la page de paiement et initie le paiement."""
        if self.payment_page:
            self.payment_page.set_amount(montant)
            self.payment_page.initiate_payment(montant,'zakat')  # Appelle la méthode d'initiation de paiement
            parent = self.parent()
            if parent:
                parent.setCurrentIndex(2)
    def return_to_previous_page(self):
        """
        Retourne à la page précédente.
        """
        parent = self.parent()
        if parent:
            parent.setCurrentIndex(0)  # Retourne à la page d'accueil ou précédente
