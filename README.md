# Command & Control System

A full-stack application for monitoring and managing devices across LA and San Diego areas.

## Overview

This system provides:
- **Real-time device monitoring** with geospatial visualization
- **REST API** for device management
- **WebSocket** for real-time status updates
- **Simulated data** for testing and development

## Architecture

```
┌─────────────────┐
│   Frontend      │  React + TypeScript + MapLibre
│   (Port 5173)   │
└────────┬────────┘
         │ HTTP/WebSocket
         ▼
┌─────────────────┐
│   Backend       │  FastAPI + PostgreSQL
│   (Port 45847)  │
└─────────────────┘
```

## Project Structure

```
test_app/
├── backend/          # FastAPI backend
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/   # SQLAlchemy models
│   │   ├── schemas/  # Pydantic schemas
│   │   ├── api/      # API endpoints
│   │   └── utils/
│   ├── tests/
│   ├── requirements.txt
│   └── README.md
├── frontend/         # React frontend
│   ├── src/
│   ├── package.json
│   └── README.md
├── tasks.json        # Task tracking
└── README.md         # This file
```

## Quick Start

### Backend

```bash
cd backend
cp .env.example .env
# Edit .env with your database credentials

pip install -r requirements.txt
uvicorn app.main:app --reload --port 45847
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## API Documentation

- **Backend**: `http://localhost:45847/docs`
- **Health Check**: `http://localhost:45847/health`

## Sample Data

The system includes 8 simulated devices:

### LA Area (5 devices)
- Camera-LA-347 (online)
- Camera-LA-717 (maintenance)
- Camera-LA-404 (offline)
- Sensor-LA-401 (offline)
- Sensor-LA-660 (maintenance)

### San Diego Area (3 devices)
- Vehicle-SA-624 (maintenance)
- Drone-SA-980 (online)
- Drone-SA-310 (online)

## Technologies

### Backend
- **FastAPI** - Modern async web framework
- **SQLAlchemy** - ORM for PostgreSQL
- **asyncpg** - Async PostgreSQL driver
- **Pydantic** - Data validation

### Frontend
- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **MapLibre GL JS** - Interactive maps
- **axios** - HTTP client

## Tasks

See `tasks.json` for the complete task list:
- Phase 1: Backend Setup ✅
- Phase 2: Frontend Setup ✅
- Phase 3: Documentation 🟡
- Phase 4: E2E Tests (pending)

## Development

### Database Initialization

```bash
cd backend
python init_db.py
```

### Running Tests

```bash
# Backend
cd backend
pytest tests/

# Frontend
cd frontend
npm run test
```

## Deployment

See individual project READMEs for deployment instructions:
- [Backend README](backend/README.md)
- [Frontend README](frontend/README.md)

## License

MIT
