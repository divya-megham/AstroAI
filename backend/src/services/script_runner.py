import subprocess
import sys
from pathlib import Path


class ScriptRunError(Exception):
    pass


def run_python_script(args: list[str]) -> None:
    """
    Runs a python script using the CURRENT venv interpreter (sys.executable).
    Raises ScriptRunError if it fails.
    """
    try:
        completed = subprocess.run(
            [sys.executable, *args],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        raise ScriptRunError(
            f"Script failed.\nCOMMAND: {e.cmd}\nSTDOUT:\n{e.stdout}\nSTDERR:\n{e.stderr}"
        )


def project_root_from_backend() -> Path:
    """
    backend/ is inside AstroAI/.
    project root = one folder up from backend/
    """
    return Path(__file__).resolve().parents[3]  # .../AstroAI/backend/src/services -> .../AstroAI


def get_scripts_dir() -> Path:
    """
    Scripts live at: AstroAI/docs/multi-system-astrology/scripts
    """
    root = project_root_from_backend()
    return root / "docs" / "multi-system-astrology" / "scripts"


def ensure_data_dirs(backend_root: Path) -> tuple[Path, Path]:
    charts_dir = backend_root / "data" / "charts"
    reports_dir = backend_root / "data" / "reports"
    charts_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    return charts_dir, reports_dir


def run_calculator(
    name: str,
    date: str,
    time: str,
    lat: float,
    lon: float,
    tz: float,
    place: str,
    ayanamsa: str,
    output_json_path: Path,
) -> None:
    scripts_dir = get_scripts_dir()
    script = scripts_dir / "multi_system_calculator.py"

    args = [
        str(script),
        "--name", name,
        "--date", date,
        "--time", time,
        "--lat", str(lat),
        "--lon", str(lon),
        "--tz", str(tz),
        "--place", place,
        "--ayanamsa", ayanamsa,
        "--output", str(output_json_path),
    ]
    run_python_script(args)


def run_report_generator(
    input_json_path: Path,
    output_md_path: Path,
) -> None:
    scripts_dir = get_scripts_dir()
    script = scripts_dir / "generate_combined_report.py"

    # IMPORTANT: this script expects input as a positional argument.
    args = [
        str(script),
        str(input_json_path),
        "--output", str(output_md_path),
    ]
    run_python_script(args)
