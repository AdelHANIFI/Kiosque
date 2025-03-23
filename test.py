import requests

class SumUpIntegration:
    def __init__(self, api_key, merchant_code):
        self.api_key = api_key
        self.merchant_code = merchant_code
        self.base_url = "https://api.sumup.com/v0.1"

    def pair_terminal(self, pairing_code):
        """
        Pairer le terminal SumUp avec le compte marchand.
        """
        url = f"{self.base_url}/merchants/{self.merchant_code}/readers"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {"pairing_code": pairing_code}

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            print("Réponse de l'API :", response.json())
            return response.json()  # Retourne les détails du terminal pairé
        except requests.RequestException as e:
            print("Erreur lors du pairing avec le terminal :", e)
            return None

# Paramètres à utiliser
api_key = "sup_sk_YkWjlUS5edcb0LAVsObRwsJXJu9dMyH6o"
merchant_code = "MFT77XNQ"
pairing_code = "UBGAV0I8R"

# Création d'une instance et pairing du terminal
sumup = SumUpIntegration(api_key, merchant_code)
terminal_details = sumup.pair_terminal(pairing_code)

if terminal_details:
    print(" Terminal pairé avec succès :", terminal_details)
else:
    print(" Le pairing du terminal a échoué.")
