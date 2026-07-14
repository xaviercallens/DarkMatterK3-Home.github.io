import requests
import json
import time

API_URL = "http://127.0.0.1:8000"

payload = {
    "sector_id": 99,
    "delta": 6.82,
    "s12": 1.99,
    "s21": 0.40,
    "mean_asymmetry": 5.12,
    "max_asymmetry": 15.34,
    "author": "@callensxavier",
    "type": "New Dark Energy Amas (Chameleon Gravitino Knot)"
}

res = requests.post(f"{API_URL}/api/v1/discoveries/browser", json=payload)
print(res.json())
