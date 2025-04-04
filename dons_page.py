from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout, QSpacerItem, QSizePolicy
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import requests

class DonsPage(QWidget):
    def __init__(self, parent=None, payment_page=None, translations=None, current_language="fr"):
        super().__init__(parent)
        self.payment_page = payment_page
        self.translations = translations if translations is not None else {}
        self.current_language = current_language
        
        # Clés de traduction à utiliser (à définir dans votre dictionnaire de traductions)
        # Par exemple, nous utiliserons "mosque" pour le titre et "mosque_help" pour le texte explicatif.
        
        # Configuration de l'API SumUp (non liée aux traductions)
        self.sumup_api_key = "sup_sk_YkWjlUS5edcb0LAVsObRwsJXJu9dMyH6o"
        self.merchant_code = "MFT77XNQ"
        self.pairing_code = "EZRVUID3R"
        
        # Layout principal
        layout = QVBoxLayout()
        
        # Titre de la page
        self.title = QLabel(self.translations.get(self.current_language, {}).get("mosque", "Dons pour la Mosquée"))
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont("Arial", 60, QFont.Bold))
        
        # Message explicatif
        self.explanation = QLabel(self.translations.get(self.current_language, {}).get("mosque_help", "Choisissez un montant à donner pour soutenir la mosquée."))
        self.explanation.setAlignment(Qt.AlignCenter)
        self.explanation.setFont(QFont("Arial", 25))
        
        layout.addWidget(self.title)
        layout.addWidget(self.explanation)
        
        # Layout pour les montants (en grille)
        buttons_layout = QGridLayout()
        buttons_layout.setHorizontalSpacing(50)
        buttons_layout.setVerticalSpacing(50)
        
        # Montants prédéfinis
        amounts = [5, 10, 20, 50, 100]
        row = 0
        col = 0
        max_columns = 3
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
            # On passe le montant en paramètre grâce à une fonction lambda
            button.clicked.connect(lambda _, m=montant: self.navigate_to_payment(m))
        
        # Bouton "Autre montant"
        other_amount_text = self.translations.get(self.current_language,  {}).get("other amount", "autre montant")
        self.other_amount_button = QPushButton("Autre\nmontant")
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
        buttons_layout.addWidget(self.other_amount_button, row, col, Qt.AlignCenter)
        self.other_amount_button.clicked.connect(lambda: self.go_to_other_amount_page('sadaqa'))
        
        layout.addLayout(buttons_layout)
        layout.addSpacerItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        #         # Bouton "Payer la Zakat al-Fitr (7 €)" (agrandi)
        # self.zakat_button = QPushButton(
        #     self.translations.get(self.current_language, {}).get("zakat_button", "Payer la Zakat al-Fitr (7 €)")
        # )
        # self.zakat_button.setFont(QFont("Arial", 22))
        # self.zakat_button.clicked.connect(self.handle_zakat)
        # layout.addWidget(self.zakat_button, alignment=Qt.AlignBottom)
        # Bouton retour
        back_text = self.translations.get(self.current_language, {}).get("back", "Retour")
        self.back_button = QPushButton(back_text)
        self.back_button.setFont(QFont("Arial", 22, QFont.Bold))
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
            self.translations.get(current_language, {}).get("mosque", "Travaux de la Mosquée")
        )
        self.explanation.setText(
            self.translations.get(current_language, {}).get("mosque_help", "Choisissez un montant à donner pour soutenir les travaux de la mosquée.")
        )
        self.other_amount_button.setText(
            self.translations.get(current_language, {}).get("other_amount", "Autre\nmontant")
        )
        self.back_button.setText(
            self.translations.get(current_language, {}).get("back", "Retour")
        )
        # self.zakat_button.setText(
        #     self.translations.get(current_language, {}).get("zakat_button", "Payer la Zakat al-Fitr (7 €)")
        # )
   
    def navigate_to_payment(self, montant):
        """Navigue vers la page de paiement et initie le paiement."""
        if self.payment_page:
            self.payment_page.set_amount(montant)
            self.payment_page.initiate_payment(montant,'sadaqa')  # Appelle la méthode d'initiation de paiement
            parent = self.parent()
            if parent:
                parent.setCurrentIndex(2)

    def return_to_home(self):
        """Retourne à la page d'accueil."""
        parent = self.parent()
        if parent:
            parent.setCurrentIndex(0)
    def handle_zakat(self):
        """
        Navigue vers la page de paiement de la Zakat.
        """
        parent = self.parent()
        if parent:
            parent.setCurrentIndex(parent.indexOf(parent.parent().zakat_page))
    def go_to_other_amount_page(self, donation_type):
        """Navigue vers la page 'Autre montant' avec le type de don spécifié."""
        main_app = self.window()  # Accède à la fenêtre principale
        if hasattr(main_app, "otheramount_page"):
            main_app.otheramount_page.set_donation_type(donation_type)
            main_app.pages.setCurrentWidget(main_app.otheramount_page)


