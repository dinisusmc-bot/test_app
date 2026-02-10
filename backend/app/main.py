"""
Command & Control API - FastAPI Application
Main entry point for the backend server.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.api.v1 import router as v1_router
from app.api.websocket import router as websocket_router

# Initialize FastAPI app
app = FastAPI(
    title="Command & Control API",
    description="API for simulated command & control system (LA/San Diego area)",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(v1_router, prefix="/api/v1")
app.include_router(websocket_router, prefix="/ws")


@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}


@app.get("/", tags=["System"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Command & Control API",
        "version": "1.0.0",
        "description": "API for simulated command & control system (LA/San Diego area)",
        "docs": "/docs",
        "health": "/health",
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
