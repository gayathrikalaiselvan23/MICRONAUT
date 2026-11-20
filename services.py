from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.orm import Session
from app import models, schemas

def create_telemetry(db: Session, payload: schemas.TelemetryCreate):
    values = payload.model_dump(exclude_unset=True)
    if values.get("recorded_at") is None:
        values["recorded_at"] = datetime.utcnow()
    row = models.Telemetry(**values)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

def list_telemetry(
    db: Session, device_id: str | None = None, limit: int = 100
):
    query = db.query(models.Telemetry)
    if device_id:
        query = query.filter(models.Telemetry.device_id == device_id)
    return query.order_by(models.Telemetry.recorded_at.desc()).limit(limit).all()

def create_detection(db: Session, payload: schemas.DetectionCreate):
    row = models.Detection(**payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

def list_detections(db: Session, pollutants_only: bool = False, limit: int = 100):
    query = db.query(models.Detection)
    if pollutants_only:
        query = query.filter(models.Detection.is_pollutant.is_(True))
    return query.order_by(models.Detection.detected_at.desc()).limit(limit).all()

def update_device(db: Session, payload: schemas.DeviceStatusUpdate):
    row = db.query(models.DeviceStatus).filter_by(
        device_id=payload.device_id
    ).first()
    values = payload.model_dump()
    values["last_seen"] = datetime.utcnow()
    if row is None:
        row = models.DeviceStatus(**values)
        db.add(row)
    else:
        for key, value in values.items():
            setattr(row, key, value)
    db.commit()
    db.refresh(row)
    return row

def get_summary(db: Session):
    telemetry_count = db.query(func.count(models.Telemetry.id)).scalar() or 0
    detection_count = db.query(func.count(models.Detection.id)).scalar() or 0
    pollutant_count = (
        db.query(func.count(models.Detection.id))
        .filter(models.Detection.is_pollutant.is_(True)).scalar() or 0
    )
    active_count = (
        db.query(func.count(models.DeviceStatus.id))
        .filter(models.DeviceStatus.is_online.is_(True)).scalar() or 0
    )
    return {
        "telemetry_records": telemetry_count,
        "detections": detection_count,
        "pollutant_detections": pollutant_count,
        "active_devices": active_count,
    }

def get_recent_telemetry(db: Session, hours: int = 24):
    cutoff = datetime.utcnow() - timedelta(hours=hours)
    return (
        db.query(models.Telemetry)
        .filter(models.Telemetry.recorded_at >= cutoff)
        .order_by(models.Telemetry.recorded_at.desc())
        .all()
    )
