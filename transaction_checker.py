from PySide6.QtCore import QThread, Signal
import requests
from datetime import datetime
import time

class TransactionChecker(QThread):
    transaction_found = Signal(dict)
    transaction_failed = Signal()
    transaction_pending = Signal()

    def __init__(self, api_key, initiated_time, expected_amount, target_transaction_id=None, parent=None):
        super().__init__(parent)
        self.api_key = api_key
        self.initiated_time = initiated_time
        self.expected_amount = expected_amount
        self.target_transaction_id = target_transaction_id
        self.running = True
        # Durée maximale d'attente avant échec (en secondes)
        self.max_wait = 30
        # Intervalle entre deux requêtes (en secondes)
        self.poll_interval = 0.5

    def run(self):
        base_url = "https://api.sumup.com/v0.1/me/transactions/history?limit=100"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        start_time = time.time()

        while self.running:
            transactions = []
            url = base_url

            # Pagination pour récupérer les transactions
            while url and self.running:
                response = requests.get(url, headers=headers)
                if response.status_code != 200:
                    self.transaction_failed.emit()
                    return

                data = response.json()
                transactions.extend(data.get("items", []))

                next_link = next(
                    (link.get("href") for link in data.get("links", []) if link.get("rel") == "next"),
                    None
                )
                url = f"https://api.sumup.com/v0.1/me/transactions/history?{next_link}" if next_link else None

            # Trier par date décroissante
            try:
                transactions.sort(
                    key=lambda tx: datetime.fromisoformat(tx.get("timestamp").replace("Z", "+00:00")),
                    reverse=True
                )
            except Exception:
                pass

            # Parcourir pour identifier la transaction
            pending_reported = False
            for tx in transactions:
                if self._tx_matches(tx):
                    status = tx.get("status")
                    if status == "SUCCESSFUL":
                        self.transaction_found.emit(tx)
                        return
                    elif status == "FAILED":
                        self.transaction_failed.emit()
                        return
                    elif status == "PENDING":
                        # Émettre que c'est en attente, puis continuer le polling
                        if not pending_reported:
                            self.transaction_pending.emit()
                            pending_reported = True
                        break  # sortir de la boucle tx pour attendre

            # Timeout global
            if time.time() - start_time >= self.max_wait:
                self.transaction_failed.emit()
                return

            time.sleep(self.poll_interval)

    def _tx_matches(self, tx):
        try:
            if self.target_transaction_id and tx.get("external_reference") != self.target_transaction_id:
                return False

            tx_time = datetime.fromisoformat(tx.get("timestamp").replace("Z", "+00:00"))
            amount = float(tx.get("amount", 0))
            delta = abs((tx_time - self.initiated_time).total_seconds())

            return delta <= 120 and amount == self.expected_amount
        except Exception:
            return False

    def stop(self):
        self.running = False
