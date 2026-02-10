# Lessons Learned - Docker Deployment Issues

## Overview
This document captures issues encountered during Docker deployment of a full-stack application (FastAPI backend, React frontend, PostgreSQL database) and their solutions.

---

## 1. Database Schema Syntax Errors

### Issue
PostgreSQL initialization failed with syntax error when using Python-style docstrings (`"""`) in SQL schema file.

### Root Cause
SQL files don't support Python-style triple-quoted strings for comments.

### Solution
Replace Python-style comments with SQL comment syntax:
```sql
-- PostgreSQL schema for Command & Control system.
```

### Lesson
Always use language-appropriate comment syntax. SQL files should use `--` for single-line comments or `/* */` for multi-line comments.

---

## 2. Docker Compose Version Deprecation

### Issue
Warning about obsolete version attribute in docker-compose.yml.

### Root Cause
Docker Compose v2+ no longer requires or uses the version field.

### Solution
Remove the `version: '3.8'` line from docker-compose.yml.

### Lesson
Stay updated with Docker Compose specification changes. The version field is deprecated.

---

## 3. PostgreSQL Healthcheck Configuration

### Issue
Backend container failed to start with "dependency postgres failed to start: container is unhealthy".

### Root Cause
Healthcheck only verified PostgreSQL user connection but not if the specific database exists.

### Solution
Update healthcheck to verify both user and database:
```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-openclaw} -d ${POSTGRES_DB:-test_app}"]
```

### Lesson
Healthchecks should verify complete service readiness. For databases, check that the specific database exists.

---

## 4. Pydantic Settings CORS Configuration

### Issue
Backend crashed with SettingsError: error parsing value for field "CORS_ORIGINS".

### Root Cause
CORS_ORIGINS was defined as `List[str]` but .env had comma-separated string.

### Solution
Change to string with property to parse it:
```python
CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

@property
def cors_origins_list(self) -> List[str]:
    if isinstance(self.CORS_ORIGINS, str):
        return [origin.strip() for origin in self.CORS_ORIGINS.split(',')]
    return self.CORS_ORIGINS
```

### Lesson
Environment variables are always strings. Provide validators or properties to handle string-to-type conversion.

---

## 5. Nginx Configuration Structure

### Issue
Frontend container restarted with "worker_processes" directive is not allowed here.

### Root Cause
Top-level nginx directives placed in `/etc/nginx/conf.d/default.conf` conflict with main nginx.conf.

### Solution
Only include server block in conf.d files:
```nginx
server {
    listen 80;
    # server configuration only
}
```

### Lesson
Files in `/etc/nginx/conf.d/` should only contain server blocks, not top-level directives.

---

## 6. Missing Pydantic Model Fields

### Issue
Backend crashed with ValidationError: Extra inputs are not permitted.

### Root Cause
.env file contained `APP_SECRET_KEY` field that wasn't defined in the Settings model.

### Solution
Add missing field to Settings model:
```python
APP_SECRET_KEY: str = "your-secret-key-here-change-in-production"
```

### Lesson
Keep Pydantic models in sync with environment files. Every field in .env should have a corresponding field in the Settings model.

---

## 7. Hardcoded URLs in Frontend

### Issue
Frontend couldn't connect to backend, showing ERR_CONNECTION_REFUSED errors to localhost:8000.

### Root Cause
Frontend was running inside Docker container. Hardcoded URLs pointed to `http://localhost:8000` - these URLs were relative to the container, not the Docker network.

### Solution
Use relative paths through nginx proxy:
```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';
```

Configure nginx to proxy these paths:
```nginx
location /api {
    proxy_pass http://backend:8000;
}
location /ws {
    proxy_pass http://backend:8000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection 'upgrade';
}
```

### Lesson
Never hardcode localhost URLs in containerized apps. Use relative paths for browser-based applications, or use Docker service names for server-to-server communication.

---

## 8. SQLAlchemy Reserved Keywords

### Issue
Backend failed to start with `InvalidRequestError: Attribute name 'metadata' is reserved when using the Declarative API`.

### Root Cause
Database schema used column name `metadata` - SQLAlchemy's Declarative Base reserves `metadata` as an attribute for table metadata.

### Solution
Rename the column to a non-reserved name:
```python
extra_data = Column(JSON, default=dict)  # Instead of metadata
```

### Lesson
Be aware of ORM reserved keywords. When designing database schemas for use with ORMs, avoid reserved words like `metadata`, `query`, `session`, etc.

---

## 9. API Response Structure Mismatch

### Issue
Frontend crashed with `TypeError: o.filter is not a function`.

### Root Cause
- Backend API returned: `{devices: [...], total: 8}`
- Frontend expected an array directly
- Frontend tried to call `.filter()` on an object instead of an array

### Solution
Transform API response in frontend:
```typescript
const response = await fetch(`${API_BASE_URL}/devices`);
const data = await response.json();
const devices = Array.isArray(data) ? data : (data as any).devices || [];
```

### Lesson
Document and validate API contracts. Ensure frontend and backend agree on response structure. Always handle unexpected data structures gracefully.

---

