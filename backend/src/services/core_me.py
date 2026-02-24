from pathlib import Path
import json

def build_core_me_paragraph(chart_json_path: Path) -> str:
    """
    chart_json_path is the saved chart json produced by run_calculator.
    This function reads it and builds a short 'core characteristics' paragraph.
    """
    chart = json.loads(chart_json_path.read_text(encoding="utf-8"))

    # Defensive reads (depends on your JSON structure)
    western = chart.get("western", {}) if isinstance(chart.get("western"), dict) else {}
    vedic = chart.get("vedic", {}) if isinstance(chart.get("vedic"), dict) else {}
    chinese = chart.get("chinese", {}) if isinstance(chart.get("chinese"), dict) else {}

    w_sun = western.get("sun_sign", "Unknown")
    w_rising = western.get("ascendant_sign", "Unknown")
    w_moon = western.get("moon_sign", "Unknown")

    v_lagna = vedic.get("lagna_sign", "Unknown")
    v_moon = vedic.get("moon_sign", "Unknown")
    v_nakshatra = vedic.get("nakshatra", "Unknown")

    c_year = chinese.get("zodiac", "Unknown")

    paragraph = (
        f"*At your core, you blend **Western {w_sun} Sun* intensity with the social style of *{w_rising} Rising*, "
        f"and the emotional patterning of a *{w_moon} Moon. In Vedic terms, your **Lagna (Ascendant) is {v_lagna}*, "
        f"your *Moon is {v_moon}, and your nakshatra influence is *{v_nakshatra}**—giving you a mix of ambition, "
        f"drive, and a strong inner compass. In Chinese astrology, your birth year aligns with *{c_year}*, adding an "
        f"additional layer to your instincts and growth style."
    )
    return paragraph