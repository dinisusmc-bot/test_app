"""
Engagement model for GeoMap Simulation API.
Tracks friendly-enemy interactions and missile engagements.
"""

from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.database import Base


class Engagement(Base):
    """Engagement model representing friendly-enemy interactions."""

    __tablename__ = "engagements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    friendly_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=True)
    enemy_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=True)
    status = Column(String(20), nullable=False, default="pending")  # pending, active, completed, cancelled
    progress = Column(Float, default=0)  # 0-100%
    estimated_completion = Column(DateTime, nullable=True)
    details = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    friendly = relationship("Asset", foreign_keys=[friendly_id], backref="friendly_engagements")
    enemy = relationship("Asset", foreign_keys=[enemy_id], backref="enemy_engagements")

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "name": self.name,
            "friendly_id": str(self.friendly_id) if self.friendly_id else None,
            "enemy_id": str(self.enemy_id) if self.enemy_id else None,
            "status": self.status,
            "progress": self.progress,
            "estimated_completion": self.estimated_completion.isoformat() if self.estimated_completion else None,
            "details": self.details,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
