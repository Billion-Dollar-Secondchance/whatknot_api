# File: trigger_moodbox.py

import requests
import os
from datetime import datetime

API_URL = os.getenv("MOODBOX_TRIGGER_URL", "http://localhost:8000/mystery-moodbox/trigger-scheduled-prompts")
TOKEN = os.getenv("MOODBOX_ADMIN_TOKEN", "your-admin-token-here")  # Replace this with your actual token or export it

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def trigger_mystery_moodbox():
    try:
        response = requests.post(API_URL, headers=headers)
        response.raise_for_status()
        result = response.json()
        print(f"[{datetime.now()}] ✅ Triggered: {result}")
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now()}] ❌ Error triggering prompt questions: {e}")

if __name__ == "__main__":
    trigger_mystery_moodbox()
