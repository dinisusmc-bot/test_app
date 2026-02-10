"""
Database initialization script for Command & Control API.
"""

import asyncio
from sqlalchemy import text
from app.database import engine
from app.models.devices import Device
from app.models.locations import Location
from app.models.events import Event
from app.models.commands import Command
from app.utils.data_generator import (
    generate_simulated_device,
    generate_simulated_location,
)


async def init_db():
    """Initialize the database with tables and sample data."""
    async with engine.begin() as conn:
        # Create tables
        await conn.run_sync(Device.metadata.create_all)
        await conn.run_sync(Location.metadata.create_all)
        await conn.run_sync(Event.metadata.create_all)
        await conn.run_sync(Command.metadata.create_all)
        
        # Generate sample devices
        sample_devices = [
            generate_simulated_device(area="la") for _ in range(5)
        ] + [
            generate_simulated_device(area="san_diego") for _ in range(3)
        ]
        
        # Generate sample locations
        sample_locations = [
            generate_simulated_location(zone="LA") for _ in range(5)
        ] + [
            generate_simulated_location(zone="San Diego") for _ in range(3)
        ]
        
        print(f"Created {len(sample_devices)} sample devices")
        print(f"Created {len(sample_locations)} sample locations")
        
        return {"devices": len(sample_devices), "locations": len(sample_locations)}


async def main():
    """Main entry point."""
    result = await init_db()
    print(f"Database initialized: {result}")


if __name__ == "__main__":
    asyncio.run(main())
