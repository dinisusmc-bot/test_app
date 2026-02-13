"""
Schemas for asset-related operations.
"""

from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from uuid import UUID


class AssetBase(BaseModel):
    """Base asset schema."""
    name: str = Field(..., min_length=1, max_length=100)
    asset_type: str = Field(..., pattern="^(drone|sensor|camera|vehicle)$")
    status: str = Field(default="available", pattern="^(available|in_use|maintenance|offline)$")
    lat: Optional[float] = Field(default=None, ge=-90, le=90)
    lon: Optional[float] = Field(default=None, ge=-180, le=180)
    zone: Optional[str] = Field(default=None, max_length=50)
    is_friendly: Optional[bool] = Field(default=True)
    is_active: Optional[bool] = Field(default=True)
    extra_data: Dict[str, Any] = Field(default_factory=dict)


class AssetCreate(AssetBase):
    """Schema for creating a new asset."""
    pass


class AssetUpdate(BaseModel):
    """Schema for updating an asset."""
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    asset_type: Optional[str] = Field(default=None, pattern="^(drone|sensor|camera|vehicle)$")
    status: Optional[str] = Field(default=None, pattern="^(available|in_use|maintenance|offline)$")
    lat: Optional[float] = Field(default=None, ge=-90, le=90)
    lon: Optional[float] = Field(default=None, ge=-180, le=180)
    zone: Optional[str] = Field(default=None, max_length=50)
    is_friendly: Optional[bool] = None
    is_active: Optional[bool] = None
    extra_data: Optional[Dict[str, Any]] = None


class AssetResponse(AssetBase):
    """Schema for asset response."""
    id: UUID
    last_seen: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True


class AssetListResponse(BaseModel):
    """Schema for asset list response."""
    assets: list[AssetResponse]
    total: int
