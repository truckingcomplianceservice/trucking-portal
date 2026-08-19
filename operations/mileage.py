"""
Free, offline mileage estimation — no API key required.
Estimates driving miles between US locations using a built-in coordinate
table + haversine (great-circle) distance x a road-winding factor.
This is an ESTIMATE (typically within ~10-15% of actual road miles). Users can
always override the numbers by hand. For exact miles, a Google Maps key can be
added later.
"""
import math
import re

# Road distance is longer than straight-line; ~1.2 is a common approximation.
ROAD_FACTOR = 1.2

# State centroid coordinates (lat, lon) — fallback when we only know the state.
STATE_COORDS = {
    "AL": (32.8, -86.8), "AK": (64.2, -149.5), "AZ": (34.2, -111.7), "AR": (34.8, -92.4),
    "CA": (37.2, -119.4), "CO": (39.0, -105.5), "CT": (41.6, -72.7), "DE": (39.0, -75.5),
    "FL": (28.6, -82.4), "GA": (32.6, -83.4), "HI": (20.3, -156.4), "ID": (44.4, -114.6),
    "IL": (40.0, -89.2), "IN": (39.9, -86.3), "IA": (42.0, -93.5), "KS": (38.5, -98.4),
    "KY": (37.5, -85.3), "LA": (31.0, -92.0), "ME": (45.4, -69.2), "MD": (39.0, -76.8),
    "MA": (42.3, -71.8), "MI": (44.3, -85.4), "MN": (46.3, -94.3), "MS": (32.7, -89.7),
    "MO": (38.4, -92.5), "MT": (46.9, -110.0), "NE": (41.5, -99.8), "NV": (39.3, -116.6),
    "NH": (43.7, -71.6), "NJ": (40.1, -74.7), "NM": (34.4, -106.1), "NY": (42.9, -75.5),
    "NC": (35.6, -79.4), "ND": (47.5, -100.5), "OH": (40.3, -82.8), "OK": (35.6, -97.5),
    "OR": (44.0, -120.5), "PA": (40.9, -77.8), "RI": (41.7, -71.5), "SC": (33.9, -80.9),
    "SD": (44.4, -100.2), "TN": (35.9, -86.4), "TX": (31.5, -99.3), "UT": (39.3, -111.7),
    "VT": (44.1, -72.7), "VA": (37.5, -78.9), "WA": (47.4, -120.5), "WV": (38.6, -80.6),
    "WI": (44.6, -89.9), "WY": (43.0, -107.6), "DC": (38.9, -77.0),
}

# Major freight cities (city, ST) -> (lat, lon). Extend as needed.
CITY_COORDS = {
    ("los angeles", "CA"): (34.05, -118.24), ("san francisco", "CA"): (37.77, -122.42),
    ("sacramento", "CA"): (38.58, -121.49), ("san diego", "CA"): (32.72, -117.16),
    ("fresno", "CA"): (36.75, -119.77), ("oakland", "CA"): (37.80, -122.27),
    ("stockton", "CA"): (37.96, -121.29), ("bakersfield", "CA"): (35.37, -119.02),
    ("ontario", "CA"): (34.06, -117.65), ("las vegas", "NV"): (36.17, -115.14),
    ("reno", "NV"): (39.53, -119.81), ("phoenix", "AZ"): (33.45, -112.07),
    ("tucson", "AZ"): (32.22, -110.97), ("denver", "CO"): (39.74, -104.99),
    ("salt lake city", "UT"): (40.76, -111.89), ("portland", "OR"): (45.52, -122.68),
    ("seattle", "WA"): (47.61, -122.33), ("spokane", "WA"): (47.66, -117.43),
    ("boise", "ID"): (43.62, -116.20), ("dallas", "TX"): (32.78, -96.80),
    ("fort worth", "TX"): (32.76, -97.33), ("houston", "TX"): (29.76, -95.37),
    ("san antonio", "TX"): (29.42, -98.49), ("austin", "TX"): (30.27, -97.74),
    ("el paso", "TX"): (31.76, -106.49), ("laredo", "TX"): (27.53, -99.49),
    ("oklahoma city", "OK"): (35.47, -97.52), ("tulsa", "OK"): (36.15, -95.99),
    ("kansas city", "MO"): (39.10, -94.58), ("st louis", "MO"): (38.63, -90.20),
    ("chicago", "IL"): (41.88, -87.63), ("indianapolis", "IN"): (39.77, -86.16),
    ("columbus", "OH"): (39.96, -83.00), ("cleveland", "OH"): (41.50, -81.69),
    ("cincinnati", "OH"): (39.10, -84.51), ("detroit", "MI"): (42.33, -83.05),
    ("minneapolis", "MN"): (44.98, -93.27), ("milwaukee", "WI"): (43.04, -87.91),
    ("memphis", "TN"): (35.15, -90.05), ("nashville", "TN"): (36.16, -86.78),
    ("atlanta", "GA"): (33.75, -84.39), ("savannah", "GA"): (32.08, -81.09),
    ("jacksonville", "FL"): (30.33, -81.66), ("orlando", "FL"): (28.54, -81.38),
    ("tampa", "FL"): (27.95, -82.46), ("miami", "FL"): (25.76, -80.19),
    ("charlotte", "NC"): (35.23, -80.84), ("raleigh", "NC"): (35.78, -78.64),
    ("nashville", "TN"): (36.16, -86.78), ("louisville", "KY"): (38.25, -85.76),
    ("richmond", "VA"): (37.54, -77.44), ("washington", "DC"): (38.90, -77.04),
    ("baltimore", "MD"): (39.29, -76.61), ("philadelphia", "PA"): (39.95, -75.17),
    ("pittsburgh", "PA"): (40.44, -79.996), ("new york", "NY"): (40.71, -74.01),
    ("newark", "NJ"): (40.74, -74.17), ("boston", "MA"): (42.36, -71.06),
    ("buffalo", "NY"): (42.89, -78.88), ("albany", "NY"): (42.65, -73.75),
    ("harrisburg", "PA"): (40.27, -76.88), ("allentown", "PA"): (40.60, -75.47),
    ("new orleans", "LA"): (29.95, -90.07), ("birmingham", "AL"): (33.52, -86.80),
    ("little rock", "AR"): (34.75, -92.29), ("omaha", "NE"): (41.26, -95.93),
    ("des moines", "IA"): (41.59, -93.62), ("wichita", "KS"): (37.69, -97.34),
    ("albuquerque", "NM"): (35.08, -106.65), ("amarillo", "TX"): (35.22, -101.83),
}

