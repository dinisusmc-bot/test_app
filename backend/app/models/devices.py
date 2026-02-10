"""
Device model for Command & Control API.
"""

from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, Enum, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base


class Device(Base):
    """Device model representing physical devices in the system."""

    __tablename__ = "devices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    device_type = Column(String(50), nullable=False)  # drone, sensor, camera, vehicle
    status = Column(String(20), nullable=False, default="online")  # online, offline, maintenance
    location_lat = Column(Float, nullable=True)  # LA/San Diego area
    location_lon = Column(Float, nullable=True)
    last_seen = Column(DateTime, default=datetime.utcnow)
    extra_data = Column(JSON, default=dict)
    zone = Column(String(50), nullable=True)  # LA, San Diego, etc.
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "name": self.name,
            "device_type": self.device_type,
            "status": self.status,
            "location_lat": self.location_lat,
            "location_lon": self.location_lon,
            "last_seen": self.last_seen.isoformat() if self.last_seen else None,
            "extra_data": self.extra_data,
            "zone": self.zone,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
