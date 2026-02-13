"""
Utility functions for the Command & Control API.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
import random
from app.models.asset import Asset


def generate_lat_lon(area: str = "la") -> tuple:
    """Generate random coordinates in specified area."""
    if area == "la":
        # Los Angeles area: 33.7-34.5, -118.5--117.5
        lat = random.uniform(33.7, 34.5)
        lon = random.uniform(-118.5, -117.5)
    elif area == "san_diego":
        # San Diego area: 32.5-33.2, -117.5--116.8
        lat = random.uniform(32.5, 33.2)
        lon = random.uniform(-117.5, -116.8)
    else:
        # Default to LA
        lat = random.uniform(33.7, 34.5)
        lon = random.uniform(-118.5, -117.5)
    
    return round(lat, 6), round(lon, 6)


def get_zone(lat: float, lon: float) -> str:
    """Determine zone based on coordinates."""
    if 33.7 <= lat <= 34.5 and -118.5 <= lon <= -117.5:
        return "LA"
    elif 32.5 <= lat <= 33.2 and -117.5 <= lon <= -116.8:
        return "San Diego"
    return "Unknown"


def generate_simulated_device(device_type: str = None, area: str = "la") -> Dict[str, Any]:
    """Generate a simulated device with random data."""
    if device_type is None:
        device_type = random.choice(["drone", "sensor", "camera", "vehicle"])
    
    lat, lon = generate_lat_lon(area)
    zone = get_zone(lat, lon)
    
    device_status = random.choice(["online", "online", "online", "offline", "maintenance"])
    
    return {
        "name": f"{device_type.title()}-{zone[:2].upper()}-{random.randint(100, 999)}",
        "device_type": device_type,
        "status": device_status,
        "location_lat": lat,
        "location_lon": lon,
        "zone": zone,
        "metadata": {
            "battery_level": random.randint(10, 100),
            "signal_strength": random.randint(1, 100),
            "firmware_version": f"{random.randint(1, 3)}.{random.randint(0, 9)}.{random.randint(0, 99)}",
            "last_maintenance": (datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0).isoformat()),
        },
    }


def generate_simulated_location(zone: str = "LA") -> Dict[str, Any]:
    """Generate a simulated location."""
    lat, lon = generate_lat_lon("la" if zone == "LA" else "san_diego")
    
    area_types = ["urban", "suburban", "industrial"]
    area_type = random.choice(area_types)
    
    addresses = {
        "LA": ["Downtown LA", "Santa Monica", "Long Beach", "Hollywood", "Beverly Hills"],
        "San Diego": ["Downtown SD", "La Jolla", "Coronado", "San Diego International Airport", "Gaslamp Quarter"]
    }
    address = random.choice(addresses.get(zone, ["Unknown Location"]))
    
    return {
        "name": f"{zone} {area_type.title()} Zone {random.randint(1, 20)}",
        "address": address,
        "location_lat": lat,
        "location_lon": lon,
        "area_type": area_type,
        "zone": zone,
    }


def generate_simulated_event(device_id: str, event_type: str = None) -> Dict[str, Any]:
    """Generate a simulated event."""
    if event_type is None:
        event_type = random.choice(["alert", "status_change", "command_ack"])
    
    severities = {
        "alert": random.choice(["info", "warning", "critical"]),
        "status_change": "info",
        "command_ack": "info",
    }
    
    details = {
        "alert": {"message": f"Alert from device {device_id[:8]}...", "threshold_exceeded": random.choice(["battery", "signal", "temperature"])},
        "status_change": {"old_status": random.choice(["online", "offline", "maintenance"]), "new_status": random.choice(["online", "offline", "maintenance"])},
        "command_ack": {"command_id": f"cmd-{random.randint(1000, 9999)}", "acknowledged_by": "system"},
    }
    
    return {
        "device_id": device_id,
        "event_type": event_type,
        "details": details[event_type],
        "severity": severities[event_type],
    }


def generate_simulated_command(device_id: str, command_type: str = None) -> Dict[str, Any]:
    """Generate a simulated command."""
    if command_type is None:
        command_type = random.choice(["patrol", "survey", "return", "stop", "resume"])
    
    return {
        "device_id": device_id,
        "command_type": command_type,
        "payload": {
            "duration_minutes": random.randint(5, 120),
            "waypoints": [
                {"lat": random.uniform(33.7, 34.5), "lon": random.uniform(-118.5, -117.5)}
                for _ in range(random.randint(2, 5))
            ],
        },
    }


def generate_simulated_asset(asset_type: str = None, area: str = "la", is_friendly: bool = True) -> Dict[str, Any]:
    """Generate a simulated asset with random data."""
    if asset_type is None:
        asset_type = random.choice(["drone", "sensor", "camera", "vehicle"])
    
    lat, lon = generate_lat_lon(area)
    zone = get_zone(lat, lon)
    
    asset_status = random.choice(["available", "available", "available", "in_use", "maintenance", "offline"])
    
    return {
        "name": f"{'Friendly' if is_friendly else 'Enemy'}-{asset_type.title()}-{zone[:2].upper()}-{random.randint(100, 999)}",
        "asset_type": asset_type,
        "status": asset_status,
        "lat": lat,
        "lon": lon,
        "zone": zone,
        "is_friendly": is_friendly,
        "extra_data": {
            "battery_level": random.randint(10, 100),
            "signal_strength": random.randint(1, 100),
            "firmware_version": f"{random.randint(1, 3)}.{random.randint(0, 9)}.{random.randint(0, 99)}",
            "last_maintenance": (datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0).isoformat()),
        },
    }


def generate_simulated_engagement(friendly: Optional[Asset] = None, enemy: Optional[Asset] = None) -> Dict[str, Any]:
    """Generate a simulated engagement."""
    friendly_id = str(friendly.id) if isinstance(friendly, Asset) else friendly.get('id', None) if isinstance(friendly, dict) else None
    enemy_id = str(enemy.id) if isinstance(enemy, Asset) else enemy.get('id', None) if isinstance(enemy, dict) else None
    friendly_name = friendly.get('name', '???')[:8] if isinstance(friendly, dict) else (friendly.name[:8] if friendly else '???')
    enemy_name = enemy.get('name', '???')[:8] if isinstance(enemy, dict) else (enemy.name[:8] if enemy else '???')
    
    return {
        "name": f"Engagement-{friendly_name}-to-{enemy_name}",
        "friendly_id": friendly_id,
        "enemy_id": enemy_id,
        "status": "pending",
        "progress": 0,
        "details": {
            "engagement_type": random.choice(["missile", "surveillance", "interception"]),
            "estimated_completion_minutes": random.randint(5, 60),
        },
    }
