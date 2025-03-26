import requests

API_KEY = "sup_sk_YkWjlUS5edcb0LAVsObRwsJXJu9dMyH6o"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

def get_all_transactions():
    url = "https://api.sumup.com/v0.1/me/transactions/history"
    all_transactions = []

    while url:
        print(f"Requête vers : {url}")
        response = requests.get(url, headers=headers)

        try:
            data = response.json()
        except Exception as e:
            print("Erreur JSON :", e)
            print("Contenu brut :", response.text)
            break

        if isinstance(data, list):
            print(" La réponse est une liste, structure inattendue :", data)
            break

        if response.status_code != 200:
            print(" Erreur :", response.status_code, data)
            break

        transactions = data.get("items", [])
        all_transactions.extend(transactions)

        # Vérification de la pagination
        next_link = None
        for link in data.get("links", []):
            if link.get("rel") == "next":
                next_link = link.get("href")
                break

        url = f"https://api.sumup.com/v0.1/me/transactions/history?{next_link}" if next_link else None

    return all_transactions

# Appel de la fonction
transactions = get_all_transactions()

# Affichage
print(f"\n{len(transactions)} transaction(s) trouvée(s) :")
for tx in transactions:
    print("ID              :", tx.get("transaction_code"))
    print("Montant         :", tx.get("amount"), tx.get("currency"))
    print("Statut          :", tx.get("status"))
    print("Date            :", tx.get("timestamp"))
    print("Description     :", tx.get("description"))
