from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QMovie
import requests
import time
import uuid
from datetime import datetime, timezone
import sys
import json
import os 

def load_terminal_id():
    config_path = os.path.join(os.path.dirname(__file__), "terminal_config.json")
    with open (config_path,"r") as f :
        data = json.load(f)
        data.get("terminal_id")
class PaymentPage(QWidget):
    API_KEY = "sup_sk_YkWjlUS5edcb0LAVsObRwsJXJu9dMyH6o"  # Clé API SumUp
    TERMINAL_ID = load_terminal_id() # ID du terminal
    LOG_FILE = "transactions_log.txt"  # Fichier où les transactions seront enregistrées

    
    
    
    
    def __init__(self, parent=None, amount=0.0, api_key=None, translations=None, current_language="fr",donation_type=None):
        super().__init__(parent)
        self.amount = amount
        self.api_key = api_key
        self.translations = translations if translations is not None else {}
        self.current_language = current_language
        self.initiated_time = None
        self.payment_pending = False  # Indicateur de paiement en attente
        self.donation_type = donation_type


        layout = QVBoxLayout()
        self.title = QLabel(self.translations.get(self.current_language, {}).get("payment_title", "JE SOUTIENS"))
        self.title.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self.title.setFont(QFont("Arial", 30, QFont.Bold))
        layout.addWidget(self.title)

        self.subtitle = QLabel(self.translations.get(self.current_language, {}).get("payment_subtitle", "Mosquée de Pau"))
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.subtitle.setFont(QFont("Arial", 40, QFont.Bold))
        layout.addWidget(self.subtitle)

        self.amount_label = QLabel(f"{self.amount:.2f} €")
        self.amount_label.setAlignment(Qt.AlignCenter)
        self.amount_label.setFont(QFont("Arial", 50, QFont.Bold))
        layout.addWidget(self.amount_label)

        self.toggle_button = QPushButton("Cacher montant")
        self.toggle_button.setFont(QFont("Arial", 20))
        self.toggle_button.setCheckable(True)
        self.toggle_button.clicked.connect(self.toggle_visibility)
        layout.addWidget(self.toggle_button, alignment=Qt.AlignCenter)

        self.gif_label = QLabel()
        self.gif_label.setAlignment(Qt.AlignCenter)
        self.gif = QMovie("images/gif.gif")
        self.gif_label.setMovie(self.gif)
        self.gif.start()
        layout.addWidget(self.gif_label)

        self.instructions = QLabel("Veuillez taper ou insérer votre carte de crédit/débit ci-dessous")
        self.instructions.setAlignment(Qt.AlignCenter)
        self.instructions.setFont(QFont("Arial", 20))
        layout.addWidget(self.instructions)

        self.back_button = QPushButton("Retour")
        self.back_button.setFont(QFont("Arial", 20))
        self.back_button.clicked.connect(self.return_to_home)
        layout.addWidget(self.back_button, alignment=Qt.AlignBottom)

        self.setLayout(layout)
       

    def initiate_payment(self, amount, donation_type):
        """Initie le paiement sur le terminal SumUp."""
        if self.payment_pending:
            self.display_pending_message()
            return

        descriptions = {
            'iftar': 'Don pour l\'Iftar',
            'travaux': 'Don pour les travaux',
            'zakat': 'Zakat',
            'sadaqa': 'Don pour la mosquée'
        }
        description = descriptions.get(donation_type, 'Don pour la mosquée')

        #url = f"https://api.sumup.com/v0.1/terminals/{self.TERMINAL_ID}/checkout"
        url = f"https://api.sumup.com/v0.1/merchants/MFT77XNQ/readers/{self.TERMINAL_ID}/checkout"
        headers = {"Authorization": f"Bearer {self.API_KEY}", "Content-Type": "application/json"}

        self.initiated_time = datetime.now(timezone.utc)  # Heure du paiement en UTC

        data = {
            "amount": amount,
            "currency": "EUR",
            "description": description,
            "client_id": str(uuid.uuid4())
        }

        print(f" Envoi de la requête de paiement ({donation_type})...")
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 201:
                print(f"Paiement initié avec succès.")
                QTimer.singleShot(5000, self.check_transaction_status)  # Vérifier après 5s
            elif response.status_code == 422 and "A pending transaction already exists for this device" in response.text:
                print("Un paiement est déjà en attente sur le terminal.")
                self.payment_pending = True
                self.display_pending_message()
            else:
                print("Erreur lors de l'initiation du paiement :", response.json())
                self.display_payment_status(False)
        except Exception as e:
            print("Erreur :", str(e))
            self.display_payment_status(False)

    def check_transaction_status(self):
        """Vérifie l'état du paiement avec pagination `next_link`."""
        url = "https://api.sumup.com/v0.1/me/transactions/history"
        headers = {"Authorization": f"Bearer {self.API_KEY}"}

        while url:
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                transactions = data.get("items", [])

                for tx in transactions:
                    if self.compare_transaction(tx):
                        return  # Arrêt dès qu'on trouve la transaction

                # Vérifier s'il y a une page suivante
                next_link = None
                for link in data.get("links", []):
                    if link.get("rel") == "next":
                        next_link = link.get("href")
                        break

                url = f"https://api.sumup.com/v0.1/me/transactions/history?{next_link}" if next_link else None
            else:
                print(f"Erreur récupération : {response.status_code}")
                self.display_payment_status(False)
                return

        QTimer.singleShot(2000, self.check_transaction_status)  # Relancer dans 5s

    def compare_transaction(self, transaction):
        """Compare la transaction avec celle initiée en utilisant l'heure et le montant."""
        transaction_time = datetime.fromisoformat(transaction["timestamp"].replace("Z", "+00:00"))
        transaction_amount = float(transaction["amount"])
        transaction_status = transaction["status"]

        # Vérification avec l'heure et le montant uniquement
        if (
            abs((transaction_time - self.initiated_time).total_seconds()) <= 120
            and transaction_amount == self.amount
        ):
            print(f"Transaction trouvée : {transaction_status}")
            if transaction_status == "SUCCESSFUL":
                self.log_transaction(transaction)  
                self.display_payment_status(True)
                return True
            elif transaction_status == "FAILED":
                self.log_transaction(transaction)  
                self.display_payment_status(False)
                return True
        elif transaction_status == "PENDING":
            print(" Paiement en attente...")
            return False

        return False

    def log_transaction(self, transaction):
        """Enregistre une transaction réussie dans le bon fichier."""
        donation_files = {
            "sadaqa": "transactions_sadaqa.txt",
            "iftar": "transactions_iftar.txt",
            "travaux": "transactions_travaux.txt",
            "zakat": "transactions_zakat.txt",
        }
        file_name = donation_files.get(self.donation_type, "transactions_autres.txt")  

        log_entry = (
            f"{datetime.now()} | Montant: {transaction['amount']} {transaction['currency']} | "
            f"Carte: {transaction.get('card_type', 'Inconnu')} | "
            f"Statut: {transaction['status']} | Utilisateur: {transaction.get('user', 'N/A')}\n"
        )

        with open(file_name, "a", encoding="utf-8") as f:
            f.write(log_entry)

        print(f" Transaction enregistrée dans {file_name}.")

    def display_pending_message(self):
        """Affiche un message demandant d'annuler ou de finaliser un paiement en attente."""
        self.clear_screen()
        label = QLabel("Un paiement est en attente sur le terminal.\n\nMerci de patienter ou d'annuler le paiement.")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 30, QFont.Bold))
        self.layout().addWidget(label)
        QTimer.singleShot(3000, self.return_to_home)
    def display_payment_status(self, success):
        """Affiche le statut du paiement et redirige vers la bonne page."""
        self.clear_screen()
        
        if success:
            message = " Merci pour votre don !"
            label = QLabel(message)
            label.setAlignment(Qt.AlignCenter)
            label.setFont(QFont("Arial", 30, QFont.Bold))
            self.layout().addWidget(label)

            # Retour à l'accueil après 3 secondes
            QTimer.singleShot(3000, self.return_to_home)
        
        else:
            message = " Paiement échoué. Veuillez réessayer."
            label = QLabel(message)
            label.setAlignment(Qt.AlignCenter)
            label.setFont(QFont("Arial", 30, QFont.Bold))
            self.layout().addWidget(label)

            retry_button = QPushButton("Réessayer")
            retry_button.setFont(QFont("Arial", 20))
            retry_button.clicked.connect(self.retry_payment)  # Appelle une nouvelle méthode
            self.layout().addWidget(retry_button, alignment=Qt.AlignCenter)

            cancel_button = QPushButton("Annuler")
            cancel_button.setFont(QFont("Arial", 20))
            cancel_button.clicked.connect(self.return_to_home)
            self.layout().addWidget(cancel_button, alignment=Qt.AlignCenter)

    def clear_screen(self):
        """Efface tous les widgets de la page."""
        for i in reversed(range(self.layout().count())):
            widget = self.layout().itemAt(i).widget()
            if widget:
                widget.setParent(None)
    def update_translations(self, translations, current_language):
        self.translations = translations
        self.current_language = current_language
        self.title.setText(self.translations.get(current_language, {}).get("payment_title", "JE SOUTIENS"))
        self.subtitle.setText(self.translations.get(current_language, {}).get("payment_subtitle", "Mosquée de Pau"))
        self.instructions.setText(self.translations.get(current_language, {}).get("payment_instructions", "Veuillez taper ou insérer votre carte de crédit/débit ci-dessous"))
    def toggle_visibility(self):
        if self.amount_label.text() == "******":
            self.amount_label.setText(f"{self.amount:.2f} €")
            self.toggle_button.setText("Cacher montant")
        else:
            self.amount_label.setText("******")
            self.toggle_button.setText("Afficher montant")
    def retry_payment(self):
        """Réinitialise la page et relance le paiement."""
        self.clear_screen()  # On efface l'affichage précédent

        layout = self.layout()

        self.title.setText(self.translations.get(self.current_language, {}).get("payment_title", "JE SOUTIENS"))
        layout.addWidget(self.title)

        self.subtitle.setText(self.translations.get(self.current_language, {}).get("payment_subtitle", "Mosquée de Pau"))
        layout.addWidget(self.subtitle)

        self.amount_label.setText(f"{self.amount:.2f} €")
        layout.addWidget(self.amount_label)

        self.gif_label.setMovie(self.gif)
        self.gif.start()
        layout.addWidget(self.gif_label)

        self.instructions.setText("Veuillez taper ou insérer votre carte de crédit/débit ci-dessous")
        layout.addWidget(self.instructions)

        # Relancer le paiement
        self.reset_page()  # Nettoyage avant de relancer un paiement
        self.initiate_payment(self.amount, "sadaqa")  # Relance le paiement
    def reset_page(self):
        """Réinitialise complètement la page pour un nouvel affichage propre."""
        self.clear_screen()  # Efface tous les widgets

        # Réinitialisation des variables
        self.payment_pending = False
        self.initiated_time = None

        #  Réaffichage des éléments
        layout = self.layout()

        self.title.setText(self.translations.get(self.current_language, {}).get("payment_title", "JE SOUTIENS"))
        layout.addWidget(self.title)

        self.subtitle.setText(self.translations.get(self.current_language, {}).get("payment_subtitle", "Mosquée de Pau"))
        layout.addWidget(self.subtitle)

        self.amount_label.setText(f"{self.amount:.2f} €")
        layout.addWidget(self.amount_label)

        self.gif_label.setMovie(self.gif)
        self.gif.start()
        layout.addWidget(self.gif_label)

        self.instructions.setText("Veuillez taper ou insérer votre carte de crédit/débit ci-dessous")
        layout.addWidget(self.instructions)

        self.back_button.setText("Retour")
        layout.addWidget(self.back_button)

        print(" Page réinitialisée !")


    def return_to_home(self):
        """Annule et retourne à l'accueil avec une page propre."""
        self.reset_page()  # Réinitialise tout avant de partir
        parent = self.parent()
        if parent:
            parent.setCurrentIndex(0)  # Retour à la page d'accueil

    def set_amount(self, amount):
        self.amount = float(amount)
        self.amount_label.setText(f"{self.amount:.2f} €")
