# test_app - Deployment Tasks

## Project: Command & Control System

### Issues Found

#### test_app
1. **Missing docker-compose.yml** - No container orchestration for backend + frontend
2. **Missing Dockerfile for backend** - Cannot containerize the FastAPI app
3. **Missing Dockerfile for frontend** - Cannot containerize the React app
4. **Backend needs .env.example** - Missing environment template

### Tasks to Fix and Deploy

#### Phase 1: Containerization
- [ ] Create Dockerfile for backend (FastAPI)
- [ ] Create Dockerfile for frontend (React + Vite)
- [ ] Create docker-compose.yml to orchestrate both services

#### Phase 2: Environment Configuration
- [ ] Create backend/.env.example with all required variables
- [ ] Document environment variables in README

#### Phase 3: Documentation
- [ ] Add deployment section to README
- [ ] Document Docker Compose usage
- [ ] Add troubleshooting section

### Estimated Deployment Steps

```bash
# Development
cd backend && uvicorn app.main:app --reload --port 45847
cd frontend && npm run dev

# Production with Docker Compose
docker-compose up -d
```

### Services
- Backend: FastAPI on port 45847
- Frontend: React on port 5173 (development) / port 80 (production)
