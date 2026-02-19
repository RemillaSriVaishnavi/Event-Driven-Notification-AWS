from src.services.notificationProcessor import poll_messages
from src.database import engine
from src.models.notification import Base, Notification

print("Creating notifications table...")
Base.metadata.create_all(bind=engine)

print("Worker Started...Polling SQS...")
poll_messages()
