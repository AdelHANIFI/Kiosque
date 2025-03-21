import requests
import time
import uuid
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client_id = str(uuid.uuid4())

def refresh_access_token():
    url = "https://api.sumup.com/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": "rt_classic_zV5UHdS5Fp0aQT4lCRSwAxeyQEwW6819llmyUcNfq2Kvz5abaIMIs",
        "client_id": "cc_classic_qf3ruSkctMqev5ZrWrhRViXFrj4he",
        "client_secret": "cc_sk_classic_mB997MTJmFEIcAbOJ0D2fGkfrfzRhQDmHUPtBCiqEQzaip4Wwu",
        "scope": "payments"  # Scope requis pour les paiements
    }
    
    response = requests.post(url, data=data)
    if response.status_code == 200:
        token_data = response.json()
        return token_data["access_token"], token_data["expires_in"]
    else:
        logger.error("Erreur lors de l'obtention du jeton : %s", response.json())
        raise Exception("Erreur lors de l'obtention du jeton :", response.json())
def initiate_payment(amount):
    try:
        access_token, expires_in = refresh_access_token()
        url = "https://api.sumup.com/v0.1/terminals/0af00839-2a15-413d-9c8e-584a5e58a72c/checkout"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        checkout_reference = f"donation-{int(time.time())}"
        data = {
            "amount": amount,
            "checkout_reference": checkout_reference,
            "currency": "EUR",
            "description": "Don pour la mosquée",
            "merchant_code": "MFT77XNQ",
            "client_id": client_id
        }
        response = requests.post(url, headers=headers, json=data)
        logger.info("Status code: %s", response.status_code)
        logger.info("Response headers: %s", response.headers)
        logger.info("Response text: %s", response.text)
        
        if response.status_code == 201:
            if response.text.strip():
                try:
                    json_response = response.json()
                    checkout_id = json_response.get("id")
                    if checkout_id:
                        logger.info("Paiement initié avec succès, checkout_id : %s", checkout_id)
                        return checkout_id
                    else:
                        logger.warning("Paiement initié, mais aucun checkout_id trouvé : %s", json_response)
                        return None
                except Exception as e:
                    logger.error("Erreur lors du décodage du JSON : %s", e)
                    return None
            else:
                logger.info("Paiement initié avec succès, mais aucune donnée retournée. checkout_reference: %s", checkout_reference)
                generated_id = str(uuid.uuid4())
                logger.info("Génération d'un checkout_id local : %s", generated_id)
                return generated_id
        else:
            logger.error("Erreur lors de l'initiation du paiement : %s %s", response.status_code, response.text)
            return None
    except Exception as e:
        logger.error("Une erreur s'est produite : %s", e)
        return None

def get_payment_status(checkout_id):
    try:
        access_token, expires_in = refresh_access_token()
        url = f"https://api.sumup.com/v0.1/checkouts/{checkout_id}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        response = requests.get(url, headers=headers)
        logger.info("Status code: %s", response.status_code)
        logger.info("Response headers: %s", response.headers)
        logger.info("Response text: %s", response.text)
        
        if response.status_code == 200:
            payment_status = response.json().get("status")
            logger.info("État du paiement pour checkout_id %s : %s", checkout_id, payment_status)
            return payment_status
        else:
            logger.error("Erreur lors de la récupération de l'état du paiement : %s %s", response.status_code, response.text)
            return None
    except Exception as e:
        logger.error("Une erreur s'est produite : %s", e)
        return None

def cancel_payment(checkout_id):
    try:
        access_token, expires_in = refresh_access_token()
        url = f"https://api.sumup.com/v0.1/checkouts/{checkout_id}/cancel"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        response = requests.post(url, headers=headers)
        logger.info("Status code: %s", response.status_code)
        logger.info("Response headers: %s", response.headers)
        logger.info("Response text: %s", response.text)
        
        if response.status_code == 200:
            logger.info("Paiement annulé avec succès pour checkout_id : %s", checkout_id)
            return True
        else:
            logger.error("Erreur lors de l'annulation du paiement : %s %s", response.status_code, response.text)
            return False
    except Exception as e:
        logger.error("Une erreur s'est produite lors de l'annulation du paiement : %s", e)
        return False

if __name__ == "__main__":
    # Initier un paiement
    checkout_id = initiate_payment(3)
    if checkout_id:
        logger.info("Paiement initié avec succès. Checkout ID: %s", checkout_id)
        
        # Vérifier l'état du paiement avant annulation
        payment_status = get_payment_status(checkout_id)
        if payment_status and payment_status == "PENDING":  # Annuler seulement si le paiement est en attente
            logger.info("Tentative d'annulation du paiement...")
            if cancel_payment(checkout_id):
                logger.info("Paiement annulé avec succès.")
            else:
                logger.error("Échec de l'annulation du paiement.")
        else:
            logger.error("Le paiement ne peut pas être annulé (état : %s).", payment_status)
    else:
        logger.error("Échec de l'initiation du paiement.")