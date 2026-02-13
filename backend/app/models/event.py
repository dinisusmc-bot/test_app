"""
Event model for GeoMap Simulation API.
Tracks system events and engagement events.
"""

from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base


class Event(Base):
    """Event model representing system events in the simulation."""

    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=True)
    engagement_id = Column(UUID(as_uuid=True), ForeignKey("engagements.id"), nullable=True)
    event_type = Column(String(50), nullable=False)  # alert, status_change, command_ack, engagement_start, engagement_end
    details = Column(JSON, default=dict)
    timestamp = Column(DateTime, default=datetime.utcnow)
    severity = Column(String(20), nullable=True)  # info, warning, critical
    resolved = Column(String(20), default="pending")  # pending, resolved, ignored
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "asset_id": str(self.asset_id) if self.asset_id else None,
            "engagement_id": str(self.engagement_id) if self.engagement_id else None,
            "event_type": self.event_type,
            "details": self.details,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "severity": self.severity,
            "resolved": self.resolved,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
