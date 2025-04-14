from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton,
    QGridLayout, QLineEdit, QSizePolicy, QSpacerItem
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

class OtherAmountPage(QWidget):
    def __init__(self, parent=None, payment_page=None, translations=None, current_language="fr"):
        super().__init__(parent)
        self.donation_type = None  # Initialise le type de don
        self.translations = translations if translations is not None else {}
        self.current_language = current_language
        self.init_ui()
        self.payment_page = payment_page
    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # En-tête : titre
        self.title = QLabel(self.translations.get(self.current_language, {}).get("other_amount_title", "Saisissez un montant"))
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont("Arial", 48, QFont.Bold))
        main_layout.addWidget(self.title)
        
        # Zone d'affichage du montant
        self.amount_input = QLineEdit()
        self.amount_input.setAlignment(Qt.AlignCenter)
        self.amount_input.setFont(QFont("Arial", 40))
        self.amount_input.setPlaceholderText("0.00 €")
        self.amount_input.setFixedHeight(80)
        self.amount_input.setReadOnly(True)
        main_layout.addWidget(self.amount_input)
        
        # Bouton toggle (afficher/cacher le montant)
        toggle_layout = QHBoxLayout()
        toggle_layout.addStretch()
        self.toggle_button = QPushButton(self.translations.get(self.current_language, {}).get("hide_amount", "Cacher montant"))
        self.toggle_button.setFont(QFont("Arial", 20))
        self.toggle_button.setCheckable(True)
        self.toggle_button.setStyleSheet("""
            QPushButton {
                background-color: #f9f9f9;
                border: 2px solid #2b8c8c;
                border-radius: 10px;
                padding: 8px 16px;
                color: #2b8c8c;
            }
            QPushButton:hover {
                background-color: #e0f7f7;
            }
            QPushButton:pressed {
                background-color: #b0d6d6;
            }
        """)
        self.toggle_button.clicked.connect(self.toggle_visibility)
        toggle_layout.addWidget(self.toggle_button)
        toggle_layout.addStretch()
        main_layout.addLayout(toggle_layout)
        
        # Pavé numérique
        keypad_layout = QGridLayout()
        keypad_layout.setContentsMargins(10, 10, 10, 10)
        keypad_layout.setSpacing(10)
        keys = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2),
            ('C', 3, 0), ('0', 3, 1), ('.', 3, 2)
        ]
        for text, row, col in keys:
            btn = QPushButton(text)
            btn.setFont(QFont("Arial", 30, QFont.Bold))
            btn.setFixedSize(120, 120)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #ffffff;
                    border: 2px solid #2b8c8c;
                    border-radius: 60px;
                    color: #2b8c8c;
                }
                QPushButton:hover {
                    background-color: #d1f1f1;
                }
                QPushButton:pressed {
                    background-color: #a8e4e4;
                }
            """)
            btn.clicked.connect(self.handle_keypress)
            keypad_layout.addWidget(btn, row, col, Qt.AlignCenter)
        main_layout.addLayout(keypad_layout)
        
        # Bouton de validation (centré)
        validate_layout = QHBoxLayout()
        validate_layout.addStretch()
        self.validate_button = QPushButton(self.translations.get(self.current_language, {}).get("validate", "Valider"))
        self.validate_button.setFont(QFont("Arial", 30, QFont.Bold))
        self.validate_button.setFixedHeight(70)
        self.validate_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 15px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.validate_button.clicked.connect(self.validate_amount)
        validate_layout.addWidget(self.validate_button)
        validate_layout.addStretch()
        main_layout.addLayout(validate_layout)
        
        # Espace flexible
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Bouton retour (bas, centré)
        back_layout = QHBoxLayout()
        back_layout.addStretch()
        self.back_button = QPushButton(self.translations.get(self.current_language, {}).get("back", "Retour"))
        self.back_button.setFont(QFont("Arial", 22, QFont.Bold))
        self.back_button.setFixedHeight(60)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #f9f9f9;
                border: 2px solid #2b8c8c;
                border-radius: 10px;
                color: #2b8c8c;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #e0f7f7;
            }
            QPushButton:pressed {
                background-color: #b0d6d6;
            }
        """)
        self.back_button.clicked.connect(self.return_to_previous_page)
        back_layout.addWidget(self.back_button)
        back_layout.addStretch()
        main_layout.addLayout(back_layout)
        
        self.setLayout(main_layout)
    def set_donation_type(self, donation_type):
        """Définit le type de don."""
        self.donation_type = donation_type
    def update_translations(self, translations, current_language):
        self.translations = translations
        self.current_language = current_language
        self.title.setText(
            self.translations.get(current_language, {}).get("other_amount_title", "Saisissez un montant")
        )
        # Actualise le texte du bouton toggle selon son état
        if self.toggle_button.isChecked():
            self.toggle_button.setText(
                self.translations.get(current_language, {}).get("show_amount", "Afficher montant")
            )
        else:
            self.toggle_button.setText(
                self.translations.get(current_language, {}).get("hide_amount", "Cacher montant")
            )
        self.validate_button.setText(
            self.translations.get(current_language, {}).get("validate", "Valider")
        )
        self.back_button.setText(
            self.translations.get(current_language, {}).get("back", "Retour")
        )

    def handle_keypress(self):
        sender = self.sender()
        current_text = self.amount_input.text()
        if sender.text() == 'C':
            self.amount_input.setText("")
        elif sender.text() == '.':
            if '.' not in current_text:
                self.amount_input.setText(current_text + '.')
        else:
            self.amount_input.setText(current_text + sender.text())

    def toggle_visibility(self):
        from PySide6.QtWidgets import QLineEdit
        if self.toggle_button.isChecked():
            self.amount_input.setEchoMode(QLineEdit.Password)
            self.toggle_button.setText(
                self.translations.get(self.current_language, {}).get("show_amount", "Afficher montant")
            )
        else:
            self.amount_input.setEchoMode(QLineEdit.Normal)
            self.toggle_button.setText(
                self.translations.get(self.current_language, {}).get("hide_amount", "Cacher montant")
            )

    def validate_amount(self):
        amount = self.amount_input.text()
        try:
            if not amount or float(amount) <= 0:
                raise ValueError
        except ValueError:
            error_message = self.translations.get(self.current_language, {}).get("invalid_amount", "Veuillez entrer un montant valide.")
            error_dialog = QLabel(error_message)
            error_dialog.setAlignment(Qt.AlignCenter)
            error_dialog.setFont(QFont("Arial", 20, QFont.Bold))
            self.layout().addWidget(error_dialog)
            return
        print(f"Montant validé : {amount} €")
        montant = float(amount)
        self.navigate_to_payment(montant)


    def return_to_previous_page(self):
        """Retourne à la page précédente et efface le montant saisi si non validé."""
        self.amount_input.clear()  # Efface le champ de saisie
        parent = self.parent()
        if parent:
            parent.setCurrentIndex(0)  # Retour à la page précédente

    def navigate_to_payment(self, montant):
        """Navigue vers la page de paiement et initie le paiement."""
        self.amount_input.clear()  # Efface le champ de saisie

        if self.payment_page:
            self.payment_page.set_amount(montant)
            self.payment_page.initiate_payment(montant, self.donation_type)  # Appelle la méthode d'initiation de paiement avec le type de don
            parent = self.parent()
            if parent:
                parent.setCurrentIndex(2)
