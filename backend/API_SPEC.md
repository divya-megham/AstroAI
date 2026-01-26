# AstroAI Backend API Spec (v1)

## Overview
This backend exposes APIs to generate:
1) Astrology chart data (JSON)
2) Full combined astrology reading (Markdown)

The backend accepts user-friendly inputs:
- name
- birth_date
- birth_time
- birth_place (text)

The backend internally resolves:
- latitude / longitude / timezone

Then runs the existing scripts:
- multi_system_calculator.py
- generate_combined_report.py

---

## Endpoint 1 — Health Check
GET /health

Response 200:
{
  "status": "ok"
}

---

## Endpoint 2 — Resolve Location (India MVP)
POST /location/resolve

Request:
{
  "place": "Visakhapatnam, India",
  "date": "1999-11-13",
  "time": "16:20:00"
}

Response 200:
{
  "place": "Visakhapatnam, India",
  "latitude": 17.6868,
  "longitude": 83.2185,
  "timezone_name": "Asia/Kolkata",
  "timezone_offset": 5.5
}

Errors:
- 400 if place/date/time missing
- 404 if place not found
- 409 if ambiguous (needs clarification)

---

## Endpoint 3 — Calculate Chart
POST /charts/calculate

Request:
{
  "name": "TestUser1",
  "date": "1999-11-13",
  "time": "16:20:00",
  "place": "Visakhapatnam, India",
  "ayanamsa": "raman"
}

Response 200:
{
  "chart_id": "chart_YYYYMMDD_HHMMSS_random",
  "meta": {
    "name": "TestUser1",
    "birth_date": "1999-11-13",
    "birth_time": "16:20:00",
    "birth_place": "Visakhapatnam, India"
  }
}

Notes:
- The full chart JSON is stored on the backend (file or database).
- The response returns chart_id + minimal meta.

Errors:
- 400 missing fields
- 404 place not found
- 500 calculator error

---

## Endpoint 4 — Generate Combined Reading Report
POST /reports/combined

Request:
{
  "chart_id": "chart_YYYYMMDD_HHMMSS_random"
}

Response 200:
{
  "chart_id": "chart_YYYYMMDD_HHMMSS_random",
  "report_markdown": "....full markdown content...."
}

Errors:
- 404 chart_id not found
- 500 report generation error

---

## Optional Endpoint 5 — One Shot (Chart + Report)
POST /reading/generate

Request:
{
  "name": "TestUser1",
  "date": "1999-11-13",
  "time": "16:20:00",
  "place": "Visakhapatnam, India",
  "ayanamsa": "raman"
}

Response 200:
{
  "chart_id": "chart_YYYYMMDD_HHMMSS_random",
  "chart_json": { ...optional... },
  "report_markdown": "....full markdown content...."
}

Notes:
- For MVP, this is the simplest user experience.
- For scale, split into /charts and /reports.

---

## Data Storage (MVP)
Store per chart_id:
- chart JSON file
- report Markdown file
- input request payload

Suggested folder structure:
backend/data/
  charts/
  reports/

---

## Determinism Rules
- Chart JSON is the source of truth
- Reports must be derived from chart JSON
- AI models must not invent placements or dates
