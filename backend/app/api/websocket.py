"""
WebSocket endpoints for real-time updates.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from typing import Dict, Set
import json
import asyncio

router = APIRouter(prefix="/ws", tags=["WebSocket"])


class ConnectionManager:
    """Manages WebSocket connections."""

    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, channel: str = "all"):
        """Accept new WebSocket connection."""
        await websocket.accept()
        if channel not in self.active_connections:
            self.active_connections[channel] = set()
        self.active_connections[channel].add(websocket)

    def disconnect(self, websocket: WebSocket, channel: str = "all"):
        """Remove WebSocket connection."""
        if channel in self.active_connections:
            self.active_connections[channel].discard(websocket)

    async def send_to_channel(self, channel: str, message: dict):
        """Send message to all connections in a channel."""
        if channel in self.active_connections:
            message_json = json.dumps(message)
            for connection in self.active_connections.copy()[channel]:
                try:
                    await connection.send_text(message_json)
                except Exception:
                    self.disconnect(connection, channel)


manager = ConnectionManager()


@router.websocket("/devices/{device_id}")
async def device_websocket(websocket: WebSocket, device_id: str):
    """WebSocket for device-specific updates."""
    await manager.connect(websocket, f"device:{device_id}")
    
    try:
        while True:
            # Handle incoming messages
            data = await websocket.receive_text()
            
            # Echo back
            await websocket.send_text(f"Received: {data}")
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, f"device:{device_id}")


@router.websocket("/all")
async def all_updates_websocket(websocket: WebSocket):
    """WebSocket for all system updates."""
    await manager.connect(websocket, "all")
    
    try:
        while True:
            # Send periodic heartbeat
            await asyncio.sleep(30)
            await websocket.send_text(json.dumps({"type": "heartbeat", "timestamp": asyncio.get_event_loop().time()}))
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, "all")


@router.get("/broadcast")
async def broadcast_message(message: dict):
    """Broadcast message to all connections."""
    await manager.send_to_channel("all", message)
    return {"status": "broadcast sent"}