## 10. Database Field Name Mapping

### Issue
Frontend displayed "Invalid LngLat object: (NaN, NaN)" error when trying to render map markers.

### Root Cause
- Backend API returned: `location_lat`, `location_lon`
- Frontend expected: `lat`, `lon`
- Field name mismatch resulted in undefined values being passed to map library

### Solution
Use Pydantic field aliases:
```python
location_lat: Optional[float] = Field(alias="lat")
location_lon: Optional[float] = Field(alias="lon")

class Config:
    populate_by_name = True
```

### Lesson
Standardize naming conventions or use adapters. Either agree on consistent field names between frontend and backend, or create transformation layers. Consider using DTOs (Data Transfer Objects) to explicitly define the interface contract.

---

## Best Practices Summary

### Development Workflow
1. Start with clean state: Use `docker compose down -v` to remove volumes when schema changes
2. Incremental builds: Build one service at a time during debugging: `docker compose build backend`
3. Check logs immediately: Always run `docker compose logs <service> --tail 50` after failures
4. Test locally first: Validate SQL syntax, config files, and code before building containers

### Configuration Management
1. Environment variables: Document all required env vars in `.env.example`
2. Defaults: Provide sensible defaults for development in code, not just .env
3. Validation: Use Pydantic or similar tools to validate configuration on startup
4. Comments: Include comments explaining why certain values are needed

### Container Communication
1. Service names: Use Docker Compose service names for inter-container communication
2. Relative URLs: Use relative paths in browser-based frontends
3. Proxy setup: Configure reverse proxy (nginx) for clean routing
4. Healthchecks: Implement proper healthchecks that verify full service readiness

### Database Considerations
1. Schema syntax: Use SQL-native comment syntax in .sql files
2. Reserved words: Check ORM documentation for reserved column names
3. Migrations: Consider using Alembic or similar for schema management
4. Init scripts: Keep initialization scripts simple and idempotent
5. **Clean state**: Always run `docker compose down -v` before schema changes to remove old volumes

### Frontend-Backend Integration
1. API contracts: Document expected request/response formats
2. Field mapping: Use consistent naming or explicit transformation layers
3. Error handling: Always handle unexpected data structures gracefully
4. Type safety: Use TypeScript interfaces that match backend models

### Container Networking
1. Docker Desktop: Use `host.docker.internal` to reach host services from containers
2. Docker Compose services: Use service names for inter-container communication
3. Relative URLs: Use relative paths in browser-based frontends
4. Nginx proxy: Configure reverse proxy for clean routing

### Debugging Strategy
1. One issue at a time: Fix errors sequentially, rebuilding after each fix
2. Read error messages carefully: They usually indicate the exact problem
3. Check assumptions: Verify data structures, field names, and types match expectations
4. Browser cache: Always hard refresh (Ctrl+Shift+R) after frontend rebuilds

---

## Tools and Commands Reference

### Useful Docker Commands
```bash
# Clean slate (before schema changes)
docker compose down -v

# Build specific service
docker compose build <service> --no-cache

# View logs
docker compose logs <service> --tail 50 --follow

# Check container status
docker compose ps

# Execute command in container
docker compose exec <service> <command>

# Test API endpoint
curl -s http://localhost/api/v1/devices | jq
```

### Debugging Checklist
- [ ] Check all containers are running: `docker compose ps`
- [ ] Review startup logs: `docker compose logs --tail 50`
- [ ] Verify environment variables: `docker compose exec backend env`
- [ ] Test database connection: `docker compose exec postgres psql -U user -d db`
- [ ] Check nginx config: `docker compose exec frontend nginx -t`
- [ ] Verify API responses: `curl localhost/api/v1/devices`
- [ ] Clear browser cache and hard refresh
- [ ] Check browser console for errors

---

## Conclusion
Most issues stemmed from:
1. Impedance mismatches between technologies (Python/SQL, frontend/backend naming)
2. Configuration errors (nginx structure, Pydantic settings)
3. Container networking (hardcoded URLs, service discovery)
4. Data structure assumptions (API response format, field names)

By following these lessons and best practices, similar issues can be prevented or resolved much more quickly in future projects.

---

## Key Docker Networking Lesson

### Issue
Frontend container couldn't connect to backend services using `localhost` from within the Docker network.

### Root Cause
Inside Docker containers, `localhost` refers to the container itself, not the host machine. The Docker Compose service names (like `backend`, `postgres`) are used for inter-container communication.

### Solution
For Docker Desktop, use `host.docker.internal` to reach services running on the host machine:
- Backend API: `http://host.docker.internal:45847/api/v1`
- Database: `postgresql://postgres@host.docker.internal:5432/test_app`

For Docker Compose service-to-service communication, use service names:
- Backend from nginx: `http://backend:8000`
- Database from backend: `postgresql://...@postgres:5432/test_app`

### Lesson
- **Docker Desktop**: Use `host.docker.internal` to reach host services
- **Docker Compose services**: Use service names (`backend`, `postgres`) for container-to-container communication
- **Browser-based apps**: Use relative paths (`/api/v1`) to avoid URL issues entirely
