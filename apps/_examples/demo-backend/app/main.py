"""
FastAPI Demo Backend Application

Features:
- Health and readiness endpoints
- PostgreSQL database integration
- Prometheus metrics
- CRUD operations for items
"""

import logging
import os
import time
from contextlib import asynccontextmanager, contextmanager
from typing import List, Optional

import psycopg2
from fastapi import FastAPI, HTTPException
from prometheus_client import Counter, Gauge, Histogram, generate_latest
from pydantic import BaseModel
from starlette.responses import Response

# Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "info").upper()
DATABASE_URL = os.getenv("DATABASE_URL", "")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

# Logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# Lifespan context manager
@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Application lifespan manager."""
    db_url_display = (
        DATABASE_URL.split("@")[1] if "@" in DATABASE_URL else "Not configured"
    )
    logger.info("Starting Demo Backend v%s", APP_VERSION)
    logger.info("Database URL: %s", db_url_display)
    logger.info("Log level: %s", LOG_LEVEL)
    yield


# FastAPI app
app = FastAPI(
    title="Demo Backend",
    description="Example backend service for GitOps deployment",
    version=APP_VERSION,
    lifespan=lifespan,
)

# Prometheus metrics
http_requests_total = Counter(
    "http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"]
)
http_request_duration_seconds = Histogram(
    "http_request_duration_seconds", "HTTP request duration", ["method", "endpoint"]
)
db_connections_active = Gauge("db_connections_active", "Active database connections")


# Pydantic models
class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None


class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    version: str


# Database connection manager
@contextmanager
def get_db_connection():
    """Context manager for database connections."""
    conn = None
    try:
        db_connections_active.inc()
        conn = psycopg2.connect(DATABASE_URL)
        yield conn
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise
    finally:
        if conn:
            conn.close()
        db_connections_active.dec()


# Middleware for metrics
@app.middleware("http")
async def add_metrics(request, call_next):
    """Add Prometheus metrics to all requests."""
    start_time = time.time()

    try:
        response = await call_next(request)

        # Record metrics
        duration = time.time() - start_time
        http_requests_total.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code,
        ).inc()
        http_request_duration_seconds.labels(
            method=request.method, endpoint=request.url.path
        ).observe(duration)

        return response
    except Exception as e:
        logger.error(f"Request error: {e}")
        raise


# Routes
@app.get("/", response_model=dict)
async def root():
    """Root endpoint."""
    return {
        "message": "Demo Backend API",
        "version": APP_VERSION,
        "documentation": "/docs",
    }


@app.get("/health", response_model=HealthResponse)
async def health():
    """
    Health check endpoint (liveness probe).
    Always returns healthy if the application is running.
    """
    return HealthResponse(status="healthy", version=APP_VERSION)


@app.get("/ready", response_model=HealthResponse)
async def ready():
    """
    Readiness check endpoint (readiness probe).
    Checks database connectivity.
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
        return HealthResponse(status="ready", version=APP_VERSION)
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        raise HTTPException(status_code=503, detail="Not ready: database unavailable")


@app.get("/items", response_model=List[Item])
async def list_items():
    """List all items from database."""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, name, description FROM items ORDER BY id")
                rows = cursor.fetchall()

                return [
                    Item(id=row[0], name=row[1], description=row[2]) for row in rows
                ]
    except Exception as e:
        logger.error(f"Error listing items: {e}")
        raise HTTPException(status_code=500, detail="Database error")


@app.post("/items", response_model=Item, status_code=201)
async def create_item(item: ItemCreate):
    """Create a new item."""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO items (name, description) VALUES (%s, %s) RETURNING id",
                    (item.name, item.description),
                )
                item_id = cursor.fetchone()[0]
                conn.commit()

                return Item(id=item_id, name=item.name, description=item.description)
    except Exception as e:
        logger.error(f"Error creating item: {e}")
        raise HTTPException(status_code=500, detail="Database error")


@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """Get a specific item by ID."""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id, name, description FROM items WHERE id = %s", (item_id,)
                )
                row = cursor.fetchone()

                if not row:
                    raise HTTPException(status_code=404, detail="Item not found")

                return Item(id=row[0], name=row[1], description=row[2])
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting item: {e}")
        raise HTTPException(status_code=500, detail="Database error")


@app.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int):
    """Delete an item by ID."""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
                if cursor.rowcount == 0:
                    raise HTTPException(status_code=404, detail="Item not found")
                conn.commit()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting item: {e}")
        raise HTTPException(status_code=500, detail="Database error")


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    return Response(content=generate_latest(), media_type="text/plain")
