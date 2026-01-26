import requests


class LocationResolveError(Exception):
    pass


def resolve_place_india(place: str) -> dict:
    """
    Free geocoding using OpenStreetMap Nominatim.
    India MVP:
      - returns lat/lon via OSM
      - timezone fixed to Asia/Kolkata (+5.5)

    If place is ambiguous or not found, raise LocationResolveError.
    """

    if not place or not place.strip():
        raise LocationResolveError("Place is empty.")

    # Strongly bias results to India to reduce wrong matches
    query = place.strip()
    if "india" not in query.lower():
        query = f"{query}, India"

    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": query,
        "format": "json",
        "limit": 1,
        "addressdetails": 1,
    }

    # Nominatim requires a valid User-Agent
    headers = {
        "User-Agent": "AstroAI/1.0 (learning-project; contact: local-dev)"
    }

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=15)
        resp.raise_for_status()
        results = resp.json()
    except Exception as e:
        raise LocationResolveError(f"Failed to call OpenStreetMap resolver: {e}")

    if not results:
        raise LocationResolveError("Place not found. Please provide City, State, India.")

    r = results[0]
    lat = float(r["lat"])
    lon = float(r["lon"])

    return {
        "place": place,
        "latitude": lat,
        "longitude": lon,
        "timezone_name": "Asia/Kolkata",
        "timezone_offset": 5.5,
    }
