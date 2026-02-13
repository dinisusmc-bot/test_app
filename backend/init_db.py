"""
Database initialization script for GeoMap Simulation API.
"""

import asyncio
from sqlalchemy import text
from app.database import engine, get_session
from app.models.asset import Asset
from app.models.engagement import Engagement
from app.models.event import Event
from app.models.command import Command
from app.utils.data_generator import (
    generate_simulated_asset,
    generate_simulated_engagement,
)


async def init_db():
    """Initialize the database with tables and sample data."""
    async with engine.begin() as conn:
        # Create tables
        await conn.run_sync(Asset.metadata.create_all)
        await conn.run_sync(Engagement.metadata.create_all)
        await conn.run_sync(Event.metadata.create_all)
        await conn.run_sync(Command.metadata.create_all)
    
    # Generate and insert sample data
    async for session in get_session():
        try:
            # Generate sample assets (friendly)
            sample_assets = []
            for _ in range(5):
                asset_data = generate_simulated_asset(area="la", is_friendly=True)
                asset = Asset(**asset_data)
                session.add(asset)
                sample_assets.append(asset)
            
            for _ in range(3):
                asset_data = generate_simulated_asset(area="san_diego", is_friendly=True)
                asset = Asset(**asset_data)
                session.add(asset)
                sample_assets.append(asset)
            
            await session.commit()
            
            # Generate sample engagements
            for i in range(3):
                if i < len(sample_assets) and i + 3 < len(sample_assets):
                    engagement_data = generate_simulated_engagement(
                        friendly=sample_assets[i], 
                        enemy=sample_assets[i + 3]
                    )
                    engagement = Engagement(**engagement_data)
                    session.add(engagement)
            
            await session.commit()
            
            print(f"Created {len(sample_assets)} sample assets")
            print(f"Created 3 sample engagements")
            
            return {"assets": len(sample_assets), "engagements": 3}
        except Exception as e:
            await session.rollback()
            raise


async def main():
    """Main entry point."""
    result = await init_db()
    print(f"Database initialized: {result}")


if __name__ == "__main__":
    asyncio.run(main())
