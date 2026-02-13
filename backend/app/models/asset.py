"""
Asset model for GeoMap Simulation API.
Represents friendly and enemy assets in the geospatial simulation system.
"""

from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, Enum, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.database import Base


class Asset(Base):
    """Asset model representing friendly or enemy assets in the system."""

    __tablename__ = "assets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    asset_type = Column(String(50), nullable=False)  # drone, sensor, camera, vehicle
    status = Column(String(20), nullable=False, default="available")  # available, in_use, maintenance, offline
    lat = Column(Float, nullable=True)  # LA/San Diego area
    lon = Column(Float, nullable=True)
    last_seen = Column(DateTime, default=datetime.utcnow)
    extra_data = Column(JSON, default=dict)
    zone = Column(String(50), nullable=True)  # LA, San Diego, etc.
    is_active = Column(Boolean, default=True)
    is_friendly = Column(Boolean, default=True)  # True for friendly, False for enemy
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "name": self.name,
            "asset_type": self.asset_type,
            "status": self.status,
            "lat": self.lat,
            "lon": self.lon,
            "last_seen": self.last_seen.isoformat() if self.last_seen else None,
            "extra_data": self.extra_data,
            "zone": self.zone,
            "is_active": self.is_active,
            "is_friendly": self.is_friendly,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
