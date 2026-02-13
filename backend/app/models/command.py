"""
Command model for GeoMap Simulation API.
Tracks commands sent to assets.
"""

from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base


class Command(Base):
    """Command model representing commands sent to assets."""

    __tablename__ = "commands"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=True)
    engagement_id = Column(UUID(as_uuid=True), ForeignKey("engagements.id"), nullable=True)
    command_type = Column(String(50), nullable=False)  # patrol, survey, return, stop, resume, engage, disengage
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
            "asset_id": str(self.asset_id) if self.asset_id else None,
            "engagement_id": str(self.engagement_id) if self.engagement_id else None,
            "command_type": self.command_type,
            "payload": self.payload,
            "status": self.status,
            "error_message": self.error_message,
            "acknowledged_at": self.acknowledged_at.isoformat() if self.acknowledged_at else None,
            "failed_at": self.failed_at.isoformat() if self.failed_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
