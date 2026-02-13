"""
Schemas for API responses.
"""

from datetime import datetime
from pydantic import BaseModel
from app.schemas.assets import AssetCreate, AssetUpdate, AssetResponse, AssetListResponse
from app.schemas.engagements import EngagementCreate, EngagementUpdate, EngagementResponse, EngagementListResponse
from app.schemas.events import EventCreate, EventResponse
from app.schemas.commands import CommandCreate, CommandResponse

__all__ = [
    "AssetCreate",
    "AssetUpdate",
    "AssetResponse",
    "AssetListResponse",
    "EngagementCreate",
    "EngagementUpdate",
    "EngagementResponse",
    "EngagementListResponse",
    "EventCreate",
    "EventResponse",
    "CommandCreate",
    "CommandResponse",
    "HealthResponse",
    "RootResponse",
]


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str


class RootResponse(BaseModel):
    """Root endpoint response."""
    name: str
    version: str
    description: str
    docs: str
    health: str
