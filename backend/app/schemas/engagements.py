"""
Schemas for engagement-related operations.
"""

from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from uuid import UUID


class EngagementBase(BaseModel):
    """Base engagement schema."""
    name: str = Field(..., min_length=1, max_length=100)
    friendly_id: Optional[UUID] = Field(default=None, description="Friendly asset ID")
    enemy_id: Optional[UUID] = Field(default=None, description="Enemy asset ID")
    status: str = Field(default="pending", pattern="^(pending|active|completed|cancelled|engaging|missile_in_flight)$")
    progress: float = Field(default=0, ge=0, le=100, description="Progress percentage (0-100)")
    estimated_completion: Optional[datetime] = None
    details: Dict[str, Any] = Field(default_factory=dict)


class EngagementCreate(EngagementBase):
    """Schema for creating a new engagement."""
    pass


class EngagementUpdate(BaseModel):
    """Schema for updating an engagement."""
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    friendly_id: Optional[UUID] = Field(default=None)
    enemy_id: Optional[UUID] = Field(default=None)
    status: Optional[str] = Field(default=None, pattern="^(pending|active|completed|cancelled|engaging|missile_in_flight)$")
    progress: Optional[float] = Field(default=None, ge=0, le=100)
    estimated_completion: Optional[datetime] = None
    details: Optional[Dict[str, Any]] = Field(default=None)


class EngagementResponse(EngagementBase):
    """Schema for engagement response."""
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EngagementListResponse(BaseModel):
    """Schema for engagement list response."""
    engagements: list[EngagementResponse]
    total: int
