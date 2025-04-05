# transaction_checker.py

from PySide6.QtCore import QThread, Signal
import requests
from datetime import datetime

class TransactionChecker(QThread):
    transaction_found = Signal(dict)
    transaction_failed = Signal()

    def __init__(self, api_key, initiated_time, expected_amount, parent=None):
        super().__init__(parent)
        self.api_key = api_key
        self.initiated_time = initiated_time
        self.expected_amount = expected_amount
        self.running = True

    def run(self):
        url = "https://api.sumup.com/v0.1/me/transactions/history"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        while url and self.running:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                self.transaction_failed.emit()
                return

            data = response.json()
            transactions = data.get("items", [])

            for tx in transactions:
                if self.is_matching_transaction(tx):
                    self.transaction_found.emit(tx)
                    return

            next_link = next((link.get("href") for link in data.get("links", []) if link.get("rel") == "next"), None)
            url = f"https://api.sumup.com/v0.1/me/transactions/history?{next_link}" if next_link else None

    def is_matching_transaction(self, transaction):
        try:
            transaction_time = datetime.fromisoformat(transaction["timestamp"].replace("Z", "+00:00"))
            transaction_amount = float(transaction.get("amount", 0))
            transaction_status = transaction.get("status", "UNKNOWN")
            delta = abs((transaction_time - self.initiated_time).total_seconds())
            return delta <= 120 and transaction_amount == self.expected_amount and transaction_status in ["SUCCESSFUL", "FAILED"]
        except Exception:
            return False

    def stop(self):
        self.running = False
