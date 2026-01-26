---
name: multi-system-astrology
description: Generate comprehensive astrology reports combining Vedic (Indian Sidereal), Western (Tropical), and Chinese astrology. Uses Raman ayanamsa by default. Creates birth charts with Nakshatras, planetary positions, Vimshottari Dasha, 2026 transits, Mercury retrogrades, and synthesized predictions. Outputs professional PDF or Markdown reports.
---

# Multi-System Astrology Skill

Generate comprehensive astrology reports combining **Vedic (Indian Sidereal)**, **Western (Tropical)**, and **Chinese** astrology systems.

## Overview

| System | Focus | Key Features |
|--------|-------|--------------|
| **Vedic** | Moon-based, karmic | Nakshatras, Rashis, Vimshottari Dasha |
| **Western** | Sun-based, psychological | Tropical zodiac, Transits, Retrogrades |
| **Chinese** | Year-based, elemental | 12 Animals, 5 Elements, Yin/Yang |

## Installation

```bash
pip install pyswisseph pytz --break-system-packages
```

## Quick Start

```bash
python3 scripts/multi_system_calculator.py \
    --name "Person Name" \
    --date "1998-11-26" \
    --time "08:34:00" \
    --lat 16.9891 \
    --lon 82.2475 \
    --tz 5.5 \
    --place "Kakinada, India" \
    --ayanamsa raman \
    --output report.json
```

## Ayanamsa Options

| Code | Name | Description |
|------|------|-------------|
| `raman` | B.V. Raman | **DEFAULT** - Traditional Indian astrologers |
| `lahiri` | Lahiri/Chitrapaksha | Government of India standard |
| `kp` | Krishnamurti | KP System practitioners |
| `yukteshwar` | Sri Yukteshwar | Some traditional schools |
| `true_chitra` | True Chitrapaksha | Astronomically precise |

**Why Raman is Default:** Many traditional Indian family astrologers use Raman or similar ayanamsa values (~22.4°). Lahiri (~23.8°) is the government standard but can differ by ~1.4° which affects Pada calculations near boundaries.

## Scripts

### Primary: `multi_system_calculator.py`

Generates comprehensive JSON with all three systems.

**Required Arguments:**
- `--name` - Person's name
- `--date` - Birth date (YYYY-MM-DD)
- `--time` - Birth time (HH:MM:SS, 24-hour)
- `--lat` - Latitude (decimal)
- `--lon` - Longitude (decimal)
- `--tz` - Timezone offset from UTC

**Optional Arguments:**
- `--place` - Birth place name
- `--ayanamsa` - Ayanamsa system (default: raman)
- `--output` - Output file (default: stdout)

### Report Generators

```bash
# Generate Markdown
python3 scripts/generate_markdown.py data.json --output report.md

# Generate LaTeX → PDF
python3 scripts/generate_latex.py data.json --output report.tex
pdflatex report.tex
```

## Output Structure

```json
{
  "meta": { "name", "birth_date", "birth_time", "birth_place", ... },
  "vedic": {
    "ayanamsa": 22.39,
    "ayanamsa_type": "B.V. Raman",
    "ascendant": { "rashi": {...}, "nakshatra": {...} },
    "planets": {
      "moon": { "rashi": {...}, "nakshatra": {...}, "pada": 3, ... },
      "sun": {...}, "mars": {...}, ...
    }
  },
  "western": {
    "ascendant": { "sign": "Capricorn", "degree": "4°36'" },
    "planets": { "sun": { "sign": "Sagittarius", ... }, ... }
  },
  "chinese": {
    "animal": "Tiger",
    "element": "Earth", 
    "yin_yang": "Yang",
    "full": "Earth Tiger"
  },
  "vimshottari_dasha": {
    "current_dasha": "Jupiter",
    "moon_nakshatra": "Dhanishtha",
    "periods": [...]
  },
  "transits_2026": {
    "mercury_retrogrades": [
      { "start": "2026-02-26", "end": "2026-03-20", "sign": "Pisces" },
      { "start": "2026-06-29", "end": "2026-07-23", "sign": "Cancer" },
      { "start": "2026-10-24", "end": "2026-11-13", "sign": "Scorpio" }
    ],
    "major_transits": [...],
    "eclipses": [...],
    "chinese_year": { "animal": "Horse", "element": "Fire" }
  }
}
```

