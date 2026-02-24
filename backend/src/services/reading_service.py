from pathlib import Path
import re
from src.services.core_me import build_core_me_paragraph

from src.location.osm_resolver import resolve_place_india, LocationResolveError
from src.services.script_runner import (
    run_calculator,
    run_report_generator,
    ensure_data_dirs,
    ScriptRunError,
)

def _slug(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_") or "place"

def generate_reading(name: str, date: str, time: str, place: str, ayanamsa: str) -> dict:
    # 1) resolve place
    try:
        loc = resolve_place_india(place)
    except LocationResolveError as e:
        raise ValueError(str(e))

    lat = loc["latitude"]
    lon = loc["longitude"]
    tz = loc["timezone_offset"]

    # 2) build chart_id + file paths
    name_slug = _slug(name)
    date_part = date.replace("-", "")
    time_part = time.replace(":", "")
    place_slug = _slug(place.split(",")[0])
    chart_id = f"{name_slug}{date_part}{time_part}_{place_slug}"

    backend_root = Path(_file_).resolve().parents[2]
    charts_dir, reports_dir = ensure_data_dirs(backend_root)

    chart_path = charts_dir / f"{chart_id}_chart.json"
    report_path = reports_dir / f"{chart_id}_report.md"

    # 3) run scripts
    try:
        run_calculator(
            name=name,
            date=date,
            time=time,
            lat=lat,
            lon=lon,
            tz=tz,
            place=place,
            ayanamsa=ayanamsa or "raman",
            output_json_path=chart_path,
        )
        run_report_generator(
            input_json_path=chart_path,
            output_md_path=report_path,
        )
    except ScriptRunError as e:
        raise ValueError(f"Astrology script failed: {e}")

    # 4) read report
    report_markdown = report_path.read_text(encoding="utf-8")

    # 5) inject "Core Characteristics" paragraph right after Core Signature
    core_me_paragraph = build_core_me_paragraph(chart_path)

    # Add a new section under Core Signature
    injection = (
        "## Core Signature\n\n"
        f"{core_me_paragraph}\n\n"
        "## 2026 Headline\n"
    )

    # Replace the existing heading sequence safely
    report_markdown = report_markdown.replace("## Core Signature\n", injection)

    return {
        "chart_id": chart_id,
        "report_markdown": report_markdown,
    }
