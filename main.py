from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import create_tables
from app.routers import telemetry, detections, devices, dashboard

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Tables are created for this starter project.
    # For production, use Alembic migrations instead.
    create_tables()
    yield

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="REST API backend for MICRONAUT aquatic monitoring.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this to your dashboard URL in production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

prefix = settings.API_PREFIX
app.include_router(telemetry.router, prefix=prefix)
app.include_router(detections.router, prefix=prefix)
app.include_router(devices.router, prefix=prefix)
app.include_router(dashboard.router, prefix=prefix)

@app.get("/")
def root():
    return {
        "project": "MICRONAUT",
        "message": "Aquatic monitoring API is running",
        "docs": "/docs",
    }

@app.get("/health")
def health():
    return {"status": "ok"}
