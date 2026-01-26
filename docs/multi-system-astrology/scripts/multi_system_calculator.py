#!/usr/bin/env python3
"""
Multi-System Astrology Calculator
Combines Vedic (Sidereal), Western (Tropical), and Chinese astrology.
Supports multiple ayanamsas: Lahiri, Raman, KP, etc.
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from typing import Dict, Any, Tuple, List

try:
    import swisseph as swe
except ImportError:
    print("Error: pyswisseph not installed. Run: pip install pyswisseph --break-system-packages")
    sys.exit(1)

# =============================================================================
# AYANAMSA CONFIGURATIONS
# =============================================================================
AYANAMSAS = {
    "lahiri": (swe.SIDM_LAHIRI, "Lahiri (Chitrapaksha)"),
    "raman": (swe.SIDM_RAMAN, "B.V. Raman"),
    "kp": (swe.SIDM_KRISHNAMURTI, "Krishnamurti (KP)"),
    "yukteshwar": (swe.SIDM_YUKTESHWAR, "Sri Yukteshwar"),
    "true_chitra": (swe.SIDM_TRUE_CITRA, "True Chitrapaksha"),
}

# =============================================================================
# NAKSHATRA DATA
# =============================================================================
NAKSHATRAS = [
    {"name": "Ashwini", "deity": "Ashwini Kumaras", "ruler": "Ketu", "symbol": "Horse's head", "nature": "Light/Swift", "gana": "Deva", "animal": "Male Horse"},
    {"name": "Bharani", "deity": "Yama", "ruler": "Venus", "symbol": "Yoni", "nature": "Fierce", "gana": "Manushya", "animal": "Male Elephant"},
    {"name": "Krittika", "deity": "Agni", "ruler": "Sun", "symbol": "Razor/Flame", "nature": "Mixed", "gana": "Rakshasa", "animal": "Female Sheep"},
    {"name": "Rohini", "deity": "Brahma", "ruler": "Moon", "symbol": "Ox cart", "nature": "Fixed", "gana": "Manushya", "animal": "Male Serpent"},
    {"name": "Mrigashira", "deity": "Soma", "ruler": "Mars", "symbol": "Deer's head", "nature": "Soft", "gana": "Deva", "animal": "Female Serpent"},
    {"name": "Ardra", "deity": "Rudra", "ruler": "Rahu", "symbol": "Teardrop", "nature": "Sharp", "gana": "Manushya", "animal": "Female Dog"},
    {"name": "Punarvasu", "deity": "Aditi", "ruler": "Jupiter", "symbol": "Bow", "nature": "Movable", "gana": "Deva", "animal": "Female Cat"},
    {"name": "Pushya", "deity": "Brihaspati", "ruler": "Saturn", "symbol": "Lotus/Arrow", "nature": "Light", "gana": "Deva", "animal": "Male Sheep"},
    {"name": "Ashlesha", "deity": "Nagas", "ruler": "Mercury", "symbol": "Serpent", "nature": "Sharp", "gana": "Rakshasa", "animal": "Male Cat"},
    {"name": "Magha", "deity": "Pitris", "ruler": "Ketu", "symbol": "Throne", "nature": "Fierce", "gana": "Rakshasa", "animal": "Male Rat"},
    {"name": "Purva Phalguni", "deity": "Bhaga", "ruler": "Venus", "symbol": "Hammock", "nature": "Fierce", "gana": "Manushya", "animal": "Female Rat"},
    {"name": "Uttara Phalguni", "deity": "Aryaman", "ruler": "Sun", "symbol": "Bed", "nature": "Fixed", "gana": "Manushya", "animal": "Male Cow"},
    {"name": "Hasta", "deity": "Savitar", "ruler": "Moon", "symbol": "Hand", "nature": "Light", "gana": "Deva", "animal": "Female Buffalo"},
    {"name": "Chitra", "deity": "Vishwakarma", "ruler": "Mars", "symbol": "Pearl", "nature": "Soft", "gana": "Rakshasa", "animal": "Female Tiger"},
    {"name": "Swati", "deity": "Vayu", "ruler": "Rahu", "symbol": "Coral/Sword", "nature": "Movable", "gana": "Deva", "animal": "Male Buffalo"},
    {"name": "Vishakha", "deity": "Indra-Agni", "ruler": "Jupiter", "symbol": "Arch", "nature": "Mixed", "gana": "Rakshasa", "animal": "Male Tiger"},
    {"name": "Anuradha", "deity": "Mitra", "ruler": "Saturn", "symbol": "Lotus", "nature": "Soft", "gana": "Deva", "animal": "Female Deer"},
    {"name": "Jyeshtha", "deity": "Indra", "ruler": "Mercury", "symbol": "Earring", "nature": "Sharp", "gana": "Rakshasa", "animal": "Male Deer"},
    {"name": "Mula", "deity": "Nirriti", "ruler": "Ketu", "symbol": "Roots", "nature": "Sharp", "gana": "Rakshasa", "animal": "Male Dog"},
    {"name": "Purva Ashadha", "deity": "Apas", "ruler": "Venus", "symbol": "Fan", "nature": "Fierce", "gana": "Manushya", "animal": "Male Monkey"},
    {"name": "Uttara Ashadha", "deity": "Vishvadevas", "ruler": "Sun", "symbol": "Tusk", "nature": "Fixed", "gana": "Manushya", "animal": "Male Mongoose"},
    {"name": "Shravana", "deity": "Vishnu", "ruler": "Moon", "symbol": "Ear/Trident", "nature": "Movable", "gana": "Deva", "animal": "Female Monkey"},
    {"name": "Dhanishtha", "deity": "Vasus", "ruler": "Mars", "symbol": "Drum", "nature": "Movable", "gana": "Rakshasa", "animal": "Female Lion"},
    {"name": "Shatabhisha", "deity": "Varuna", "ruler": "Rahu", "symbol": "Circle", "nature": "Movable", "gana": "Rakshasa", "animal": "Female Horse"},
    {"name": "Purva Bhadrapada", "deity": "Aja Ekapada", "ruler": "Jupiter", "symbol": "Sword", "nature": "Fierce", "gana": "Manushya", "animal": "Male Lion"},
    {"name": "Uttara Bhadrapada", "deity": "Ahir Budhnya", "ruler": "Saturn", "symbol": "Twins", "nature": "Fixed", "gana": "Manushya", "animal": "Female Cow"},
    {"name": "Revati", "deity": "Pushan", "ruler": "Mercury", "symbol": "Fish/Drum", "nature": "Soft", "gana": "Deva", "animal": "Female Elephant"},
]

# Navamsa signs for each pada
PADA_NAVAMSA = [
    "Aries", "Taurus", "Gemini", "Cancer",  # Ashwini padas
    "Leo", "Virgo", "Libra", "Scorpio",  # Bharani padas
    # ... continues cyclically through 12 signs
]

# =============================================================================
# RASHI (ZODIAC SIGN) DATA
# =============================================================================
RASHIS_VEDIC = [
    {"name": "Mesha", "english": "Aries", "element": "Fire", "quality": "Movable", "ruler": "Mars"},
    {"name": "Vrishabha", "english": "Taurus", "element": "Earth", "quality": "Fixed", "ruler": "Venus"},
    {"name": "Mithuna", "english": "Gemini", "element": "Air", "quality": "Dual", "ruler": "Mercury"},
    {"name": "Karka", "english": "Cancer", "element": "Water", "quality": "Movable", "ruler": "Moon"},
    {"name": "Simha", "english": "Leo", "element": "Fire", "quality": "Fixed", "ruler": "Sun"},
    {"name": "Kanya", "english": "Virgo", "element": "Earth", "quality": "Dual", "ruler": "Mercury"},
    {"name": "Tula", "english": "Libra", "element": "Air", "quality": "Movable", "ruler": "Venus"},
    {"name": "Vrishchika", "english": "Scorpio", "element": "Water", "quality": "Fixed", "ruler": "Mars"},
    {"name": "Dhanu", "english": "Sagittarius", "element": "Fire", "quality": "Dual", "ruler": "Jupiter"},
    {"name": "Makara", "english": "Capricorn", "element": "Earth", "quality": "Movable", "ruler": "Saturn"},
    {"name": "Kumbha", "english": "Aquarius", "element": "Air", "quality": "Fixed", "ruler": "Saturn"},
    {"name": "Meena", "english": "Pisces", "element": "Water", "quality": "Dual", "ruler": "Jupiter"},
]

SIGNS_WESTERN = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

# =============================================================================
# CHINESE ZODIAC DATA
# =============================================================================
CHINESE_ANIMALS = [
    "Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake",
    "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"
]

CHINESE_ELEMENTS = ["Wood", "Fire", "Earth", "Metal", "Water"]

# =============================================================================
# DASHA DATA
# =============================================================================
DASHA_YEARS = {
    "Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7,
    "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17
}

DASHA_SEQUENCE = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]

# Planet mapping for Swiss Ephemeris
PLANETS = {
    "Sun": swe.SUN, "Moon": swe.MOON, "Mars": swe.MARS,
    "Mercury": swe.MERCURY, "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS, "Saturn": swe.SATURN,
    "Uranus": swe.URANUS, "Neptune": swe.NEPTUNE, "Pluto": swe.PLUTO,
    "Rahu": swe.MEAN_NODE,
}


def degrees_to_dms(degrees: float) -> str:
    """Convert decimal degrees to degrees, minutes, seconds string."""
    d = int(degrees)
    m = int((degrees - d) * 60)
    s = ((degrees - d) * 60 - m) * 60
    return f"{d}°{m}'{s:.0f}\""


def get_nakshatra(longitude: float) -> Dict[str, Any]:
    """Calculate Nakshatra and Pada from sidereal longitude."""
    nakshatra_span = 360.0 / 27  # 13°20'
    pada_span = nakshatra_span / 4  # 3°20'
    
    nakshatra_idx = int(longitude / nakshatra_span) % 27
    position_in_nakshatra = longitude % nakshatra_span
    pada = int(position_in_nakshatra / pada_span) + 1
    
    # Calculate navamsa for this pada
    total_pada = nakshatra_idx * 4 + (pada - 1)
    navamsa_sign = SIGNS_WESTERN[total_pada % 12]
    
    nak = NAKSHATRAS[nakshatra_idx]
    return {
        "index": nakshatra_idx + 1,
        "name": nak["name"],
        "deity": nak["deity"],
        "ruler": nak["ruler"],
        "symbol": nak["symbol"],
        "nature": nak["nature"],
        "gana": nak["gana"],
        "animal": nak["animal"],
        "pada": pada,
        "navamsa": navamsa_sign,
        "longitude": longitude,
        "longitude_dms": degrees_to_dms(longitude),
    }


def get_rashi(longitude: float) -> Dict[str, Any]:
    """Calculate Rashi (zodiac sign) from sidereal longitude."""
    rashi_idx = int(longitude / 30) % 12
    position_in_rashi = longitude % 30
    
    rashi = RASHIS_VEDIC[rashi_idx]
    return {
        "index": rashi_idx + 1,
        "name": rashi["name"],
        "english": rashi["english"],
        "full_name": f"{rashi['name']} ({rashi['english']})",
        "element": rashi["element"],
        "quality": rashi["quality"],
        "ruler": rashi["ruler"],
        "degree_in_sign": position_in_rashi,
        "degree_in_sign_dms": degrees_to_dms(position_in_rashi),
    }


def get_western_sign(longitude: float) -> Dict[str, Any]:
    """Get Western tropical zodiac sign."""
    sign_idx = int(longitude / 30) % 12
    position_in_sign = longitude % 30
    
    return {
        "sign": SIGNS_WESTERN[sign_idx],
        "degree": position_in_sign,
        "degree_dms": degrees_to_dms(position_in_sign),
    }


def get_chinese_zodiac(year: int, month: int, day: int) -> Dict[str, Any]:
    """Calculate Chinese zodiac animal and element."""
    # Chinese New Year typically falls between Jan 21 - Feb 20
    # For simplicity, using Feb 4 as cutoff (Lichun - start of spring)
    if month < 2 or (month == 2 and day < 4):
        year -= 1
    
    # Animal cycle (12 years, starting from Rat in year 4 of 60-year cycle)
    animal_idx = (year - 4) % 12
    animal = CHINESE_ANIMALS[animal_idx]
    
    # Element cycle (10 years = 5 elements × 2 years each)
    element_idx = ((year - 4) % 10) // 2
    element = CHINESE_ELEMENTS[element_idx]
    
    # Yin/Yang
    yin_yang = "Yang" if year % 2 == 0 else "Yin"
    
    return {
        "animal": animal,
        "element": element,
        "yin_yang": yin_yang,
        "full": f"{element} {animal}",
        "year": year,
    }


def get_current_chinese_year(year: int = 2026) -> Dict[str, Any]:
    """Get Chinese zodiac for a given year."""
    return get_chinese_zodiac(year, 6, 15)  # Mid-year to ensure correct year


def calculate_julian_day(year: int, month: int, day: int, hour: float, tz_offset: float) -> float:
    """Calculate Julian Day from date/time, adjusting for timezone."""
    utc_hour = hour - tz_offset
    
    if utc_hour < 0:
        utc_hour += 24
        # Adjust date backwards
        dt = datetime(year, month, day) - timedelta(days=1)
        year, month, day = dt.year, dt.month, dt.day
    elif utc_hour >= 24:
        utc_hour -= 24
        dt = datetime(year, month, day) + timedelta(days=1)
        year, month, day = dt.year, dt.month, dt.day
    
    return swe.julday(year, month, day, utc_hour)


def calculate_vedic_positions(jd: float, lat: float, lon: float, ayanamsa: str = "raman") -> Dict[str, Any]:
    """Calculate Vedic sidereal positions."""
    
    # Set ayanamsa
    if ayanamsa in AYANAMSAS:
        swe.set_sid_mode(AYANAMSAS[ayanamsa][0])
        ayanamsa_name = AYANAMSAS[ayanamsa][1]
    else:
        swe.set_sid_mode(swe.SIDM_RAMAN)
        ayanamsa_name = "B.V. Raman"
    
    ayanamsa_value = swe.get_ayanamsa(jd)
    
    positions = {}
    
    for planet_name, planet_id in PLANETS.items():
        if planet_name in ["Uranus", "Neptune", "Pluto"]:
            continue  # Skip outer planets for Vedic
        
        try:
            pos, _ = swe.calc_ut(jd, planet_id, swe.FLG_SIDEREAL)
            longitude = pos[0] if pos[0] >= 0 else pos[0] + 360
            
            positions[planet_name.lower()] = {
                "name": planet_name,
                "longitude": longitude,
                "longitude_dms": degrees_to_dms(longitude),
                "latitude": pos[1],
                "speed": pos[3],
                "retrograde": pos[3] < 0,
                "nakshatra": get_nakshatra(longitude),
                "rashi": get_rashi(longitude),
            }
        except Exception as e:
            positions[planet_name.lower()] = {"error": str(e)}
    
    # Calculate Ketu (opposite to Rahu)
    if "rahu" in positions and "error" not in positions["rahu"]:
        ketu_lon = (positions["rahu"]["longitude"] + 180) % 360
        positions["ketu"] = {
            "name": "Ketu",
            "longitude": ketu_lon,
            "longitude_dms": degrees_to_dms(ketu_lon),
            "retrograde": True,  # Nodes are always retrograde
            "nakshatra": get_nakshatra(ketu_lon),
            "rashi": get_rashi(ketu_lon),
        }
    
    # Calculate Ascendant
    cusps, ascmc = swe.houses(jd, lat, lon, b'P')
    asc_sidereal = (ascmc[0] - ayanamsa_value) % 360
    
    ascendant = {
        "longitude": asc_sidereal,
        "longitude_dms": degrees_to_dms(asc_sidereal),
        "nakshatra": get_nakshatra(asc_sidereal),
        "rashi": get_rashi(asc_sidereal),
    }
    
    return {
        "ayanamsa": ayanamsa_value,
        "ayanamsa_type": ayanamsa_name,
        "ascendant": ascendant,
        "planets": positions,
    }


def calculate_western_positions(jd: float, lat: float, lon: float) -> Dict[str, Any]:
    """Calculate Western tropical positions."""
    
    positions = {}
    
    for planet_name, planet_id in PLANETS.items():
        try:
            pos, _ = swe.calc_ut(jd, planet_id)
            longitude = pos[0] if pos[0] >= 0 else pos[0] + 360
            
            positions[planet_name.lower()] = {
                "name": planet_name,
                "longitude": longitude,
                "longitude_dms": degrees_to_dms(longitude),
                "sign": get_western_sign(longitude),
                "retrograde": pos[3] < 0,
            }
        except Exception as e:
            positions[planet_name.lower()] = {"error": str(e)}
    
    # Ascendant
    cusps, ascmc = swe.houses(jd, lat, lon, b'P')
    asc_lon = ascmc[0]
    
    ascendant = {
        "longitude": asc_lon,
        "longitude_dms": degrees_to_dms(asc_lon),
        "sign": get_western_sign(asc_lon),
    }
    
    return {
        "ascendant": ascendant,
        "planets": positions,
    }


def calculate_vimshottari_dasha(moon_longitude: float, birth_date: datetime) -> Dict[str, Any]:
    """Calculate Vimshottari Dasha periods."""
    nakshatra_data = get_nakshatra(moon_longitude)
    nakshatra_idx = nakshatra_data["index"] - 1
    
    # Nakshatra ruler determines starting Dasha
    nakshatra_rulers = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
    starting_ruler = nakshatra_rulers[nakshatra_idx % 9]
    
    # Calculate elapsed portion
    nakshatra_span = 360.0 / 27
    position_in_nakshatra = moon_longitude % nakshatra_span
    elapsed_fraction = position_in_nakshatra / nakshatra_span
    
    start_idx = DASHA_SEQUENCE.index(starting_ruler)
    first_dasha_remaining = DASHA_YEARS[starting_ruler] * (1 - elapsed_fraction)
    
    dashas = []
    current_date = birth_date
    
    for i in range(9):
        dasha_idx = (start_idx + i) % 9
        dasha_planet = DASHA_SEQUENCE[dasha_idx]
        years = first_dasha_remaining if i == 0 else DASHA_YEARS[dasha_planet]
        end_date = current_date + timedelta(days=years * 365.25)
        
        dashas.append({
            "planet": dasha_planet,
            "years": round(years, 2),
            "start": current_date.strftime("%Y-%m-%d"),
            "end": end_date.strftime("%Y-%m-%d"),
        })
        current_date = end_date
    
    # Find current dasha
    today = datetime.now()
    current_dasha = None
    for d in dashas:
        start = datetime.strptime(d["start"], "%Y-%m-%d")
        end = datetime.strptime(d["end"], "%Y-%m-%d")
        if start <= today <= end:
            current_dasha = d["planet"]
            break
    
    return {
        "starting_dasha": starting_ruler,
        "moon_nakshatra": nakshatra_data["name"],
        "current_dasha": current_dasha,
        "periods": dashas,
    }


def get_2026_transits() -> Dict[str, Any]:
    """Get major astrological transits for 2026."""
    return {
        "mercury_retrogrades": [
            {"start": "2026-02-26", "end": "2026-03-20", "sign": "Pisces"},
            {"start": "2026-06-29", "end": "2026-07-23", "sign": "Cancer"},
            {"start": "2026-10-24", "end": "2026-11-13", "sign": "Scorpio"},
        ],
        "major_transits": [
            {"date": "2026-01-26", "event": "Neptune enters Aries"},
            {"date": "2026-02-13", "event": "Saturn enters Aries"},
            {"date": "2026-04-25", "event": "Uranus enters Gemini"},
            {"date": "2026-06-30", "event": "Jupiter enters Leo (Tropical)"},
            {"date": "2026-06-01", "event": "Jupiter enters Cancer (Vedic/Sidereal)"},
            {"date": "2026-10-31", "event": "Jupiter enters Leo (Vedic/Sidereal)"},
            {"date": "2026-12-05", "event": "Rahu-Ketu shift to Capricorn-Cancer"},
        ],
        "eclipses": [
            {"date": "2026-02-17", "type": "Annular Solar", "sign": "Aquarius"},
            {"date": "2026-03-03", "type": "Total Lunar", "sign": "Virgo"},
            {"date": "2026-08-12", "type": "Total Solar", "sign": "Leo"},
            {"date": "2026-08-28", "type": "Partial Lunar", "sign": "Pisces"},
        ],
        "chinese_year": {
            "starts": "2026-02-17",
            "animal": "Horse",
            "element": "Fire",
            "full": "Fire Horse",
        }
    }


def generate_full_report(
    name: str,
    date_str: str,
    time_str: str,
    latitude: float,
    longitude: float,
    tz_offset: float,
    place: str = "",
    ayanamsa: str = "raman",
) -> Dict[str, Any]:
    """Generate comprehensive multi-system astrology report."""
    
    # Parse date and time
    date_parts = [int(x) for x in date_str.split("-")]
    time_parts = [int(x) for x in time_str.split(":")]
    
    year, month, day = date_parts
    hour = time_parts[0] + time_parts[1]/60 + (time_parts[2]/3600 if len(time_parts) > 2 else 0)
    
    birth_datetime = datetime(year, month, day, time_parts[0], time_parts[1])
    
    # Calculate Julian Day
    jd = calculate_julian_day(year, month, day, hour, tz_offset)
    
    # Calculate all systems
    vedic = calculate_vedic_positions(jd, latitude, longitude, ayanamsa)
    western = calculate_western_positions(jd, latitude, longitude)
    chinese = get_chinese_zodiac(year, month, day)
    
    # Vimshottari Dasha
    moon_lon = vedic["planets"]["moon"]["longitude"]
    dasha = calculate_vimshottari_dasha(moon_lon, birth_datetime)
    
    # 2026 Transits
    transits_2026 = get_2026_transits()
    
    return {
        "meta": {
            "name": name,
            "birth_date": date_str,
            "birth_time": time_str,
            "birth_place": place,
            "latitude": latitude,
            "longitude": longitude,
            "timezone_offset": tz_offset,
            "julian_day": jd,
            "generated_at": datetime.now().isoformat(),
        },
        "vedic": vedic,
        "western": western,
        "chinese": chinese,
        "vimshottari_dasha": dasha,
        "transits_2026": transits_2026,
    }


def main():
    parser = argparse.ArgumentParser(description="Multi-System Astrology Calculator")
    parser.add_argument("--name", required=True, help="Person's name")
    parser.add_argument("--date", required=True, help="Birth date (YYYY-MM-DD)")
    parser.add_argument("--time", required=True, help="Birth time (HH:MM:SS, 24h)")
    parser.add_argument("--lat", type=float, required=True, help="Latitude (decimal)")
    parser.add_argument("--lon", type=float, required=True, help="Longitude (decimal)")
    parser.add_argument("--tz", type=float, required=True, help="Timezone offset from UTC")
    parser.add_argument("--place", default="", help="Birth place name")
    parser.add_argument("--ayanamsa", default="raman", choices=list(AYANAMSAS.keys()),
                       help="Ayanamsa system (default: raman)")
    parser.add_argument("--output", default="-", help="Output file (default: stdout)")
    
    args = parser.parse_args()
    
    report = generate_full_report(
        name=args.name,
        date_str=args.date,
        time_str=args.time,
        latitude=args.lat,
        longitude=args.lon,
        tz_offset=args.tz,
        place=args.place,
        ayanamsa=args.ayanamsa,
    )
    
    output_json = json.dumps(report, indent=2, ensure_ascii=False)
    
    if args.output == "-":
        print(output_json)
    else:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_json)
        print(f"Report saved to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