_STATE_RE = re.compile(r",?\s*([A-Za-z]{2})\b\.?\s*(?:\d{5})?\s*$")


def _parse(location):
    """Return (city_lower, state_upper) from a free-text location string."""
    if not location:
        return None, None
    loc = location.strip()
    state = None
    m = _STATE_RE.search(loc)
    if m:
        state = m.group(1).upper()
        loc = loc[:m.start()].strip().rstrip(",")
    city = loc.split(",")[0].strip().lower() if loc else ""
    return city, state


def coords_for(location):
    """Best-effort (lat, lon) for a location string, or None."""
    city, state = _parse(location)
    if city and state and (city, state) in CITY_COORDS:
        return CITY_COORDS[(city, state)]
    if state and state in STATE_COORDS:
        return STATE_COORDS[state]
    # try city match against any state
    if city:
        for (c, st), xy in CITY_COORDS.items():
            if c == city:
                return xy
    return None


def haversine_miles(a, b):
    lat1, lon1 = a
    lat2, lon2 = b
    r = 3958.8  # earth radius in miles
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    x = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(x))


def estimate_miles(stops):
    """Estimate total road miles across an ordered list of stop strings.
    Returns (miles, unknown_stops)."""
    pts = []
    unknown = []
    for s in stops:
        xy = coords_for(s)
        if xy:
            pts.append(xy)
        elif s and s.strip():
            unknown.append(s)
    total = 0.0
    for i in range(len(pts) - 1):
        total += haversine_miles(pts[i], pts[i + 1])
    return int(round(total * ROAD_FACTOR)), unknown


def estimate_leg(a, b):
    """Estimate miles between two location strings (for deadhead)."""
    ca, cb = coords_for(a), coords_for(b)
    if not ca or not cb:
        return None
    return int(round(haversine_miles(ca, cb) * ROAD_FACTOR))


# ---- Google Maps (exact road miles) — used only when a key is configured ----
def _google_key():
    import os
    return os.environ.get("GOOGLE_MAPS_API_KEY", "").strip()


def google_miles(waypoints):
    """Exact road miles across an ordered list of location strings via Google
    Distance Matrix / Directions. Returns int miles or None on any problem."""
    key = _google_key()
    if not key or len([w for w in waypoints if w and w.strip()]) < 2:
        return None
    import json, urllib.parse, urllib.request
    pts = [w.strip() for w in waypoints if w and w.strip()]
    origin = urllib.parse.quote(pts[0])
    destination = urllib.parse.quote(pts[-1])
    params = f"origin={origin}&destination={destination}&units=imperial&key={key}"
    if len(pts) > 2:
        mid = "|".join(urllib.parse.quote(p) for p in pts[1:-1])
        params += f"&waypoints={mid}"
    url = f"https://maps.googleapis.com/maps/api/directions/json?{params}"
    try:
        with urllib.request.urlopen(url, timeout=12) as r:
            data = json.loads(r.read().decode("utf-8"))
        if data.get("status") != "OK" or not data.get("routes"):
            return None
        meters = sum(leg["distance"]["value"] for leg in data["routes"][0]["legs"])
        return int(round(meters / 1609.34))
    except Exception:
        return None


def best_miles(waypoints):
    """Prefer exact Google road miles; fall back to the free estimate.
    Returns (miles, source, unknown_stops)."""
    g = google_miles(waypoints)
    if g:
        return g, "google", []
    miles, unknown = estimate_miles(waypoints)
    return miles, "estimate", unknown


def best_leg(a, b):
    """Miles between two points — Google if available, else free estimate."""
    g = google_miles([a, b])
    if g:
        return g, "google"
    est = estimate_leg(a, b)
    return est, "estimate"
