import requests
import json
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from datetime import timedelta


def generate_order(amount):
    data = {
        "amount": int(amount * 100),  # Convert the amount to paise
        "currency": "INR",
        "partial_payment": False,
    }
    response = requests.post(
        'https://api.razorpay.com/v1/orders/',
        headers={
            "Content-Type": "application/json",
        },
        data=json.dumps(data),
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET,
        )
    )
    if response.status_code == 200:
        order_data = json.loads(response.content)
        order_id = order_data.get("id")
        print("Generated Order ID:", order_id)  # Add this line for debugging
        return order_id
    else:
        return None


