import requests


from datetime import datetime

API_KEY = "sup_sk_YkWjlUS5edcb0LAVsObRwsJXJu9dMyH6o"


# On demande 100 transactions par page pour réduire le nombre d'appels
base_url = "https://api.sumup.com/v0.1/me/transactions/history?limit=200"
headers = {
    "Authorization": f"Bearer {API_KEY}"
}

def get_all_transactions():
    transactions = []
    current_url = base_url

    while current_url:
        response = requests.get(current_url, headers=headers)
        if response.status_code != 200:
            print("Erreur lors de la récupération :", response.status_code, response.text)
            break

        data = response.json()
        items = data.get("items", [])
        transactions.extend(items)

        # Chercher le lien "next" dans la réponse
        next_link = None
        for link in data.get("links", []):
            if link.get("rel") == "next":
                next_link = link.get("href")
                break

        if next_link:
            # On reconstruit l'URL complète à partir du lien next
            current_url = f"https://api.sumup.com/v0.1/me/transactions/history?{next_link}"
        else:
            current_url = None

    return transactions

def get_last_5_transactions():
    transactions = get_all_transactions()
    if not transactions:
        print("Aucune transaction trouvée.")
        return

    # Tri des transactions par horodatage décroissant (du plus récent au plus ancien)
    sorted_transactions = sorted(
        transactions,
        key=lambda tx: datetime.fromisoformat(tx.get("timestamp").replace("Z", "+00:00")),
        reverse=True
    )

    last_5 = sorted_transactions[:5]

    print("----- Les 5 transactions les plus récentes -----")
    for tx in last_5:
        print("-" * 40)
        print("ID externe :", tx.get("external_reference", "Non défini"))
        print("Montant    :", tx.get("amount"))
        print("Statut     :", tx.get("status"))
        print("Horodatage :", tx.get("timestamp"))

if __name__ == "__main__":
    get_last_5_transactions()
