from src.models.notification import Notification
from src.database import SessionLocal

def save_notification(event_id, user_id, notification_type, message):
    db = SessionLocal()
    notif = Notification(
        event_id=event_id,
        user_id=user_id,
        notification_type=notification_type,
        message_content=message,
        status="SENT"
    )
    db.add(notif)
    db.commit()
    db.close()
