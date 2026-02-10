"""
Location model for Command & Control API.
"""

from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base


class Location(Base):
    """Location model representing physical locations in the system."""

    __tablename__ = "locations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=True)
    location_lat = Column(Float, nullable=False)  # LA/San Diego area
    location_lon = Column(Float, nullable=False)
    area_type = Column(String(20), nullable=True)  # urban, suburban, industrial
    zone = Column(String(50), nullable=True)  # LA, San Diego, etc.
    metadata = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "name": self.name,
            "address": self.address,
            "location_lat": self.location_lat,
            "location_lon": self.location_lon,
            "area_type": self.area_type,
            "zone": self.zone,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
