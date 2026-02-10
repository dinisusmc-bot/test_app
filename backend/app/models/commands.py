"""
Command model for Command & Control API.
"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base


class Command(Base):
    """Command model representing commands sent to devices."""

    __tablename__ = "commands"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_id = Column(UUID(as_uuid=True), nullable=False)
    location_id = Column(UUID(as_uuid=True), nullable=True)
    command_type = Column(String(50), nullable=False)  # patrol, survey, return, etc.
    payload = Column(JSON, default=dict)
    status = Column(String(20), nullable=False, default="pending")  # pending, sent, acknowledged, failed
    error_message = Column(String(255), nullable=True)
    acknowledged_at = Column(DateTime, nullable=True)
    failed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "device_id": str(self.device_id),
            "location_id": str(self.location_id) if self.location_id else None,
            "command_type": self.command_type,
            "payload": self.payload,
            "status": self.status,
            "error_message": self.error_message,
            "acknowledged_at": self.acknowledged_at.isoformat() if self.acknowledged_at else None,
            "failed_at": self.failed_at.isoformat() if self.failed_at else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
