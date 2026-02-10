"""
Schemas for API responses.
"""

from datetime import datetime
from pydantic import BaseModel


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
