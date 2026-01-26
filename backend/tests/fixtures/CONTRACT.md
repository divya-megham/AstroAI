# Output Contract – Astrology Engine (v1)

## 1. Chart JSON Acceptance Criteria

The astrology chart JSON output is considered VALID only if all the following conditions are met.

### 1.1 Top-level structure
The JSON output MUST contain the following top-level keys:
- meta
- vedic
- western
- chinese
- vimshottari_dasha
- transits_2026

If any of these keys are missing, the output is INVALID.

---

### 1.2 Meta section requirements
The `meta` object MUST contain:
- name
- birth_date
- birth_time
- birth_place
- latitude
- longitude
- timezone_offset
- generated_at

This section ensures traceability and reproducibility of the chart.

---

### 1.3 Vedic astrology section requirements
The `vedic` object MUST contain:
- ascendant
- planets

The `planets` object MUST include the following keys:
- sun
- moon
- mars
- mercury
- jupiter
- venus
- saturn
- rahu
- ketu

Each planet entry MUST include:
- longitude
- nakshatra
- rashi

---

### 1.4 Western astrology section requirements
The `western` object MUST contain:
- ascendant
- planets

The `planets` object MUST include at least:
- sun
- moon
- mars
- mercury
- jupiter
- venus
- saturn

Outer planets (uranus, neptune, pluto) SHOULD be included if supported.

---

### 1.5 Chinese astrology section requirements
The `chinese` object MUST contain:
- animal
- element
- yin_yang
- year

---

### 1.6 Vimshottari dasha section requirements
The `vimshottari_dasha` object MUST contain:
- starting_dasha
- current_dasha
- periods

Each item in `periods` MUST contain:
- planet
- start
- end

---

### 1.7 Transits section requirements
The `transits_2026` object MUST include:
- mercury_retrogrades
- major_transits
- eclipses
- chinese_year 






## 2. Astrology Report (Markdown) Acceptance Criteria

The generated astrology report is considered VALID only if all the following conditions are met.

### 2.1 Report generation
- The report MUST be generated without runtime errors.
- The output MUST be a valid Markdown (.md) file.
- The report MUST be readable in a Markdown viewer or editor.

---

### 2.2 Required content sections
The report SHOULD contain clear, human-readable sections covering:
- Personality and nature
- Career and professional life
- Relationships and emotional patterns
- Vimshottari dasha and life phases
- Yearly outlook (e.g., 2026)

No major section SHOULD be empty or placeholder-only.

---

### 2.3 Content accuracy rules
- The report MUST be based only on the chart JSON data.
- The report MUST NOT invent planetary positions, signs, nakshatras, dashas, or dates.
- All astrological facts MUST match the underlying chart JSON.

---

### 2.4 Tone and style guidelines
- The tone SHOULD be informative, clear, and respectful.
- Language SHOULD be understandable to non-experts.
- The report MUST avoid extreme predictions or absolute claims.

---

### 2.5 Determinism requirement
- Given the same chart JSON input, the report generation MUST be reproducible.
- Formatting may vary slightly, but the meaning MUST remain consistent.


## 3. Deterministic vs AI-Generated Responsibilities

To ensure correctness and prevent hallucinations, the following separation of responsibilities MUST be maintained.

### 3.1 Deterministic (Non-AI) Components
The following data MUST always be produced by deterministic calculation logic and MUST NOT be generated or altered by AI models:

- Birth latitude, longitude, and timezone offset
- Planetary longitudes and positions
- Ascendant calculations
- Signs (rashi), nakshatras, and houses
- Vimshottari dasha periods and dates
- Transit dates and events
- Any numerical or date-based astrology data

These values represent the source of truth for the system.

---

### 3.2 AI-Generated Components
AI models (Amazon Bedrock) MAY be used only for:

- Interpreting planetary placements
- Explaining dashas and transits in natural language
- Summarizing chart insights
- Providing advice or guidance based on existing chart data
- Improving tone, clarity, and structure of the reading

AI-generated output MUST reference the deterministic chart data and MUST NOT introduce new astrological facts.

---

### 3.3 Validation rule
If AI-generated text contradicts deterministic chart data, the deterministic data MUST be treated as correct and authoritative.