## Key Calculations

### Vedic (Sidereal)

**Nakshatra:** Moon longitude ÷ 13.333° = Nakshatra index (0-26)
**Pada:** Position in Nakshatra × 4 ÷ 13.333° = Pada (1-4)
**Rashi:** Moon longitude ÷ 30° = Rashi index (0-11)

### Western (Tropical)

Uses equinox-based zodiac. Positions are ~22-24° ahead of sidereal.

### Chinese

- **Animal:** (Year - 4) mod 12 → Rat, Ox, Tiger, etc.
- **Element:** (Year - 4) mod 10 ÷ 2 → Wood, Fire, Earth, Metal, Water
- **2026:** Fire Horse year (starts Feb 17, 2026)

## 2026 Key Dates

| Date | Event |
|------|-------|
| Feb 13 | Saturn enters Aries |
| Feb 17 | Chinese New Year (Fire Horse) |
| Feb 26 - Mar 20 | Mercury Retrograde (Pisces) |
| Apr 25 | Uranus enters Gemini |
| Jun 1 | Jupiter enters Cancer (Vedic) |
| Jun 29 - Jul 23 | Mercury Retrograde (Cancer) |
| Jun 30 | Jupiter enters Leo (Western) |
| Oct 24 - Nov 13 | Mercury Retrograde (Scorpio) |
| Oct 31 | Jupiter enters Leo (Vedic) |
| Dec 5 | Rahu-Ketu shift to Capricorn-Cancer |

## Example: Complete Workflow

```python
import json
import subprocess

# Step 1: Generate data
subprocess.run([
    "python3", "scripts/multi_system_calculator.py",
    "--name", "Eswar Prasad Saladi",
    "--date", "1998-11-26",
    "--time", "08:34:00",
    "--lat", "16.9891",
    "--lon", "82.2475",
    "--tz", "5.5",
    "--place", "Kakinada, Andhra Pradesh, India",
    "--ayanamsa", "raman",
    "--output", "eswar.json"
])

# Step 2: Load and use
with open("eswar.json") as f:
    data = json.load(f)

vedic = data["vedic"]
western = data["western"]
chinese = data["chinese"]
dasha = data["vimshottari_dasha"]

print(f"=== {data['meta']['name']} ===")
print(f"Vedic Moon: {vedic['planets']['moon']['nakshatra']['name']} Pada {vedic['planets']['moon']['nakshatra']['pada']}")
print(f"Vedic Moon Sign: {vedic['planets']['moon']['rashi']['full_name']}")
print(f"Western Sun: {western['planets']['sun']['sign']['sign']}")
print(f"Chinese: {chinese['full']}")
print(f"Current Dasha: {dasha['current_dasha']} Mahadasha")
```

## Report Sections

A complete report includes:

1. **Executive Summary** - Core signature from all systems
2. **Vedic Analysis** - Nakshatra, Pada, Rashi, Navamsa, characteristics
3. **Western Analysis** - Sun sign, rising, planetary aspects
4. **Chinese Profile** - Animal, element, year compatibility
5. **Planetary Positions** - Tables for both systems
6. **Vimshottari Dasha** - Current and upcoming periods
7. **2026 Predictions** - Synthesized from all systems
8. **Month-by-Month Playbook** - Practical guidance
9. **Key Dates** - Retrogrades, eclipses, transits
10. **Remedies** - Gemstones, mantras, colors

## File Structure

```
vedic-astrology/
├── SKILL.md                          # This documentation
├── scripts/
│   ├── multi_system_calculator.py    # Main calculator (all 3 systems)
│   ├── vedic_calculator.py           # Vedic-only (legacy)
│   ├── generate_latex.py             # PDF report generator
│   └── generate_markdown.py          # Markdown report generator
├── references/
│   └── nakshatras.md                 # Complete Nakshatra data
└── assets/
    └── report_template.tex           # LaTeX template
```

## Notes

1. **Ayanamsa Matters:** ~1.4° difference between Raman and Lahiri can change Pada near boundaries
2. **Birth Time:** Even 2-4 minutes can change Ascendant and house positions
3. **Timezone:** Use the timezone at birth location (account for DST)
4. **Consistency:** Use same ayanamsa your family tradition uses
