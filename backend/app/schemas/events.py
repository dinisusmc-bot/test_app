"""
Schemas for event-related operations.
"""

from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from uuid import UUID


class EventBase(BaseModel):
    """Base event schema."""
    device_id: UUID
    location_id: Optional[UUID] = None
    event_type: str = Field(..., pattern="^(alert|status_change|command_ack)$")
    details: Dict[str, Any] = Field(default_factory=dict)
    severity: Optional[str] = Field(default=None, pattern="^(info|warning|critical)$")
    resolved: Optional[str] = Field(default="pending", pattern="^(pending|resolved|ignored)$")


class EventCreate(EventBase):
    """Schema for creating a new event."""
    pass


class EventResponse(EventBase):
    """Schema for event response."""
    id: UUID
    timestamp: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class EventListResponse(BaseModel):
    """Schema for event list response."""
    events: list[EventResponse]
    total: int


class EventDeviceResponse(BaseModel):
    """Schema for events by device."""
    device_id: UUID
    events: list[EventResponse]
    total: int
