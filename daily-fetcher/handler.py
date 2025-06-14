import json
from datetime import datetime

def handle(event, context):
    try:
        payload = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "trigger": "daily-fetcher"
        }
        print(json.dumps(payload))
        return json.dumps(payload)
    except Exception as e:
        return f"Erreur handler daily-fetcher : {str(e)}", 500
