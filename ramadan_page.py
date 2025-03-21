from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from dons_page import DonsPage

class RamadanPage(QWidget):
    def __init__(self, parent=None, translations=None, current_language="fr"):
        super().__init__(parent)
        # Stocker les traductions et la langue actuelle
        self.translations = translations if translations is not None else {}
        self.current_language = current_language

        self.setup_ui()
        self.apply_styles()
        # Exemple d'intégration d'une page interne (ici, la page des dons)
        self.pages = QStackedWidget()
        self.dons_page = DonsPage(self.pages)  # Vous pouvez également transmettre les traductions à DonsPage
        self.pages.addWidget(self.dons_page)

    def setup_ui(self):
        # Layout principal
        layout = QVBoxLayout()

        # Titre
        self.title = QLabel(
            self.translations.get(self.current_language, {}).get("ramadan_title", "Dons pour le Ramadan")
        )
        self.title.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.title.setFont(QFont("Arial", 50, QFont.Bold))

        # Bouton "Faire une Sadaqa pour l'Iftar"
        self.sadaqa_button = QPushButton(
            self.translations.get(self.current_language, {}).get("sadaqa_button", "Faire une Sadaqa pour l'Iftar")
        )
        self.sadaqa_button.setFont(QFont("Arial", 16))
        self.sadaqa_button.setFixedSize(400, 100)
        self.sadaqa_button.clicked.connect(self.go_to_sadaqa_page)

        # Bouton "Payer la Zakat al-Fitr (7 €)"
        self.zakat_button = QPushButton(
            self.translations.get(self.current_language, {}).get("zakat_button", "Payer la Zakat al-Fitr (7 €)")
        )
        self.zakat_button.setObjectName("zakatButton")
        self.zakat_button.setFixedSize(400, 100)
        self.zakat_button.clicked.connect(self.handle_zakat)

        # Bouton retour
        self.back_button = QPushButton(
            self.translations.get(self.current_language, {}).get("back", "Retour")
        )
        self.back_button.setObjectName("backButton")
        self.back_button.setFixedSize(200, 50)
        self.back_button.clicked.connect(self.return_to_home)

        # Ajouter les widgets au layout
        layout.addWidget(self.title)
        layout.addWidget(self.sadaqa_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.zakat_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.back_button, alignment=Qt.AlignBottom | Qt.AlignHCenter)

        self.setLayout(layout)

    def apply_styles(self):
        self.setStyleSheet("""
        QWidget {
            background-color: #ffffff;
        }

        QLabel {
            color: #2b8c8c;
            font-size: 50px;
        }

        QPushButton {
            background-color: #f1f1f1;
            border: 2px solid #2b8c8c;
            border-radius: 10px;
            font-size: 20px;
            color: #2b8c8c;
        }

        QPushButton:hover {
            background-color: #d1e7e7;
        }

        QPushButton:pressed {
            background-color: #b0d6d6;
        }

        QPushButton#backButton {
            font-size: 18px;
            background-color: #f9f9f9;
            border: 2px solid #2b8c8c;
        }

        QPushButton#backButton:hover {
            background-color: #e0f7f7;
        }
        """)

    def update_translations(self, translations, current_language):
        """
        Met à jour les textes de la page selon la langue sélectionnée.
        """
        self.translations = translations
        self.current_language = current_language
        self.title.setText(
            self.translations.get(current_language, {}).get("ramadan_title", "Dons pour le Ramadan")
        )
        self.sadaqa_button.setText(
            self.translations.get(current_language, {}).get("sadaqa_button", "Faire une Sadaqa pour l'Iftar")
        )
        self.zakat_button.setText(
            self.translations.get(current_language, {}).get("zakat_button", "Payer la Zakat al-Fitr (7 €)")
        )
        self.back_button.setText(
            self.translations.get(current_language, {}).get("back", "Retour")
        )

    def go_to_sadaqa_page(self):
        """
        Navigue vers la page Sadaqa.
        """
        parent = self.parent()
        if parent:
            # Par exemple, on navigue vers une page Sadaqa accessible via parent.parent().sadaqa_page
            parent.setCurrentIndex(parent.indexOf(parent.parent().iftar_page))

    def handle_zakat(self):
        """
        Navigue vers la page de paiement de la Zakat.
        """
        parent = self.parent()
        if parent:
            parent.setCurrentIndex(parent.indexOf(parent.parent().zakat_page))

    def return_to_home(self):
        """
        Retourne à la page d'accueil.
        """
        parent = self.parent()
        if parent:
            parent.setCurrentIndex(parent.indexOf(parent.parent().home_page))
