# File: scripts/trigger_vibe_match.py

import requests
from datetime import datetime

if __name__ == "__main__":
    try:
        # Trigger the scheduled Vibe Match questions (this should point to your backend's trigger endpoint)
        response = requests.post("http://localhost:8000/vibe-match/trigger-scheduled")
        print(f"[{datetime.now()}] Triggered vibe match prompts.")
        print("Response:", response.json())
    except Exception as e:
        print(f"Error triggering vibe match prompts: {str(e)}")
