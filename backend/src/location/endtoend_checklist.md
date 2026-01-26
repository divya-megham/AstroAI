# Step 8.5 — End-to-End Validation Checklist (India MVP)

## Goal
Confirm the pipeline works end-to-end using only:
- name
- birth_date
- birth_time
- birth_place (text)

And produces:
- chart JSON
- combined report Markdown

---

## Pre-Checks
- Virtual environment is active (.venv)
- multi_system_calculator.py works
- generate_combined_report.py works
- Location resolver is ready to return lat/lon/tz for India places

---

## End-to-End Test Case (Primary)

### User Input (what the user will type)
- name: TestUser1
- birth_date: 1999-11-13
- birth_time: 16:20:00
- birth_place: "Visakhapatnam, India"

### Expected Resolver Output
- latitude: approx 17.6868
- longitude: approx 83.2185
- timezone_name: Asia/Kolkata
- timezone_offset: +5.5

### Expected System Result
- chart JSON is generated successfully
- combined report Markdown is generated successfully

---

## End-to-End Test Case (Secondary)

### User Input
- name: TestUser2
- birth_date: 2000-05-10
- birth_time: 09:15:00
- birth_place: "Hyderabad, India"

### Expected Resolver Output
- latitude: approx 17.3850
- longitude: approx 78.4867
- timezone_name: Asia/Kolkata
- timezone_offset: +5.5

### Expected System Result
- chart JSON is generated successfully
- combined report Markdown is generated successfully

---

## Validation Rules (Pass/Fail)

PASS if:
- place string converts to lat/lon
- timezone_name is Asia/Kolkata
- timezone_offset is +5.5
- chart JSON is produced with required top-level keys
- report is produced and is readable

FAIL if:
- resolver guesses a random location
- resolver returns missing/empty lat/lon
- calculator runs with incorrect or missing timezone
- report generation fails

---

## Negative Test (Not Found)

### Input
- birth_place: "RandomUnknownPlace"

Expected behavior:
- Resolver returns a clear error message:
  "Place not found. Please provide City, State, India"
- Calculator and report generation do NOT run

---

## Ambiguous Test (Needs Clarification)

### Input
- birth_place: "Rajahmundry"

Expected behavior:
- Resolver asks user to specify:
  "Rajahmundry, Andhra Pradesh, India"
- System does NOT proceed until clarified
