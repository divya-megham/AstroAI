#!/usr/bin/env python3
"""
Vedic Astrology Calculator using Swiss Ephemeris
Calculates planetary positions, Nakshatras, Rashis, and more.
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from typing import Dict, Any, Tuple

try:
    import swisseph as swe
except ImportError:
    print("Error: pyswisseph not installed. Run: pip install pyswisseph --break-system-packages")
    sys.exit(1)

# Nakshatra data: name, deity, ruling planet, symbol, nature
NAKSHATRAS = [
    ("Ashwini", "Ashwini Kumaras", "Ketu", "Horse's head", "Light/Swift"),
    ("Bharani", "Yama", "Venus", "Yoni", "Fierce"),
    ("Krittika", "Agni", "Sun", "Razor/Flame", "Mixed"),
    ("Rohini", "Brahma", "Moon", "Ox cart", "Fixed"),
    ("Mrigashira", "Soma", "Mars", "Deer's head", "Soft"),
    ("Ardra", "Rudra", "Rahu", "Teardrop", "Sharp"),
    ("Punarvasu", "Aditi", "Jupiter", "Bow", "Movable"),
    ("Pushya", "Brihaspati", "Saturn", "Lotus/Arrow", "Light"),
    ("Ashlesha", "Nagas", "Mercury", "Serpent", "Sharp"),
    ("Magha", "Pitris", "Ketu", "Throne", "Fierce"),
    ("Purva Phalguni", "Bhaga", "Venus", "Hammock", "Fierce"),
    ("Uttara Phalguni", "Aryaman", "Sun", "Bed", "Fixed"),
    ("Hasta", "Savitar", "Moon", "Hand", "Light"),
    ("Chitra", "Vishwakarma", "Mars", "Pearl", "Soft"),
    ("Swati", "Vayu", "Rahu", "Coral/Sword", "Movable"),
    ("Vishakha", "Indra-Agni", "Jupiter", "Arch", "Mixed"),
    ("Anuradha", "Mitra", "Saturn", "Lotus", "Soft"),
    ("Jyeshtha", "Indra", "Mercury", "Earring", "Sharp"),
    ("Mula", "Nirriti", "Ketu", "Roots", "Sharp"),
    ("Purva Ashadha", "Apas", "Venus", "Fan", "Fierce"),
    ("Uttara Ashadha", "Vishvadevas", "Sun", "Tusk", "Fixed"),
    ("Shravana", "Vishnu", "Moon", "Ear/Trident", "Movable"),
    ("Dhanishtha", "Vasus", "Mars", "Drum", "Movable"),
    ("Shatabhisha", "Varuna", "Rahu", "Circle", "Movable"),
    ("Purva Bhadrapada", "Aja Ekapada", "Jupiter", "Sword", "Fierce"),
    ("Uttara Bhadrapada", "Ahir Budhnya", "Saturn", "Twins", "Fixed"),
    ("Revati", "Pushan", "Mercury", "Fish/Drum", "Soft"),
]

# Rashi (Moon Sign) data: name, element, quality, ruling planet
RASHIS = [
    ("Mesha (Aries)", "Fire", "Movable", "Mars"),
    ("Vrishabha (Taurus)", "Earth", "Fixed", "Venus"),
    ("Mithuna (Gemini)", "Air", "Dual", "Mercury"),
    ("Karka (Cancer)", "Water", "Movable", "Moon"),
    ("Simha (Leo)", "Fire", "Fixed", "Sun"),
    ("Kanya (Virgo)", "Earth", "Dual", "Mercury"),
    ("Tula (Libra)", "Air", "Movable", "Venus"),
    ("Vrishchika (Scorpio)", "Water", "Fixed", "Mars"),
    ("Dhanu (Sagittarius)", "Fire", "Dual", "Jupiter"),
    ("Makara (Capricorn)", "Earth", "Movable", "Saturn"),
    ("Kumbha (Aquarius)", "Air", "Fixed", "Saturn"),
    ("Meena (Pisces)", "Water", "Dual", "Jupiter"),
]

# Planet mapping for Swiss Ephemeris
PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS,
    "Saturn": swe.SATURN,
    "Rahu": swe.MEAN_NODE,  # North Node
}

# Vimshottari Dasha years for each planet
DASHA_YEARS = {
    "Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7,
    "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17
}

# Dasha sequence starting from each Nakshatra's ruler
DASHA_SEQUENCE = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]


def degrees_to_dms(degrees: float) -> str:
    """Convert decimal degrees to degrees, minutes, seconds string."""
    d = int(degrees)
    m = int((degrees - d) * 60)
    s = ((degrees - d) * 60 - m) * 60
    return f"{d}°{m}'{s:.1f}\""


def get_nakshatra(longitude: float) -> Tuple[int, int, Dict[str, Any]]:
    """Calculate Nakshatra and Pada from sidereal longitude."""
    nakshatra_span = 360.0 / 27  # 13°20'
    pada_span = nakshatra_span / 4  # 3°20'
    
    nakshatra_idx = int(longitude / nakshatra_span)
    position_in_nakshatra = longitude % nakshatra_span
    pada = int(position_in_nakshatra / pada_span) + 1
    
    nak = NAKSHATRAS[nakshatra_idx]
    return nakshatra_idx, pada, {
        "index": nakshatra_idx + 1,
        "name": nak[0],
        "deity": nak[1],
        "ruler": nak[2],
        "symbol": nak[3],
        "nature": nak[4],
        "pada": pada,
        "longitude": longitude,
        "longitude_dms": degrees_to_dms(longitude),
    }


def get_rashi(longitude: float) -> Dict[str, Any]:
    """Calculate Rashi (zodiac sign) from sidereal longitude."""
    rashi_idx = int(longitude / 30) % 12
    position_in_rashi = longitude % 30
    
    rashi = RASHIS[rashi_idx]
    return {
        "index": rashi_idx + 1,
        "name": rashi[0],
        "element": rashi[1],
        "quality": rashi[2],
        "ruler": rashi[3],
        "degree_in_sign": position_in_rashi,
        "degree_in_sign_dms": degrees_to_dms(position_in_rashi),
    }


def calculate_julian_day(year: int, month: int, day: int, hour: float, tz_offset: float) -> float:
    """Calculate Julian Day from date/time, adjusting for timezone."""
    # Convert local time to UTC
    utc_hour = hour - tz_offset
    
    # Handle day rollover
    if utc_hour < 0:
        utc_hour += 24
        day -= 1
    elif utc_hour >= 24:
        utc_hour -= 24
        day += 1
    
    return swe.julday(year, month, day, utc_hour)


def calculate_planetary_positions(jd: float, lat: float, lon: float) -> Dict[str, Any]:
    """Calculate positions of all planets using sidereal zodiac."""
    # Set Lahiri ayanamsa (most common in Indian astrology)
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    
    positions = {}
    
    for planet_name, planet_id in PLANETS.items():
        try:
            # Calculate with sidereal flag
            pos, ret = swe.calc_ut(jd, planet_id, swe.FLG_SIDEREAL)
            longitude = pos[0]
            
            # Normalize to 0-360
            if longitude < 0:
                longitude += 360
            
            nakshatra_idx, pada, nakshatra_data = get_nakshatra(longitude)
            rashi_data = get_rashi(longitude)
            
            positions[planet_name.lower()] = {
                "name": planet_name,
                "longitude": longitude,
                "longitude_dms": degrees_to_dms(longitude),
                "latitude": pos[1],
                "speed": pos[3],
                "retrograde": pos[3] < 0,
                "nakshatra": nakshatra_data,
                "rashi": rashi_data,
            }
        except Exception as e:
            positions[planet_name.lower()] = {"error": str(e)}
    
    # Calculate Ketu (South Node) - opposite to Rahu
    if "rahu" in positions and "error" not in positions["rahu"]:
        ketu_lon = (positions["rahu"]["longitude"] + 180) % 360
        nakshatra_idx, pada, nakshatra_data = get_nakshatra(ketu_lon)
        rashi_data = get_rashi(ketu_lon)
        positions["ketu"] = {
            "name": "Ketu",
            "longitude": ketu_lon,
            "longitude_dms": degrees_to_dms(ketu_lon),
            "nakshatra": nakshatra_data,
            "rashi": rashi_data,
        }
    
    return positions


def calculate_ascendant(jd: float, lat: float, lon: float) -> Dict[str, Any]:
    """Calculate the Ascendant (Lagna) using sidereal zodiac."""
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    
    # Calculate houses - returns (cusps, ascmc) where ascmc[0] is ascendant
    cusps, ascmc = swe.houses(jd, lat, lon, b'P')  # Placidus
    
    asc_lon = ascmc[0]
    
    # Get sidereal ascendant
    ayanamsa = swe.get_ayanamsa(jd)
    asc_sidereal = (asc_lon - ayanamsa) % 360
    
    nakshatra_idx, pada, nakshatra_data = get_nakshatra(asc_sidereal)
    rashi_data = get_rashi(asc_sidereal)
    
    return {
        "longitude": asc_sidereal,
        "longitude_dms": degrees_to_dms(asc_sidereal),
        "nakshatra": nakshatra_data,
        "rashi": rashi_data,
        "ayanamsa": ayanamsa,
    }


def calculate_vimshottari_dasha(moon_longitude: float, birth_date: datetime) -> Dict[str, Any]:
    """Calculate Vimshottari Dasha periods based on Moon's Nakshatra."""
    # Get Moon's Nakshatra
    nakshatra_idx, pada, nakshatra_data = get_nakshatra(moon_longitude)
    
    # Nakshatra ruler determines starting Dasha
    nakshatra_rulers = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
    starting_ruler = nakshatra_rulers[nakshatra_idx % 9]
    
    # Calculate elapsed portion of current Nakshatra
    nakshatra_span = 360.0 / 27
    position_in_nakshatra = moon_longitude % nakshatra_span
    elapsed_fraction = position_in_nakshatra / nakshatra_span
    
    # Get starting Dasha index
    start_idx = DASHA_SEQUENCE.index(starting_ruler)
    
    # Calculate remaining years in first Dasha
    first_dasha_total = DASHA_YEARS[starting_ruler]
    first_dasha_remaining = first_dasha_total * (1 - elapsed_fraction)
    
    # Build Dasha timeline
    dashas = []
    current_date = birth_date
    
    for i in range(9):
        dasha_idx = (start_idx + i) % 9
        dasha_planet = DASHA_SEQUENCE[dasha_idx]
        
        if i == 0:
            years = first_dasha_remaining
        else:
            years = DASHA_YEARS[dasha_planet]
        
        end_date = current_date + timedelta(days=years * 365.25)
        
        dashas.append({
            "planet": dasha_planet,
            "years": round(years, 2),
            "start": current_date.strftime("%Y-%m-%d"),
            "end": end_date.strftime("%Y-%m-%d"),
        })
        
        current_date = end_date
    
    return {
        "starting_dasha": starting_ruler,
        "moon_nakshatra": nakshatra_data["name"],
        "periods": dashas,
    }


