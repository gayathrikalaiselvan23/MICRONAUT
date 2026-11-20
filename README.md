# MICRONAUT – Aquatic Monitoring Backend

A GitHub-ready FastAPI REST API starter backend for the MICRONAUT project.
It receives sensor telemetry, stores AI detection results, tracks device status,
and provides summary endpoints for a dashboard. MySQL is used for persistent
storage through SQLAlchemy.

## Technology stack

- Python
- FastAPI REST API
- MySQL
- SQLAlchemy ORM
- Pydantic validation
- Uvicorn ASGI server

## Project structure

```text
MICRONAUT_GitHub_Project/
├── app/
│   ├── routers/
│   │   ├── telemetry.py
│   │   ├── detections.py
│   │   ├── devices.py
│   │   └── dashboard.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── services.py
│   └── main.py
├── database/schema.sql
├── .env.example
├── requirements.txt
└── README.md
```

## 1. Create the MySQL database

Start MySQL, then run:

```sql
CREATE DATABASE micronaut_db;
```

The application creates the required tables when it starts. Ensure the MySQL
user has permission to create and modify tables in this database.

## 2. Install dependencies

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

## 3. Configure environment

Copy `.env.example` to `.env` and update `DB_USER` and `DB_PASSWORD` with your
local MySQL credentials. Do not commit `.env` or real passwords to GitHub.

## 4. Run the API

```bash
uvicorn app.main:app --reload
```

Open the interactive API documentation:

- http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API information |
| GET | `/health` | Health check |
| POST | `/api/v1/telemetry/` | Insert sensor readings |
| GET | `/api/v1/telemetry/` | List telemetry |
| GET | `/api/v1/telemetry/recent` | Read recent telemetry |
| POST | `/api/v1/detections/` | Save AI detection |
| GET | `/api/v1/detections/` | List AI detections |
| PUT | `/api/v1/devices/status` | Update device status |
| GET | `/api/v1/devices/` | List devices |
| GET | `/api/v1/dashboard/summary` | Dashboard summary |
| GET | `/api/v1/dashboard/telemetry` | Dashboard telemetry |

## Example telemetry request

Send this JSON to `POST /api/v1/telemetry/`:

```json
{
  "device_id": "MICRONAUT-ESP32-01",
  "water_temperature": 27.4,
  "ph": 7.2,
  "turbidity": 3.8,
  "tds": 420,
  "dissolved_oxygen": 6.5,
  "depth": 1.2,
  "latitude": 10.01,
  "longitude": 78.12
}
```

The values above are illustrative test data, not live sensor readings or
water-quality certification values.

## Example AI detection request

Send this JSON to `POST /api/v1/detections/`:

```json
{
  "device_id": "MICRONAUT-ESP32-01",
  "label": "possible_microplastic",
  "confidence": 0.91,
  "image_name": "sample_frame_001.jpg",
  "is_pollutant": true,
  "notes": "Example model output; verify using the project's validated model."
}
```

## Architecture

ESP32 / sensors / camera / AI edge device
    → communication layer
    → FastAPI REST API
    → MySQL database
    → React dashboard

This repository implements the backend API and database layer. Hardware
drivers, acoustic modem communication, YOLO model inference, robot control,
and the React dashboard must be integrated with the actual project hardware
and software separately.

## Important implementation notes

- The API accepts structured telemetry; it does not directly read ESP32 pins.
- The detection endpoint stores model results; it does not run YOLO inference.
- Replace permissive CORS settings with your dashboard origin before deployment.
- Use environment variables for secrets.
- For production, add authentication, authorization, migrations, logging,
  rate limiting, and HTTPS.
- Validate sensor calibration and detection accuracy independently.
