# Backend - Command & Control API

FastAPI backend with PostgreSQL for simulated command & control data.

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration (database, API keys)
│   ├── database.py          # PostgreSQL connection
│   ├── models/              # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── devices.py       # Device model
│   │   ├── locations.py     # Location model
│   │   ├── events.py        # Event model
│   │   └── commands.py      # Command model
│   ├── schemas/             # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── devices.py
│   │   ├── locations.py
│   │   ├── events.py
│   │   └── commands.py
│   ├── api/                 # API endpoints
│   │   ├── __init__.py
│   │   ├── v1.py            # v1 API routes
│   │   └── websocket.py     # WebSocket for real-time updates
│   └── utils/               # Helper functions
│       ├── __init__.py
│       └── data_generator.py  # Simulated data generation
├── tests/                   # Tests
│   ├── __init__.py
│   └── test_api.py
├── alembic/                 # Database migrations
├── requirements.txt
├── Dockerfile
└── .env.example
```

## Core Models

### Device
- Device ID
- Name, type, status
- Location coordinates (LA/San Diego area)
- Last seen timestamp
- Metadata

### Location
- Location ID
- Name, address
- Coordinates (lat/lon)
- Area type (urban, suburban, industrial)
- Zone assignments

### Event
- Event ID
- Device ID, location ID
- Event type (alert, status_change, command_ack)
- Timestamp
- Details

### Command
- Command ID
- Device ID, location ID
- Command type
- Payload
- Status (pending, sent, acknowledged, failed)
- Timestamps

## API Endpoints (v1)

### Devices
- `GET /api/v1/devices` - List all devices
- `GET /api/v1/devices/{id}` - Get device details
- `POST /api/v1/devices` - Create device
- `PUT /api/v1/devices/{id}` - Update device
- `DELETE /api/v1/devices/{id}` - Delete device

### Locations
- `GET /api/v1/locations` - List all locations
- `GET /api/v1/locations/{id}` - Get location details
- `GET /api/v1/locations/nearby` - Find locations near coordinates

### Events
- `GET /api/v1/events` - List events
- `GET /api/v1/events/device/{device_id}` - Events for device
- `POST /api/v1/events` - Create event

### Commands
- `GET /api/v1/commands` - List commands
- `POST /api/v1/commands` - Send command
- `GET /api/v1/commands/{id}` - Get command status

## Simulated Data

### LA Area Devices
- 50 devices across Greater LA
- Types: drone, sensor, camera, vehicle
- Locations: Downtown, Santa Monica, Long Beach, etc.

### San Diego Area Devices
- 30 devices across San Diego
- Types: drone, sensor, camera, vehicle
- Locations: Downtown, La Jolla, Coronado, etc.

## Quick Start

```bash
cd backend
cp .env.example .env
# Edit .env with your database credentials

pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Testing

```bash
pytest tests/
```
