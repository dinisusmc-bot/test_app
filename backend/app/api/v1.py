"""
API endpoints for v1.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_session
from app.models.devices import Device
from app.models.locations import Location
from app.models.events import Event
from app.models.commands import Command
from app.schemas.devices import DeviceCreate, DeviceUpdate, DeviceResponse, DeviceListResponse
from app.schemas.locations import LocationCreate, LocationResponse, LocationNearbyRequest, LocationNearbyResponse
from app.schemas.events import EventCreate, EventResponse, EventDeviceResponse
from app.schemas.commands import CommandCreate, CommandResponse

router = APIRouter(tags=["v1"])


# Devices endpoints
@router.get("/devices", response_model=DeviceListResponse)
async def list_devices(
    session: AsyncSession = Depends(get_session),
    zone: str = None,
    status: str = None,
    limit: int = 100,
    offset: int = 0,
):
    """List all devices."""
    from sqlalchemy import select
    stmt = select(Device).where(Device.is_active == True)
    
    if zone:
        stmt = stmt.where(Device.zone == zone)
    if status:
        stmt = stmt.where(Device.status == status)
    
    result = await session.execute(stmt.offset(offset).limit(limit))
    devices = result.scalars().all()
    
    return {"devices": devices, "total": len(devices)}


@router.get("/devices/{device_id}", response_model=DeviceResponse)
async def get_device(
    device_id: str,
    session: AsyncSession = Depends(get_session),
):
    """Get device by ID."""
    device = await session.get(Device, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.post("/devices", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
async def create_device(
    device: DeviceCreate,
    session: AsyncSession = Depends(get_session),
):
    """Create a new device."""
    db_device = Device(**device.model_dump())
    session.add(db_device)
    await session.commit()
    await session.refresh(db_device)
    return db_device


@router.put("/devices/{device_id}", response_model=DeviceResponse)
async def update_device(
    device_id: str,
    device: DeviceUpdate,
    session: AsyncSession = Depends(get_session),
):
    """Update a device."""
    db_device = await session.get(Device, device_id)
    if not db_device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    update_data = device.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_device, key, value)
    
    await session.commit()
    await session.refresh(db_device)
    return db_device


@router.delete("/devices/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device(
    device_id: str,
    session: AsyncSession = Depends(get_session),
):
    """Delete a device (soft delete)."""
    device = await session.get(Device, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    device.is_active = False
    await session.commit()
    return None


# Locations endpoints
@router.get("/locations", response_model=List[LocationResponse])
async def list_locations(
    session: AsyncSession = Depends(get_session),
    zone: str = None,
):
    """List all locations."""
    from sqlalchemy import select
    stmt = select(Location)
    
    if zone:
        stmt = stmt.where(Location.zone == zone)
    
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/locations/{location_id}", response_model=LocationResponse)
async def get_location(
    location_id: str,
    session: AsyncSession = Depends(get_session),
):
    """Get location by ID."""
    location = await session.get(Location, location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location


@router.post("/locations", response_model=LocationResponse, status_code=status.HTTP_201_CREATED)
async def create_location(
    location: LocationCreate,
    session: AsyncSession = Depends(get_session),
):
    """Create a new location."""
    db_location = Location(**location.model_dump())
    session.add(db_location)
    await session.commit()
    await session.refresh(db_location)
    return db_location


@router.get("/locations/nearby", response_model=List[LocationResponse])
async def get_nearby_locations(
    request: LocationNearbyRequest,
    session: AsyncSession = Depends(get_session),
):
    """Get locations within radius."""
    # Simplified - in production, use PostgreSQL PostGIS for geospatial queries
    locations = await session.execute(session.query(Location))
    locations = locations.scalars().all()
    
    # Filter by distance (simplified calculation)
    nearby = []
    for loc in locations:
        if loc.location_lat and loc.location_lon:
            # Simple Euclidean distance approximation
            lat_diff = abs(loc.location_lat - request.lat)
            lon_diff = abs(loc.location_lon - request.lon)
            distance = (lat_diff ** 2 + lon_diff ** 2) ** 0.5 * 111  # Approx km
            
            if distance <= request.radius_km:
                nearby.append(loc)
    
    return nearby


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


@router.get("/events/device/{device_id}", response_model=List[EventResponse])
async def get_device_events(
    device_id: str,
    session: AsyncSession = Depends(get_session),
):
    """Get events for a device."""
    events = await session.execute(
        session.query(Event).filter(Event.device_id == device_id)
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
