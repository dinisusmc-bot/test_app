"""
Schemas for command-related operations.
"""

from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from uuid import UUID


class CommandBase(BaseModel):
    """Base command schema."""
    device_id: UUID
    location_id: Optional[UUID] = None
    command_type: str = Field(..., pattern="^(patrol|survey|return|stop|resume)$")
    payload: Dict[str, Any] = Field(default_factory=dict)


class CommandCreate(CommandBase):
    """Schema for creating a new command."""
    pass


class CommandResponse(CommandBase):
    """Schema for command response."""
    id: UUID
    status: str = Field(..., pattern="^(pending|sent|acknowledged|failed)$")
    error_message: Optional[str] = None
    acknowledged_at: Optional[datetime] = None
    failed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CommandListResponse(BaseModel):
    """Schema for command list response."""
    commands: list[CommandResponse]
    total: int


class CommandUpdate(BaseModel):
    """Schema for updating command status."""
    status: str = Field(..., pattern="^(acknowledged|failed)$")
    error_message: Optional[str] = None
