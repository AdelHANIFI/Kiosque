from PySide6.QtCore import QThread, Signal
import requests
from datetime import datetime
import time

class TransactionChecker(QThread):
    transaction_found = Signal(dict)
    transaction_failed = Signal()

    def __init__(self, api_key, initiated_time, expected_amount, target_transaction_id=None, parent=None):
        super().__init__(parent)
        self.api_key = api_key
        self.initiated_time = initiated_time
        self.expected_amount = expected_amount
        self.target_transaction_id = target_transaction_id  # Optionnel pour cibler directement un paiement
        self.running = True

    def run(self):
        # On interroge l'API en récupérant jusqu'à 100 transactions par page
        base_url = "https://api.sumup.com/v0.1/me/transactions/history?limit=100"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        start_time = time.time()

        while self.running:
            transactions = []
            current_url = base_url

            # Récupération de toutes les pages disponibles
            while current_url and self.running:
                response = requests.get(current_url, headers=headers)
                if response.status_code != 200:
                    self.transaction_failed.emit()
                    return

                data = response.json()
                page_transactions = data.get("items", [])
                transactions.extend(page_transactions)

                # Recherche du lien suivant dans la réponse
                next_link = None
                for link in data.get("links", []):
                    if link.get("rel") == "next":
                        next_link = link.get("href")
                        break

                if next_link:
                    # Re-construire l'URL complète pour la page suivante
                    current_url = f"https://api.sumup.com/v0.1/me/transactions/history?{next_link}"
                else:
                    current_url = None

            # Trier les transactions par date décroissante (les plus récentes en premier)
            try:
                sorted_transactions = sorted(
                    transactions,
                    key=lambda tx: datetime.fromisoformat(tx.get("timestamp").replace("Z", "+00:00")),
                    reverse=True
                )
            except Exception:
                sorted_transactions = transactions  # En cas d'erreur de tri, utiliser l'ordre reçu

            # Vérifier si une transaction correspond aux critères
            found = False
            for tx in sorted_transactions:
                if self.is_matching_transaction(tx):
                    self.transaction_found.emit(tx)
                    found = True
                    break

            if found:
                return

            # Timeout global de 5 secondes
            if time.time() - start_time >= 5:
                self.transaction_failed.emit()
                return

            # Pause courte pour limiter les appels à l'API
            time.sleep(0.5)

    def is_matching_transaction(self, transaction):
        try:
            # Si un identifiant de transaction cible est défini, on vérifie la correspondance
            if self.target_transaction_id:
                if transaction.get("external_reference") != self.target_transaction_id:
                    return False

            transaction_time = datetime.fromisoformat(transaction["timestamp"].replace("Z", "+00:00"))
            transaction_amount = float(transaction.get("amount", 0))
            transaction_status = transaction.get("status", "UNKNOWN")
            # Calcul du delta en secondes entre l'heure de transaction et le paiement initié
            delta = abs((transaction_time - self.initiated_time).total_seconds())

            # Condition de correspondance : fenêtre de 120 secondes, montant exact et statut approprié
            return delta <= 120 and transaction_amount == self.expected_amount and transaction_status in ["SUCCESSFUL", "FAILED"]
        except Exception:
            return False

    def stop(self):
        self.running = False
