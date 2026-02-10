"""
Schemas for location-related operations.
"""

from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from uuid import UUID


class LocationBase(BaseModel):
    """Base location schema."""
    name: str = Field(..., min_length=1, max_length=100)
    address: Optional[str] = Field(default=None, max_length=255)
    location_lat: float = Field(..., ge=-90, le=90)
    location_lon: float = Field(..., ge=-180, le=180)
    area_type: Optional[str] = Field(default=None, pattern="^(urban|suburban|industrial)$")
    zone: Optional[str] = Field(default=None, max_length=50)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class LocationCreate(LocationBase):
    """Schema for creating a new location."""
    pass


class LocationUpdate(BaseModel):
    """Schema for updating a location."""
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    address: Optional[str] = Field(default=None, max_length=255)
    location_lat: Optional[float] = Field(default=None, ge=-90, le=90)
    location_lon: Optional[float] = Field(default=None, ge=-180, le=180)
    area_type: Optional[str] = Field(default=None, pattern="^(urban|suburban|industrial)$")
    zone: Optional[str] = Field(default=None, max_length=50)
    metadata: Optional[Dict[str, Any]] = Field(default=None)


class LocationResponse(LocationBase):
    """Schema for location response."""
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LocationNearbyRequest(BaseModel):
    """Schema for nearby location search."""
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    radius_km: float = Field(default=10.0, ge=0.1, le=100.0)


class LocationNearbyResponse(BaseModel):
    """Schema for nearby location response."""
    locations: list[LocationResponse]
    total: int
