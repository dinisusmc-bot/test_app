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

## Files Updated

- `backend/schema.sql` - Fixed to use SQL comment syntax
- `docker-compose.yml` - Removed version field, updated healthcheck
- `backend/app/config.py` - Fixed CORS_ORIGINS to use string with parser
- `frontend/nginx.conf` - Removed top-level directives, kept only server block
