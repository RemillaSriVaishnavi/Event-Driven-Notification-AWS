import uuid
from datetime import datetime

def create_event(event_type, payload):
    return {
        "eventId": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "eventType": event_type,
        "payload": payload
    }
