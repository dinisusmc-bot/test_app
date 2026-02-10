"""
Schemas for device-related operations.
"""

from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from uuid import UUID


class DeviceBase(BaseModel):
    """Base device schema."""
    name: str = Field(..., min_length=1, max_length=100)
    device_type: str = Field(..., pattern="^(drone|sensor|camera|vehicle)$")
    status: str = Field(default="online", pattern="^(online|offline|maintenance)$")
    location_lat: Optional[float] = Field(default=None, ge=-90, le=90, alias="lat")
    location_lon: Optional[float] = Field(default=None, ge=-180, le=180, alias="lon")
    zone: Optional[str] = Field(default=None, max_length=50)
    extra_data: Dict[str, Any] = Field(default_factory=dict)


class DeviceCreate(DeviceBase):
    """Schema for creating a new device."""
    pass


class DeviceUpdate(BaseModel):
    """Schema for updating a device."""
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    status: Optional[str] = Field(default=None, pattern="^(online|offline|maintenance)$")
    location_lat: Optional[float] = Field(default=None, ge=-90, le=90, alias="lat")
    location_lon: Optional[float] = Field(default=None, ge=-180, le=180, alias="lon")
    zone: Optional[str] = Field(default=None, max_length=50)
    extra_data: Optional[Dict[str, Any]] = Field(default=None)
    is_active: Optional[bool] = None


class DeviceResponse(DeviceBase):
    """Schema for device response."""
    id: UUID
    is_active: bool
    last_seen: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True


class DeviceListResponse(BaseModel):
    """Schema for device list response."""
    devices: list[DeviceResponse]
    total: int