def generate_report(
    name: str,
    date_str: str,
    time_str: str,
    latitude: float,
    longitude: float,
    tz_offset: float,
) -> Dict[str, Any]:
    """Generate complete Vedic astrology report."""
    
    # Parse date and time
    date_parts = [int(x) for x in date_str.split("-")]
    time_parts = [int(x) for x in time_str.split(":")]
    
    year, month, day = date_parts
    hour = time_parts[0] + time_parts[1]/60 + (time_parts[2]/3600 if len(time_parts) > 2 else 0)
    
    birth_datetime = datetime(year, month, day, time_parts[0], time_parts[1])
    
    # Calculate Julian Day
    jd = calculate_julian_day(year, month, day, hour, tz_offset)
    
    # Get ayanamsa value
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    ayanamsa = swe.get_ayanamsa(jd)
    
    # Calculate all positions
    planets = calculate_planetary_positions(jd, latitude, longitude)
    ascendant = calculate_ascendant(jd, latitude, longitude)
    
    # Calculate Vimshottari Dasha
    moon_lon = planets["moon"]["longitude"]
    dasha = calculate_vimshottari_dasha(moon_lon, birth_datetime)
    
    return {
        "meta": {
            "name": name,
            "birth_date": date_str,
            "birth_time": time_str,
            "latitude": latitude,
            "longitude": longitude,
            "timezone_offset": tz_offset,
            "julian_day": jd,
            "ayanamsa": ayanamsa,
            "ayanamsa_type": "Lahiri",
            "generated_at": datetime.now().isoformat(),
        },
        "ascendant": ascendant,
        **planets,
        "vimshottari_dasha": dasha,
    }


def main():
    parser = argparse.ArgumentParser(description="Vedic Astrology Calculator")
    parser.add_argument("--name", required=True, help="Person's name")
    parser.add_argument("--date", required=True, help="Birth date (YYYY-MM-DD)")
    parser.add_argument("--time", required=True, help="Birth time (HH:MM:SS, 24h)")
    parser.add_argument("--lat", type=float, required=True, help="Latitude (decimal)")
    parser.add_argument("--lon", type=float, required=True, help="Longitude (decimal)")
    parser.add_argument("--tz", type=float, required=True, help="Timezone offset from UTC (e.g., +5.5)")
    parser.add_argument("--output", default="-", help="Output file (default: stdout)")
    
    args = parser.parse_args()
    
    report = generate_report(
        name=args.name,
        date_str=args.date,
        time_str=args.time,
        latitude=args.lat,
        longitude=args.lon,
        tz_offset=args.tz,
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
