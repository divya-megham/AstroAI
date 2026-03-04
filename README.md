}
# AstroAI – AI-Powered Astrology Generator

AstroAI is a backend system that generates structured astrology readings using astronomical calculations and AI (Amazon Bedrock).

The system accepts birth details and produces a multi-system astrology report including Western, Vedic, and Chinese interpretations.

---

## Features
• Generates astrology reports from birth details  
• Supports multiple astrology systems (Western, Vedic, Chinese)  
• Uses astronomical calculations for planetary positions  
• Integrates AI (Amazon Bedrock) for interpretation  
• Exposes a FastAPI backend for generating reports

---

## Architecture

User Input  
→ FastAPI API Endpoint  
→ Astrology Calculation Engine  
→ AI Interpretation (Amazon Bedrock)  
→ Structured Markdown Report

---

## Project Structure

backend/
- src/
  - api/ → API endpoints  
  - services/ → Report generation logic  
  - location/ → Place resolution  
  - scripts/ → Astrology calculation scripts  

docs/ → Documentation for astrology systems  

testuser1_chart.json → Example generated chart  
testuser1_report.md → Example astrology report output  

---

## Example Output

Example report includes:

Western Astrology  
Vedic Astrology  
Chinese Zodiac  
Annual Themes (Career, Health, Finance)
Example generated report available in testuser1_report.md.

---

## Technologies Used

Python  
FastAPI  
Amazon Bedrock  
Astronomical calculation scripts  
Markdown report generation

---

## Running the Backend

Install dependencies:

pip install -r requirements.txt

Run the API server:

uvicorn src.api.main:app --reload --port 8000

---

## Author

Divya Megham
