"""
Event model for Command & Control API.
"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base


class Event(Base):
    """Event model representing system events and alerts."""

    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id"), nullable=False)
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.id"), nullable=True)
    event_type = Column(String(50), nullable=False)  # alert, status_change, command_ack
    details = Column(JSON, default=dict)
    timestamp = Column(DateTime, default=datetime.utcnow)
    severity = Column(String(20), nullable=True)  # info, warning, critical
    resolved = Column(String(20), nullable=True)  # pending, resolved, ignored
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "device_id": str(self.device_id),
            "location_id": str(self.location_id) if self.location_id else None,
            "event_type": self.event_type,
            "details": self.details,
            "timestamp": self.timestamp.isoformat(),
            "severity": self.severity,
            "resolved": self.resolved,
            "created_at": self.created_at.isoformat(),
        }
