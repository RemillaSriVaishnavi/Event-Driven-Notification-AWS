from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=True)
    notification_type = Column(String(100), nullable=False)
    message_content = Column(String, nullable=False)
    status = Column(String(50), nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), server_default=func.now())
