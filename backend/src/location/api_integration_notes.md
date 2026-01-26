# Step 8.6 — How APIs Will Use the Location Resolver (Step 9)

## Goal
When the user calls the API with:
- name
- birth_date
- birth_time
- birth_place (text)

The backend should automatically:
1) Resolve location (lat/lon/tz)
2) Run astrology calculator
3) Generate report
4) Return results (or return IDs)

---

## API Inputs (User-Friendly)
User sends only:
- name
- date (YYYY-MM-DD)
- time (HH:MM:SS)
- place (example: "Visakhapatnam, India")

User should NOT send:
- latitude
- longitude
- timezone_offset

---

## Backend Internal Flow (What the API does behind the scenes)

### Step 1: Validate input
- Ensure name/date/time/place are present
- If missing, return a clear error (400)

### Step 2: Call Location Resolver
Input:
- place string
- (optional) date/time for historical offset

Output:
- latitude
- longitude
- timezone_name
- timezone_offset

If resolver fails:
- return error and STOP (do not run calculator)

### Step 3: Run Chart Calculation
Run multi_system_calculator using:
- name, date, time, place
- resolved lat, lon, tz_offset

Output:
- chart JSON (store it or return it)

### Step 4: Generate Combined Report
Run generate_combined_report using:
- chart JSON file

Output:
- report Markdown (store it or return it)

---

## Suggested API Endpoints (Step 9)

### Endpoint A: Create chart
POST /charts/calculate

Request body:
- name
- date
- time
- place

Response:
- chart_id (recommended) OR chart_json

---

### Endpoint B: Generate report
POST /reports/combined

Request body:
- chart_id

Response:
- report_markdown

---

## India MVP Rules
- timezone_name must be Asia/Kolkata
- timezone_offset must be +5.5
- place must be place of birth only

---

## Error Messages (User-Friendly)
Place not found:
- "Place not found. Please provide City, State, India"

Ambiguous place:
- "Multiple matches found. Please specify State and Country."

Missing fields:
- "Missing required fields: date/time/place"
