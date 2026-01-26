# Step 8.4 — Location Resolver Integration Plan

## Goal
Allow users to enter only:
- name
- birth_date
- birth_time
- birth_place (text)

Then automatically resolve:
- latitude
- longitude
- timezone_name
- timezone_offset

And then run the existing astrology calculator + report generator.

---

## Current Workflow (Manual)
User provides:
- name, date, time, place, lat, lon, tz_offset

Then system runs:
1) multi_system_calculator.py (creates chart JSON)
2) generate_combined_report.py (creates report Markdown)

Problem: users do not know lat/lon/tz.

---

## New Workflow (After Step 8)
User provides ONLY:
- name
- date (YYYY-MM-DD)
- time (HH:MM:SS)
- place (example: "Visakhapatnam, India")

System automatically performs:

### 1) Resolve Location
Input:
- place string

Output:
- latitude
- longitude
- timezone_name
- timezone_offset

### 2) Run Chart Calculation
Use resolved values to run:
- multi_system_calculator.py with:
  --lat
  --lon
  --tz
  --place

Output:
- chart JSON file (example: chart.json)

### 3) Generate Final Reading
Run:
- generate_combined_report.py using the chart JSON

Output:
- report Markdown file (example: report.md)

---

## Integration Rules (India MVP)
- timezone_name MUST be Asia/Kolkata
- timezone_offset MUST be +5.5
- Use place of birth only (not current location)

---

## Error Handling Rules
If location resolution fails:
- Do NOT run calculator
- Return a clear error message:
  "Place not found. Please provide City, State, India"

If multiple matches:
- Ask user to clarify (add state/country)

Never guess coordinates.

---

## Definition of Done (Step 8 Complete)
Step 8 is complete when:
- User enters only name, date, time, place
- Resolver returns valid lat/lon/tz
- Calculator runs successfully using resolved values
- Combined report is generated successfully
