from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSpinBox
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import requests

class ZakatPage(QWidget):
    def __init__(self, parent=None, payment_page=None, translations=None, current_language="fr"):
        super().__init__(parent)
        self.translations = translations if translations else {}
        self.current_language = current_language
        self.payment_page = payment_page

        self.amount_per_person = 7

        layout = QVBoxLayout()

        # Titre
        self.title = QLabel(self.translations.get(self.current_language, {}).get("zakat_title", "Zakât al-Fitr"))
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont("Arial", 60, QFont.Bold))

        # Explication
        self.explanation = QLabel(
            self.translations.get(self.current_language, {}).get(
                "zakat_explanation",
                f"La Zakât al-Fitr est fixée à {self.amount_per_person} € par personne.\n"
                "Veuillez choisir le nombre de personnes."
            )
        )
        self.explanation.setAlignment(Qt.AlignCenter)
        self.explanation.setFont(QFont("Arial", 25))

        # Sélecteur de nombre de personnes
        people_layout = QHBoxLayout()
        people_label = QLabel("Nombre de personnes : ")
        people_label.setFont(QFont("Arial", 22))
        
        self.people_spinbox = QSpinBox()
        self.people_spinbox.setMinimum(1)
        self.people_spinbox.setMaximum(300)
        self.people_spinbox.setValue(1)
        self.people_spinbox.setFont(QFont("Arial", 30))
        self.people_spinbox.setFixedSize(150, 80)
        self.people_spinbox.setStyleSheet("""
            QSpinBox {
                padding: 10px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 30px;
                height: 30px;
            }
        """)

        people_layout.addWidget(people_label)
        people_layout.addWidget(self.people_spinbox)
        people_layout.setAlignment(Qt.AlignCenter)

        # Bouton de paiement
        self.zakat_button = QPushButton(f"Payer {self.amount_per_person} €")
        self.zakat_button.setFont(QFont("Arial", 40, QFont.Bold))
        self.zakat_button.setFixedSize(350, 350)
        self.zakat_button.setStyleSheet("""
            QPushButton {
                border: 2px solid #2b8c8c;
                border-radius: 175px;
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
        self.zakat_button.clicked.connect(self.pay_zakat)

        # Bouton retour
        self.back_button = QPushButton(self.translations.get(self.current_language, {}).get("back", "Retour"))
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
        self.back_button.clicked.connect(self.return_to_previous_page)

        layout.addWidget(self.title)
        layout.addWidget(self.explanation)
        layout.addLayout(people_layout)
        layout.addWidget(self.zakat_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.back_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def update_button_amount(self):
        nb_personnes = self.people_spinbox.value()
        total = nb_personnes * self.amount_per_person
        self.zakat_button.setText(f"Payer {total} €")

    def pay_zakat(self):
        nb_personnes = self.people_spinbox.value()
        total = nb_personnes * self.amount_per_person
        if self.payment_page:
            self.payment_page.set_amount(total)
            self.payment_page.initiate_payment(total, 'zakat')
            parent = self.parent()
            if parent:
                parent.setCurrentIndex(2)

    def update_translations(self, translations, current_language):
        self.translations = translations
        self.current_language = current_language
        self.title.setText(self.translations.get(current_language, {}).get("zakat_title", "Zakât al-Fitr"))
        self.explanation.setText(
            self.translations.get(current_language, {}).get(
                "zakat_explanation",
                f"La Zakât al-Fitr est fixée à {self.amount_per_person} € par personne.\nVeuillez choisir le nombre de personnes."
            )
        )
        self.back_button.setText(self.translations.get(current_language, {}).get("back", "Retour"))

    def return_to_previous_page(self):
        parent = self.parent()
        if parent:
            parent.setCurrentIndex(0)
