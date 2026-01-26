# Location Resolver (Step 8)

## Purpose
Convert birth place text into latitude, longitude, and timezone
before running the astrology calculator.

## Input
- place (string) – example: "Visakhapatnam, India"
- date (YYYY-MM-DD)
- time (HH:MM:SS)

## Output
- latitude (decimal)
- longitude (decimal)
- timezone_name (Asia/Kolkata)
- timezone_offset (+5.5)

## Data Source
- OpenStreetMap (Nominatim)

## Rules
- Use place of birth, not current location
- If place not found, ask user for more details
- Never guess coordinates
