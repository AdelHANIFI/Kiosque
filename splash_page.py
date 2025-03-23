from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QComboBox, QSizePolicy
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt, Signal
import resources_rc
class SplashPage(QWidget):
    language_changed = Signal(str)  # Signal pour informer MainApp du changement de langue

    def __init__(self, parent=None, translations=None, current_language="fr"):
        super().__init__(parent)
        self.translations = translations if translations is not None else {}
        self.current_language = current_language
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # Barre supérieure : Image tactile à gauche et Sélecteur de langue à droite
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(20, 20, 20, 20)

        # Sélecteur de langue (version tactile agrandie)
        lang_layout = QHBoxLayout()



        # Label agrandi clairement
        self.lang_label = QLabel(self.translations.get(self.current_language, {}).get("language_label", "Langue:"))
        self.lang_label.setFont(QFont("Arial", 40))

        # ComboBox agrandi clairement
        self.language_selector = QComboBox()
        self.language_selector.setFont(QFont("Arial", 36))
        self.language_selector.setFixedHeight(100)
        self.language_selector.setMinimumWidth(300)
        self.language_selector.addItems(["Français", "English", "العربية"])
        self.language_selector.currentIndexChanged.connect(self.change_language)

        lang_layout.addWidget(self.lang_label)
        lang_layout.addWidget(self.language_selector)
        lang_layout.addStretch()

        # Ajout du logo tactile en haut à droite
        top_logo_layout = QHBoxLayout()

        tactile_logo = QLabel()
        pixmap = QPixmap("images/tactile.png")  # Placez ici votre image tactile.png dans le dossier 'images'
        pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        tactile_logo.setPixmap(pixmap)
        #placer le logo tactile en haut à droite avec une marge de 20 pixels
        tactile_logo.setAlignment(Qt.AlignRight | Qt.AlignTop)
        tactile_logo.setContentsMargins(0, 60, 40, 0)
        

        top_logo_layout.addStretch()
        top_logo_layout.addWidget(tactile_logo)

        # Layout final combiné (langue à gauche, logo à droite)
        final_top_layout = QHBoxLayout()
        final_top_layout.addLayout(lang_layout)
        final_top_layout.addLayout(top_logo_layout)

        layout.addLayout(final_top_layout)
        # Titre
        self.title_label = QLabel(self.translations.get(self.current_language, {}).get("splash_title", "Borne de Paiement"))
        self.title_label.setFont(QFont("Arial", 96, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        # Logo
        self.logo_label = QLabel()
        logo_pixmap = QPixmap("images/mosquee_logo.png")
        logo_pixmap = logo_pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo_label.setPixmap(logo_pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.logo_label)

        # Instruction
        self.instruction_label = QLabel(self.translations.get(self.current_language, {}).get("splash_instruction", "Cliquez n'importe où pour continuer"))
        self.instruction_label.setFont(QFont("Arial", 48))
        self.instruction_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.instruction_label)

        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    def change_language(self):
        """Envoie la langue sélectionnée sous forme de texte à `MainApp`."""
        languages = {"Français": "fr", "English": "en", "العربية": "ar"}
        selected_text = self.language_selector.currentText()

        if selected_text in languages:
            new_language = languages[selected_text]
            print(f" SplashPage: Langue sélectionnée -> {new_language}")
            self.language_changed.emit(new_language)  # 🔴 Envoi du signal sous forme de texte


    def update_translations(self, translations, current_language):
        """Met à jour les textes selon la langue choisie."""
        self.translations = translations
        self.current_language = current_language
        self.title_label.setText(self.translations[current_language]["splash_title"])
        self.lang_label.setText(self.translations[current_language]["language_label"])
        self.instruction_label.setText(self.translations[current_language]["splash_instruction"])


    def mousePressEvent(self, event):
        if self.parent():
            self.parent().setCurrentIndex(3)

  