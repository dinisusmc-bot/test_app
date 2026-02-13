"""
API endpoints for v1.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from typing import List, Optional

from app.database import get_session
from app.models.asset import Asset
from app.models.engagement import Engagement
from app.models.event import Event
from app.models.command import Command
from app.schemas.assets import AssetCreate, AssetUpdate, AssetResponse, AssetListResponse
from app.schemas.engagements import EngagementCreate, EngagementUpdate, EngagementResponse, EngagementListResponse
from app.schemas.events import EventCreate, EventResponse
from app.schemas.commands import CommandCreate, CommandResponse

router = APIRouter(tags=["v1"])


# Assets endpoints
@router.get("/assets", response_model=AssetListResponse)
async def list_assets(
    session: AsyncSession = Depends(get_session),
    zone: str = None,
    status: str = None,
    is_friendly: bool = None,
    limit: int = 100,
    offset: int = 0,
):
    """List all assets."""
    stmt = select(Asset)
    
    if zone:
        stmt = stmt.where(Asset.zone == zone)
    if status:
        stmt = stmt.where(Asset.status == status)
    if is_friendly is not None:
        stmt = stmt.where(Asset.is_friendly == is_friendly)
    
    result = await session.execute(stmt.offset(offset).limit(limit))
    assets = result.scalars().all()
    
    return {"assets": assets, "total": len(assets)}


@router.get("/assets/{asset_id}", response_model=AssetResponse)
async def get_asset(
    asset_id: str,
    session: AsyncSession = Depends(get_session),
):
    """Get asset by ID."""
    asset = await session.get(Asset, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@router.post("/assets", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
async def create_asset(
    asset: AssetCreate,
    session: AsyncSession = Depends(get_session),
):
    """Create a new asset."""
    db_asset = Asset(**asset.model_dump())
    session.add(db_asset)
    await session.commit()
    await session.refresh(db_asset)
    return db_asset


@router.put("/assets/{asset_id}", response_model=AssetResponse)
async def update_asset(
    asset_id: str,
    asset: AssetUpdate,
    session: AsyncSession = Depends(get_session),
):
    """Update an asset."""
    db_asset = await session.get(Asset, asset_id)
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    update_data = asset.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_asset, key, value)
    
    await session.commit()
    await session.refresh(db_asset)
    return db_asset


@router.delete("/assets/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_asset(
    asset_id: str,
    session: AsyncSession = Depends(get_session),
):
    """Delete an asset (soft delete)."""
    asset = await session.get(Asset, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    asset.is_active = False
    await session.commit()
    return None


@router.get("/assets/nearby", response_model=List[AssetResponse])
async def get_nearby_assets(
    lat: float,
    lon: float,
    radius_km: float = 100,
    is_friendly: Optional[bool] = None,
    session: AsyncSession = Depends(get_session),
):
    """Get assets within radius."""
    # Get all assets
    stmt = select(Asset)
    if is_friendly is not None:
        stmt = stmt.where(Asset.is_friendly == is_friendly)
    
    result = await session.execute(stmt)
    assets = result.scalars().all()
    
    # Filter by distance (simplified calculation)
    nearby = []
    for asset in assets:
        if asset.lat and asset.lon:
            # Simple Euclidean distance approximation
            lat_diff = abs(asset.lat - lat)
            lon_diff = abs(asset.lon - lon)
            distance = (lat_diff ** 2 + lon_diff ** 2) ** 0.5 * 111  # Approx km
            
            if distance <= radius_km:
                nearby.append(asset)
    
    return nearby


# Engagements endpoints
@router.get("/engagements", response_model=EngagementListResponse)
async def list_engagements(
    session: AsyncSession = Depends(get_session),
    status: str = None,
    friendly_id: str = None,
    enemy_id: str = None,
    limit: int = 100,
    offset: int = 0,
):
    """List all engagements."""
    stmt = select(Engagement)
    
    if status:
        stmt = stmt.where(Engagement.status == status)
    if friendly_id:
        stmt = stmt.where(Engagement.friendly_id == friendly_id)
    if enemy_id:
        stmt = stmt.where(Engagement.enemy_id == enemy_id)
    
    result = await session.execute(stmt.offset(offset).limit(limit))
    engagements = result.scalars().all()
    
    return {"engagements": engagements, "total": len(engagements)}


@router.get("/engagements/{engagement_id}", response_model=EngagementResponse)
async def get_engagement(
    engagement_id: str,
    session: AsyncSession = Depends(get_session),
):
    """Get engagement by ID."""
    engagement = await session.get(Engagement, engagement_id)
    if not engagement:
        raise HTTPException(status_code=404, detail="Engagement not found")
    return engagement


@router.post("/engagements", response_model=EngagementResponse, status_code=status.HTTP_201_CREATED)
async def create_engagement(
    engagement: EngagementCreate,
    session: AsyncSession = Depends(get_session),
):
    """Create a new engagement."""
    db_engagement = Engagement(**engagement.model_dump())
    session.add(db_engagement)
    await session.commit()
    await session.refresh(db_engagement)
    return db_engagement


@router.put("/engagements/{engagement_id}", response_model=EngagementResponse)
async def update_engagement(
    engagement_id: str,
    engagement: EngagementUpdate,
    session: AsyncSession = Depends(get_session),
):
    """Update an engagement."""
    db_engagement = await session.get(Engagement, engagement_id)
    if not db_engagement:
        raise HTTPException(status_code=404, detail="Engagement not found")
    
    update_data = engagement.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_engagement, key, value)
    
    await session.commit()
    await session.refresh(db_engagement)
    return db_engagement


@router.delete("/engagements/{engagement_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_engagement(
    engagement_id: str,
    session: AsyncSession = Depends(get_session),
):
    """Delete an engagement."""
    engagement = await session.get(Engagement, engagement_id)
    if not engagement:
        raise HTTPException(status_code=404, detail="Engagement not found")
    
    await session.delete(engagement)
    await session.commit()
    return None


# Engagement actions endpoints
@router.post("/engagements/{engagement_id}/confirm", response_model=EngagementResponse)
async def confirm_engagement(
    engagement_id: str,
    session: AsyncSession = Depends(get_session),
):
    """Confirm an engagement."""
    engagement = await session.get(Engagement, engagement_id)
    if not engagement:
        raise HTTPException(status_code=404, detail="Engagement not found")
    
    if engagement.status != "pending":
        raise HTTPException(status_code=400, detail="Engagement must be in pending status")
    
    engagement.status = "active"
    engagement.progress = 0
    await session.commit()
    await session.refresh(engagement)
    return engagement


@router.post("/engagements/{engagement_id}/abort", response_model=EngagementResponse)
async def abort_engagement(
    engagement_id: str,
    session: AsyncSession = Depends(get_session),
):
    """Abort an engagement."""
    engagement = await session.get(Engagement, engagement_id)
    if not engagement:
        raise HTTPException(status_code=404, detail="Engagement not found")
    
    if engagement.status not in ["pending", "active"]:
        raise HTTPException(status_code=400, detail="Engagement must be in pending or active status")
    
    engagement.status = "cancelled"
    await session.commit()
    await session.refresh(engagement)
    return engagement


@router.post("/engagements/{engagement_id}/engage", response_model=EngagementResponse)
async def engage_target(
    engagement_id: str,
    session: AsyncSession = Depends(get_session),
):
    """Start engagement (missile launch)."""
    engagement = await session.get(Engagement, engagement_id)
    if not engagement:
        raise HTTPException(status_code=404, detail="Engagement not found")
    
    if engagement.status != "active":
        raise HTTPException(status_code=400, detail="Engagement must be confirmed before engaging")
    
    engagement.status = "engaging"
    await session.commit()
    await session.refresh(engagement)
    return engagement


@router.post("/engagements/{engagement_id}/complete", response_model=EngagementResponse)
async def complete_engagement(
    engagement_id: str,
    session: AsyncSession = Depends(get_session),
):
    """Mark engagement as complete."""
    engagement = await session.get(Engagement, engagement_id)
    if not engagement:
        raise HTTPException(status_code=404, detail="Engagement not found")
    
    if engagement.status != "engaging":
        raise HTTPException(status_code=400, detail="Engagement must be engaging to be completed")
    
    engagement.status = "completed"
    engagement.progress = 100
    await session.commit()
    await session.refresh(engagement)
    return engagement


@router.post("/engagements/{engagement_id}/missile-launch", response_model=EngagementResponse)
async def launch_missile(
    engagement_id: str,
    session: AsyncSession = Depends(get_session),
):
    """Simulate missile launch."""
    engagement = await session.get(Engagement, engagement_id)
    if not engagement:
        raise HTTPException(status_code=404, detail="Engagement not found")
    
    if engagement.status != "engaging":
        raise HTTPException(status_code=400, detail="Engagement must be in engaging status")
    
    # Update status to reflect missile in flight
    engagement.status = "missile_in_flight"
    engagement.progress = 0
    await session.commit()
    await session.refresh(engagement)
    return engagement


# Events endpoints
@router.get("/events", response_model=List[EventResponse])
async def list_events(
    session: AsyncSession = Depends(get_session),
    event_type: str = None,
    severity: str = None,
    limit: int = 100,
    offset: int = 0,
):
    """List all events."""
    query = session.query(Event)
    
    if event_type:
        query = query.filter(Event.event_type == event_type)
    if severity:
        query = query.filter(Event.severity == severity)
    
    events = await session.execute(query.offset(offset).limit(limit))
    return events.scalars().all()


@router.get("/events/asset/{asset_id}", response_model=List[EventResponse])
async def get_asset_events(
    asset_id: str,
    session: AsyncSession = Depends(get_session),
):
    """Get events for an asset."""
    events = await session.execute(
        session.query(Event).filter(Event.asset_id == asset_id)
    )
    return events.scalars().all()


@router.get("/events/engagement/{engagement_id}", response_model=List[EventResponse])
async def get_engagement_events(
    engagement_id: str,
    session: AsyncSession = Depends(get_session),
):
    """Get events for an engagement."""
    events = await session.execute(
        session.query(Event).filter(Event.engagement_id == engagement_id)
    )
    return events.scalars().all()


@router.post("/events", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(
    event: EventCreate,
    session: AsyncSession = Depends(get_session),
):
    """Create a new event."""
    db_event = Event(**event.model_dump())
    session.add(db_event)
    await session.commit()
    await session.refresh(db_event)
    return db_event


# Commands endpoints
@router.get("/commands", response_model=List[CommandResponse])
async def list_commands(
    session: AsyncSession = Depends(get_session),
    status: str = None,
    limit: int = 100,
    offset: int = 0,
):
    """List all commands."""
    query = session.query(Command)
    
    if status:
        query = query.filter(Command.status == status)
    
    commands = await session.execute(query.offset(offset).limit(limit))
    return commands.scalars().all()


@router.get("/commands/asset/{asset_id}", response_model=List[CommandResponse])
async def get_asset_commands(
    asset_id: str,
    session: AsyncSession = Depends(get_session),
):
    """Get commands for an asset."""
    commands = await session.execute(
        session.query(Command).filter(Command.asset_id == asset_id)
    )
    return commands.scalars().all()


@router.get("/commands/engagement/{engagement_id}", response_model=List[CommandResponse])
async def get_engagement_commands(
    engagement_id: str,
    session: AsyncSession = Depends(get_session),
):
    """Get commands for an engagement."""
    commands = await session.execute(
        session.query(Command).filter(Command.engagement_id == engagement_id)
    )
    return commands.scalars().all()


@router.post("/commands", response_model=CommandResponse, status_code=status.HTTP_201_CREATED)
async def create_command(
    command: CommandCreate,
    session: AsyncSession = Depends(get_session),
):
    """Create a new command."""
    db_command = Command(**command.model_dump())
    session.add(db_command)
    await session.commit()
    await session.refresh(db_command)
    return db_command


@router.get("/commands/{command_id}", response_model=CommandResponse)
async def get_command(
    command_id: str,
    session: AsyncSession = Depends(get_session),
):
    """Get command by ID."""
    command = await session.get(Command, command_id)
    if not command:
        raise HTTPException(status_code=404, detail="Command not found")
    return command
