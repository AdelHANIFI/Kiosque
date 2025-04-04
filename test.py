import requests

API_KEY = "sup_sk_YkWjlUS5edcb0LAVsObRwsJXJu9dMyH6o"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

def get_latest_transaction():
    url = "https://api.sumup.com/v0.1/me/transactions/history"
    latest_transaction = None

    while url:
        print(f"Requête vers : {url}")
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print("Erreur :", response.status_code, response.text)
            return None

        try:
            data = response.json()
        except Exception as e:
            print("Erreur JSON :", e)
            return None

        transactions = data.get("items", [])
        if transactions:
            latest_transaction = transactions[-1]  # On garde les dernières à chaque page

        # Chercher le lien "next"
        next_link = None
        for link in data.get("links", []):
            if link.get("rel") == "next":
                next_link = link.get("href")
                break

        url = f"https://api.sumup.com/v0.1/me/transactions/history?{next_link}" if next_link else None

    return latest_transaction


# Utilisation
tx = get_latest_transaction()
if tx:
    print("\nDernière transaction :")
    print("ID              :", tx.get("transaction_code"))
    print("Montant         :", tx.get("amount"), tx.get("currency"))
    print("Statut          :", tx.get("status"))
    print("Date            :", tx.get("timestamp"))
    print("Description     :", tx.get("description"))
else:
    print("Aucune transaction trouvée.")
