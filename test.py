import requests

# Vos identifiants SumUp
API_KEY = "sup_sk_YkWjlUS5edcb0LAVsObRwsJXJu9dMyH6o"  # ⚠️ Clé API privée
MERCHANT_CODE = "MFT77XNQ"  # Code marchand
READER_ID = "0af00839-2a15-413d-9c8e-584a5e58a72c"  # ID du terminal appairé

def initiate_payment(amount_euros):
    # Construction du montant en "minor units" (centimes d'euros ici)
    value = int(float(amount_euros) * 100)

    url = f"https://api.sumup.com/v0.1/merchants/{MERCHANT_CODE}/readers/{READER_ID}/checkout"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "total_amount": {
            "currency": "EUR",
            "minor_unit": 2,
            "value": value
        },
        "description": f"Paiement de {amount_euros:.2f} € via Solo"
        # Vous pouvez aussi ajouter un "return_url" ici pour un webhook
    }

    print(" Envoi du paiement au terminal...")
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        if response.status_code == 201:
            print(" Paiement lancé avec succès sur le terminal SumUp Solo !")
            print(" Détails :", response.json())
        else:
            print(" Réponse inattendue :", response.status_code, response.text)

    except requests.RequestException as e:
        print(" Erreur pendant l'initiation du paiement :", e)
        if hasattr(e, 'response') and e.response is not None:
            print("Réponse de l'API :", e.response.status_code, e.response.text)
# Exemple : lancer un paiement de 7 euros
initiate_payment(7.00)