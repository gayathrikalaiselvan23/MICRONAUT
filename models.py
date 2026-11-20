from datetime import datetime
from sqlalchemy import (
    Boolean, DateTime, Float, Integer, String, Text, func
)
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Telemetry(Base):
    __tablename__ = "telemetry"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    device_id: Mapped[str] = mapped_column(String(80), index=True)
    water_temperature: Mapped[float | None] = mapped_column(Float, nullable=True)
    ph: Mapped[float | None] = mapped_column(Float, nullable=True)
    turbidity: Mapped[float | None] = mapped_column(Float, nullable=True)
    tds: Mapped[float | None] = mapped_column(Float, nullable=True)
    dissolved_oxygen: Mapped[float | None] = mapped_column(Float, nullable=True)
    depth: Mapped[float | None] = mapped_column(Float, nullable=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

class Detection(Base):
    __tablename__ = "detections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    device_id: Mapped[str] = mapped_column(String(80), index=True)
    label: Mapped[str] = mapped_column(String(120), index=True)
    confidence: Mapped[float] = mapped_column(Float)
    image_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_pollutant: Mapped[bool] = mapped_column(Boolean, default=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    detected_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )

class DeviceStatus(Base):
    __tablename__ = "device_status"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    device_id: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    is_online: Mapped[bool] = mapped_column(Boolean, default=False)
    battery_percent: Mapped[float | None] = mapped_column(Float, nullable=True)
    operating_mode: Mapped[str] = mapped_column(String(40), default="standby")
    last_seen: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
