import requests
import base64
from datetime import datetime
from requests.auth import HTTPBasicAuth
from config import MPESA

def get_access_token():

    response = requests.get(
        MPESA["TOKEN_URL"],
        auth=HTTPBasicAuth(
            MPESA["CONSUMER_KEY"],
            MPESA["CONSUMER_SECRET"]
        )
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }


def generate_password():

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    data = MPESA["SHORTCODE"] + MPESA["PASSKEY"] + timestamp

    password = base64.b64encode(data.encode()).decode()

    return password, timestamp


def stk_push(phone, amount):

    headers = get_access_token()

    password, timestamp = generate_password()

    payload = {
        "BusinessShortCode": MPESA["SHORTCODE"],
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": phone,
        "PartyB": MPESA["SHORTCODE"],
        "PhoneNumber": phone,
        "CallBackURL": MPESA["CALLBACK_URL"],
        "AccountReference": "Order123",
        "TransactionDesc": "Payment"
    }

    response = requests.post(
        MPESA["STK_PUSH_URL"],
        json=payload,
        headers=headers
    )

    return response.json()