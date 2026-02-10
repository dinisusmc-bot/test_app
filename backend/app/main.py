"""
Command & Control API - FastAPI Application
Main entry point for the backend server.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config import settings
from app.api.v1 import router as v1_router
from app.api.websocket import router as websocket_router
from app.database import get_session
from app.models.devices import Device
from app.models.locations import Location
from app.utils.data_generator import generate_simulated_device, generate_simulated_location


app = FastAPI(
    title="Command & Control API",
    description="API for simulated command & control system (LA/San Diego area)",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    """Populate database with sample data on startup."""
    from sqlalchemy import select
    try:
        # Create a new session for startup
        from app.database import async_session
        async with async_session() as session:
            # Check if data already exists
            result = await session.execute(select(Device))
            existing_devices = result.scalars().all()
            
            if len(existing_devices) < 8:
                # Generate and insert sample devices
                sample_devices = [
                    generate_simulated_device(area="la") for _ in range(5)
                ] + [
                    generate_simulated_device(area="san_diego") for _ in range(3)
                ]
                
                for device_data in sample_devices:
                    device = Device(**device_data)
                    session.add(device)
                
                # Generate and insert sample locations
                sample_locations = [
                    generate_simulated_location(zone="LA") for _ in range(5)
                ] + [
                    generate_simulated_location(zone="San Diego") for _ in range(3)
                ]
                
                for location_data in sample_locations:
                    location = Location(**location_data)
                    session.add(location)
                
                await session.commit()
    except Exception:
        pass  # Silently fail if database is not ready


# Include routers
app.include_router(v1_router, prefix="/api/v1")
app.include_router(websocket_router, prefix="/ws")


@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}


@app.get("/", tags=["System"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Command & Control API",
        "version": "1.0.0",
        "description": "API for simulated command & control system (LA/San Diego area)",
        "docs": "/docs",
        "health": "/health",
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)},
    )
