from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt
import resources_rc
class HomePage(QWidget):
    def __init__(self, parent=None, translations=None, current_language="fr"):
        super().__init__(parent)
        self.translations = translations if translations is not None else {}
        self.current_language = current_language
        self.init_ui()

    def init_ui(self):
        # Création du widget principal
        layout = QVBoxLayout()

        # Logo en haut
        logo = QLabel()
        logo_pixmap = QPixmap("images/mosquee_logo.png").scaled(
            250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        logo.setPixmap(logo_pixmap)
        logo.setAlignment(Qt.AlignCenter)

        # Titre sous le logo
        self.title = QLabel(self.translations[self.current_language]["title"])
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont("Arial", 60, QFont.Bold))

        # Boutons
        buttons_layout = QHBoxLayout()

        buttons = [
            {"key": "adherents", "help_key": "adherents_help", "icon": "images/adhesion.png", "handler": None, "extra_text": "coming_soon"},
            {"key": "mosque", "help_key": "mosque_help", "icon": "images/don.webp", "handler": self.handle_mosque},
            {"key": "works", "help_key": "works_help", "icon": "images/tr.png", "handler": self.handle_works},
            {"key": "ramadan", "help_key": "ramadan_help", "icon": "images/ramadan.png", "handler": self.handle_ramadan},
        ]
        icon_sizes = {
            "adherents": (200, 200),  # Plus grand
            "mosque": (200, 200),  # Plus grand
            "works": (200, 200),  # Réduit
            "ramadan": (200, 200)  # Réduit
        }
        self.buttons = []
        for button_data in buttons:
            # Conteneur vertical pour l'icône, le texte principal et l'aide
            button_layout = QVBoxLayout()
            buttons_layout.setSpacing(10)  # Espacement horizontal entre les boutons
            buttons_layout.setContentsMargins(50, 0, 50, 0)  # Marges autour du layout des boutons
            
            width, height = icon_sizes.get(button_data["key"], (400, 400))
            # Icône
            icon_label = QLabel()
            icon_pixmap = QPixmap(button_data["icon"]).scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(icon_pixmap)
            icon_label.setAlignment(Qt.AlignCenter)

            # Texte principal
            text_label = QLabel(self.translations[self.current_language][button_data["key"]])
            text_label.setAlignment(Qt.AlignCenter)
            text_label.setFont(QFont("Arial", 27, QFont.Bold))

            # Texte d'aide
            help_label = QLabel(self.translations[self.current_language][button_data["help_key"]])
            help_label.setAlignment(Qt.AlignCenter)
            help_label.setFont(QFont("Arial", 14))
            help_label.setStyleSheet("color: gray;")

            # Ajout du texte "Bientôt disponible" uniquement pour "Espace Adhérents"
            extra_label = None
            if "extra_text" in button_data:
                extra_label = QLabel(self.translations[self.current_language]["coming_soon"])
                extra_label.setAlignment(Qt.AlignCenter)
                extra_label.setFont(QFont("Arial", 14))
                extra_label.setStyleSheet("color: red;")  # Texte en rouge

            # Ajouter les éléments au layout
            button_layout.addWidget(icon_label)
            button_layout.addWidget(text_label)
            button_layout.addWidget(help_label)
            if extra_label:
                button_layout.addWidget(extra_label)

            # Encapsuler dans un bouton
            button_container = QPushButton()
            button_container.setLayout(button_layout)
            button_container.setMinimumSize(200, 200)
            button_container.setObjectName("homeButton")  # Appliquer le style spécifique

            # Connecter le gestionnaire de clic, si défini
            if button_data["handler"]:
                button_container.clicked.connect(button_data["handler"])

            # Ajouter le bouton au layout horizontal
            buttons_layout.addWidget(button_container)
            self.buttons.append((text_label, help_label, extra_label, button_data["key"], button_data["help_key"], button_data.get("extra_text")))

        # Ajouter les widgets au layout principal
        layout.addWidget(logo)  # Logo
        layout.addWidget(self.title)  # Titre
        layout.addLayout(buttons_layout)  # Boutons
        layout.addStretch()  # Espacement

        # Texte en bas de l'écran
        self.footer = QLabel(self.translations[self.current_language]["footer"])
        self.footer.setAlignment(Qt.AlignCenter)
        self.footer.setFont(QFont("Arial", 10))
        layout.addWidget(self.footer)

        self.setLayout(layout)

    def handle_mosque(self):
        """Gère la redirection vers la page des dons."""
        if self.parent():
            self.parent().setCurrentIndex(3)

    def handle_ramadan(self):
        """Navigue vers la page de Ramadan."""
        if self.parent():
            self.parent().setCurrentIndex(4)

    def handle_works(self):
        """Navigue vers la page des travaux."""
        if self.parent():
            self.parent().setCurrentIndex(7)

    def update_translations(self, translations, current_language):
        """Met à jour les textes de la page d'accueil avec la nouvelle langue."""
        self.translations = translations
        self.current_language = current_language

        # Met à jour les labels
        self.title.setText(self.translations[current_language].get("title", "Titre par défaut"))
        self.footer.setText(self.translations[current_language].get("footer", ""))

        # Mise à jour des boutons
        for (text_label, help_label, extra_label, key, help_key, extra_key), button_data in zip(self.buttons, [
            {"key": "adherents", "help_key": "adherents_help", "extra_key": "coming_soon"},
            {"key": "mosque", "help_key": "mosque_help"},
            {"key": "works", "help_key": "works_help"},
            {"key": "ramadan", "help_key": "ramadan_help"}
        ]):
            text_label.setText(self.translations[current_language].get(button_data["key"], ""))
            help_label.setText(self.translations[current_language].get(button_data["help_key"], ""))
            if extra_label and "extra_key" in button_data:
                extra_label.setText(self.translations[current_language].get(button_data["extra_key"], ""))

        print(f"Mise à jour de HomePage avec la langue : {current_language}")
