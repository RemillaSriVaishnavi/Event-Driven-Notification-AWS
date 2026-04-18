from fastapi import APIRouter
from pydantic import BaseModel
from src.services.eventPublisher import publish_event

router = APIRouter()

class NotificationRequest(BaseModel):
    message: str

class UserRegisterRequest(BaseModel):
    user_id: str
    email: str

class OrderRequest(BaseModel):
    order_id: str
    user_id: str
    amount: float

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


router = APIRouter()

@router.post("/api/users/register")
def register_user(data: UserRegisterRequest):
    event = {
        "event_type": "UserRegisteredEvent",
        "event_id": data.user_id,
        "email": data.email
    }
    publish_event(event)
    return {"message": "User registered event sent"}


@router.post("/api/orders/place")
def place_order(data: OrderRequest):
    event = {
        "event_type": "OrderPlacedEvent",
        "event_id": data.order_id,
        "user_id": data.user_id,
        "amount": data.amount
    }
    publish_event(event)
    return {"message": "Order placed event sent"}