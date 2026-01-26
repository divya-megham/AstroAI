# Location Resolver – Test Cases & Validation

## Purpose
These test cases validate that the location resolver correctly converts
birth place names into latitude, longitude, and timezone details
before astrology calculations.

---

## Test Cases (India)

### Test Case 1
Input:
- place: "Visakhapatnam, India"

Expected Output:
- latitude: approx 17.6868
- longitude: approx 83.2185
- timezone_name: Asia/Kolkata
- timezone_offset: +5.5

---

### Test Case 2
Input:
- place: "Hyderabad, India"

Expected Output:
- latitude: approx 17.3850
- longitude: approx 78.4867
- timezone_name: Asia/Kolkata
- timezone_offset: +5.5

---

### Test Case 3
Input:
- place: "Vijayawada, India"

Expected Output:
- latitude: approx 16.5062
- longitude: approx 80.6480
- timezone_name: Asia/Kolkata
- timezone_offset: +5.5

---

### Test Case 4
Input:
- place: "Delhi, India"

Expected Output:
- latitude: approx 28.6139
- longitude: approx 77.2090
- timezone_name: Asia/Kolkata
- timezone_offset: +5.5

---

### Test Case 5
Input:
- place: "Tirupati, India"

Expected Output:
- latitude: approx 13.6288
- longitude: approx 79.4192
- timezone_name: Asia/Kolkata
- timezone_offset: +5.5

---

## Validation Rules

- Resolver MUST return latitude and longitude for valid places
- Resolver MUST return Asia/Kolkata for all Indian locations
- Resolver MUST return timezone offset +5.5
- Resolver MUST NOT guess values if place is unclear
- Resolver MUST fail gracefully with a clear message if place is not found

---

## Failure Scenarios

### Invalid Place
Input:
- place: "RandomUnknownPlace"

Expected Behavior:
- Return error: "Place not found. Please provide city and country."

---

### Ambiguous Place
Input:
- place: "Rajahmundry"

Expected Behavior:
- Ask user for more details (state or country)
- Do NOT auto-select a random location
