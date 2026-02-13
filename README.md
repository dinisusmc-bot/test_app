# Command & Control System - Test Application

A full-stack application for monitoring and managing assets across geospatial zones.

## Overview

This system provides:
- **Real-time asset monitoring** with geospatial visualization
- **Engagement tracking** with friendly/enemy asset relationships
- **REST API** for asset and engagement management
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
│   │   ├── models/   # SQLAlchemy models (Assets, Engagements, Events, Commands)
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

The system includes simulated asset data:

### Assets
- Multiple friendly assets (green markers)
- Multiple enemy assets (red markers)
- Assets across LA and San Diego zones

### Engagements
- Active engagement records
- Friendly/enemy pairing relationships

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
- Phase 3: Documentation ✅
- Phase 4: E2E Tests ✅

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
