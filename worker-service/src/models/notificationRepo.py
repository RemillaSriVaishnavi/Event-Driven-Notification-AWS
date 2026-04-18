from src.models.notification import Notification
from src.database import SessionLocal
from sqlalchemy.orm import Session

def save_notification(db: Session, event_id: str, message: str):

    existing = db.query(Notification).filter_by(event_id=event_id).first()

    if existing:
        print("Duplicate event, skipping...")
        return

    notification = Notification(event_id=event_id, message=message)
    db.add(notification)
    db.commit()