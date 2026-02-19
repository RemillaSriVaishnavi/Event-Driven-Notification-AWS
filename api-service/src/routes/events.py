from fastapi import APIRouter
from pydantic import BaseModel
from src.services.eventPublisher import publish_event

router = APIRouter()

class NotificationRequest(BaseModel):
    message: str

@router.post("/notify")
async def notify(request: NotificationRequest):
    event = {
        "eventType": "NotificationRequested",
        "payload": {
            "message": request.message
        }
    }

    publish_event("NotificationRequested", event)

    return {
        "status": "Notification event published"
    }
