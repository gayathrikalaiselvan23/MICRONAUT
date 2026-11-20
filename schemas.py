from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class TelemetryCreate(BaseModel):
    device_id: str = Field(min_length=1, max_length=80)
    water_temperature: float | None = None
    ph: float | None = Field(default=None, ge=0, le=14)
    turbidity: float | None = Field(default=None, ge=0)
    tds: float | None = Field(default=None, ge=0)
    dissolved_oxygen: float | None = Field(default=None, ge=0)
    depth: float | None = Field(default=None, ge=0)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    recorded_at: datetime | None = None

class TelemetryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    device_id: str
    water_temperature: float | None
    ph: float | None
    turbidity: float | None
    tds: float | None
    dissolved_oxygen: float | None
    depth: float | None
    latitude: float | None
    longitude: float | None
    recorded_at: datetime

class DetectionCreate(BaseModel):
    device_id: str
    label: str
    confidence: float = Field(ge=0, le=1)
    image_name: str | None = None
    is_pollutant: bool = False
    notes: str | None = None

class DetectionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    device_id: str
    label: str
    confidence: float
    image_name: str | None
    is_pollutant: bool
    notes: str | None
    detected_at: datetime

class DeviceStatusUpdate(BaseModel):
    device_id: str
    is_online: bool = True
    battery_percent: float | None = Field(default=None, ge=0, le=100)
    operating_mode: str = "monitoring"

class DeviceStatusRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    device_id: str
    is_online: bool
    battery_percent: float | None
    operating_mode: str
    last_seen: datetime

class SummaryRead(BaseModel):
    telemetry_records: int
    detections: int
    pollutant_detections: int
    active_devices: int
