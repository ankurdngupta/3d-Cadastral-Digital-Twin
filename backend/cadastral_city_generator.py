"""
Cadastral Map → Hypothetical 3D City Generator
================================================
Converts the uploaded village cadastral map (~200 plots numbered 1301-1915)
into a full hypothetical city with multi-floor 3D buildings, residential flats,
commercial shops, government offices, and unique ULPINs for every spatial unit.

Plot positions are approximated from the raster map image to create a
realistic city layout matching the actual cadastral boundaries.
"""

import math
import random
import numpy as np

random.seed(2026)
np.random.seed(2026)

FLOOR_HEIGHT = 3.0  # meters per floor

# ─── Administrative Identity ───────────────────────────────────────────
STATE = "RJ"
DISTRICT = "JPR"
TEHSIL = "AMER"
VILLAGE = "VLG001"
CITY_NAME = "Khatipura Nagar (Hypothetical)"
GOV_AUTHORITY = "Govt of Rajasthan · Revenue Dept / SIH 2026 Cadastral Platform"

# ─── Valuation Circle Rates (INR per sq.m) ─────────────────────────────
CIRCLE_RATES = {
    "RES": 65000,
    "COM": 110000,
    "GOV": 45000,
    "AGR": 15000,
    "PRK": 30000,
    "UTL": 40000,
}

# ─── Common Indian Names Pool for Owner Generation ─────────────────────
FIRST_NAMES = [
    "Rajesh", "Sunil", "Manoj", "Vikram", "Amit", "Priya", "Sunita",
    "Kavita", "Deepak", "Ramesh", "Sanjay", "Pooja", "Neha", "Ankit",
    "Arun", "Meena", "Geeta", "Ravi", "Mohan", "Lakshmi", "Pankaj",
    "Mahesh", "Nisha", "Seema", "Arjun", "Kiran", "Vikas", "Prem",
    "Suman", "Dinesh", "Renu", "Harsh", "Ajay", "Rekha", "Govind",
    "Bharat", "Chandra", "Divya", "Gaurav", "Hemant", "Jyoti", "Kamal",
    "Lata", "Mukesh", "Narendra", "Omprakash", "Pinky", "Rahul",
]
LAST_NAMES = [
    "Sharma", "Verma", "Gupta", "Singh", "Agarwal", "Joshi", "Meena",
    "Yadav", "Patel", "Chauhan", "Malhotra", "Saxena", "Mishra",
    "Tiwari", "Rajput", "Soni", "Khandelwal", "Mathur", "Shekhawat",
    "Rathore", "Choudhary", "Saini", "Kumawat", "Pareek", "Vyas",
    "Jain", "Goyal", "Bansal", "Mittal", "Tandon", "Kapoor",
]
COMMERCIAL_OWNERS = [
    "State Bank of India", "Punjab National Bank", "Apollo Pharmacy",
    "Reliance Fresh Mart", "More Supermarket", "Vodafone Idea Store",
    "Jio Digital Centre", "HDFC Bank Branch", "ICICI Bank ATM",
    "Big Bazaar", "DMart", "Bata Shoes", "Raymond Showroom",
    "Haldiram's Sweets", "Bikaner Namkeen", "LIC Office",
    "Post Office", "Tanishq Jewellers", "Titan Eye Plus",
    "Croma Electronics", "Airtel Experience Centre",
    "Maruti Suzuki Service", "Honda Showroom",
]
GOVT_OWNERS = [
    "Gram Panchayat Khatipura", "Rajasthan PWD Office",
    "Primary Health Centre (PHC)", "Government Primary School",
    "Government Senior Secondary School", "Anganwadi Centre",
    "Tehsil Revenue Office", "Police Chowki Khatipura",
    "Community Hall (Samudayik Bhawan)", "Jal Nigam Pump House",
    "Electricity Sub-Station (JVVNL)", "Veterinary Hospital",
    "Rajasthan Housing Board Office", "Postal Sub-Office",
]


# ═══════════════════════════════════════════════════════════════════════
# PLOT DATA — Extracted from Cadastral Map Image
# ═══════════════════════════════════════════════════════════════════════
# Format: (plot_number, norm_x%, norm_y%, size_category)
#   norm_x: 0=left edge, 100=right edge of map
#   norm_y: 0=top edge, 100=bottom edge of map
#   size:   S=small (<300 sqm)  → dense residential (3-6 floors)
#           M=medium (300-800)   → medium residential (2-4 floors)
#           L=large (800-2000)   → institutional / govt / low-rise
#           XL=very large (>2000) → open / agricultural / park
# ═══════════════════════════════════════════════════════════════════════

CADASTRAL_PLOTS = [
    # ── Row 1: Top edge (y: 0-12) ──────────────────────────────────
    # Top-left cluster
    ("5111", 5, 7, "L"),
    ("1324", 10, 7, "M"),
    ("1325", 3, 12, "L"),
    ("1326", 9, 14, "XL"),

    # Top-center-left
    ("1319", 17, 5, "S"),
    ("1320", 20, 6, "M"),
    ("1315", 30, 3, "S"),
    ("1301", 35, 4, "S"),
    ("1302", 37, 5, "S"),
    ("1313", 26, 7, "S"),
    ("1311", 28, 8, "S"),
    ("1308", 24, 10, "S"),
    ("1304", 30, 10, "S"),
    ("1307", 33, 12, "S"),
    ("1305", 36, 10, "S"),
    ("1306", 37, 13, "S"),

    # Top-center
    ("1454", 43, 3, "M"),
    ("1459", 49, 9, "M"),
    ("1445", 44, 12, "S"),
    ("1435", 51, 12, "S"),
    ("1436", 53, 11, "S"),

    # Top-center-right
    ("1464", 60, 3, "M"),
    ("1470", 64, 3, "M"),
    ("1471", 61, 7, "S"),
    ("1473", 64, 7, "S"),
    ("1477", 62, 11, "S"),
    ("1481", 64, 8, "S"),
    ("1485", 72, 5, "S"),
    ("1486", 74, 3, "M"),
    ("1489", 79, 2, "M"),
    ("1488", 79, 6, "M"),
    ("1487", 76, 8, "M"),
    ("1476", 58, 12, "S"),
    ("1480", 61, 12, "S"),
    ("1479", 65, 12, "S"),
    ("1483", 68, 9, "S"),

    # Far right top
    ("1509", 97, 2, "M"),
    ("1506", 93, 3, "S"),
    ("1510", 88, 5, "S"),
    ("1511", 91, 5, "S"),
    ("1512", 86, 8, "S"),
    ("1516", 84, 10, "S"),
    ("1513", 88, 10, "M"),
    ("1515", 86, 12, "S"),
    ("1518", 80, 16, "L"),
    ("1521", 89, 16, "M"),
    ("1524", 86, 15, "S"),
    ("1520", 91, 15, "S"),

    # ── Row 2: Upper-middle (y: 12-28) ─────────────────────────────
    # Upper-middle-left
    ("1322", 21, 13, "M"),
    ("1359", 21, 17, "M"),
    ("1362", 29, 18, "S"),
    ("1361", 31, 17, "S"),
    ("1360", 28, 20, "S"),
    ("1358", 23, 20, "M"),
    ("1365", 28, 23, "S"),
    ("1363", 34, 19, "S"),

    # Upper-middle-center
    ("1397", 43, 18, "S"),
    ("1398", 39, 19, "S"),
    ("1395", 39, 21, "S"),
    ("1376", 36, 22, "S"),
    ("1393", 38, 24, "S"),
    ("1399", 43, 20, "S"),
    ("1401", 45, 22, "S"),

    # Upper-middle-right (around 1475 area)
    ("1475", 56, 15, "M"),
    ("1427", 58, 16, "S"),
    ("1478", 70, 17, "L"),
    ("1420", 62, 20, "S"),
    ("1423", 60, 22, "S"),
    ("1422", 63, 22, "S"),
    ("1413", 58, 25, "S"),
    ("1418", 67, 23, "S"),
    ("1417", 65, 27, "M"),
    ("1414", 62, 28, "S"),
    ("1404", 53, 25, "S"),
    ("1405", 55, 27, "S"),
    ("1406", 52, 28, "S"),

    # Right column upper
    ("1673", 83, 21, "M"),
    ("1675", 86, 23, "M"),
    ("1685", 83, 25, "S"),
    ("1684", 84, 27, "M"),
    ("1683", 87, 28, "M"),
    ("1682", 90, 28, "M"),
    ("1681", 92, 32, "L"),
    ("1696", 80, 23, "L"),
    ("1676", 89, 24, "S"),
    ("1678", 92, 26, "S"),

    # ── Row 3: Center band (y: 28-48) ─────────────────────────────
    # Center-left
    ("1327", 13, 26, "M"),
    ("1328", 13, 28, "M"),
    ("1329", 11, 31, "M"),
    ("1334", 7, 35, "M"),
    ("1340", 13, 37, "M"),
    ("1344", 16, 37, "S"),
    ("1345", 18, 36, "S"),
    ("1346", 17, 34, "S"),
    ("1342", 15, 40, "M"),
    ("1343", 19, 43, "XL"),

    # Center
    ("1387", 29, 39, "XL"),
    ("1371", 29, 33, "S"),
    ("1369", 26, 31, "M"),
    ("1364", 31, 25, "S"),
    ("1388", 36, 36, "S"),
    ("1381", 33, 31, "S"),
    ("1392", 40, 28, "S"),
    ("1391", 41, 30, "S"),
    ("1408", 48, 31, "S"),
    ("1409", 46, 34, "S"),

    # Center-right
    ("1688", 67, 36, "L"),
    ("1707", 56, 36, "M"),
    ("1708", 51, 41, "M"),
    ("1706", 57, 39, "S"),
    ("1705", 62, 39, "S"),
    ("1709", 60, 43, "S"),
    ("1691", 70, 41, "S"),
    ("1692", 70, 46, "M"),

    # Far right center
    ("1886", 87, 47, "XL"),

    # ── Row 4: Lower-center (y: 45-60) ────────────────────────────
    # Lower-left column
    ("1764", 5, 46, "M"),
    ("1765", 4, 49, "S"),
    ("1762", 11, 48, "S"),
    ("1760", 13, 48, "S"),
    ("1753", 19, 50, "L"),
    ("1767", 8, 51, "S"),
    ("1756", 15, 51, "S"),
    ("1754", 17, 51, "S"),
    ("1755", 18, 53, "S"),
    ("1770", 11, 54, "S"),
    ("1772", 13, 56, "S"),
    ("1774", 9, 58, "S"),
    ("1777", 6, 61, "S"),
    ("1778", 6, 64, "S"),

    # Center-lower
    ("1749", 26, 53, "S"),
    ("1750", 23, 54, "S"),
    ("1728", 31, 48, "S"),
    ("1726", 41, 46, "M"),
    ("1723", 44, 49, "M"),
    ("1724", 43, 47, "S"),
    ("1735", 36, 53, "S"),
    ("1734", 38, 53, "S"),
    ("1733", 34, 51, "S"),
    ("1737", 34, 56, "S"),
    ("1742", 33, 59, "S"),
    ("1741", 35, 59, "S"),
    ("1740", 36, 61, "S"),
    ("1738", 39, 59, "M"),
    ("1739", 41, 61, "S"),
    ("1712", 52, 51, "S"),
    ("1704", 57, 49, "M"),
    ("1698", 49, 56, "S"),
    ("1699", 49, 59, "S"),
    ("1700", 53, 59, "S"),
    ("1701", 56, 57, "S"),
    ("1694", 56, 61, "S"),
    ("1695", 53, 63, "S"),
    ("1693", 59, 59, "S"),

    # ── Row 5: Bottom band (y: 60-85) ─────────────────────────────
    # Bottom-left
    ("1781", 15, 63, "M"),
    ("1784", 19, 58, "S"),
    ("1785", 23, 58, "M"),
    ("1787", 25, 61, "M"),
    ("1800", 23, 63, "M"),
    ("1801", 19, 66, "M"),
    ("1806", 5, 69, "M"),
    ("1805", 8, 68, "S"),
    ("1803", 11, 67, "S"),
    ("1802", 13, 67, "S"),
    ("1795", 23, 66, "M"),

    # Bottom-center
    ("1809", 26, 71, "M"),
    ("1812", 29, 73, "M"),
    ("1811", 23, 77, "M"),
    ("1810", 21, 79, "M"),
    ("1813", 29, 79, "M"),
    ("1816", 34, 80, "M"),
    ("1820", 39, 79, "M"),
    ("1826", 39, 73, "M"),
    ("1839", 43, 63, "M"),
    ("1845", 48, 63, "M"),
    ("1847", 51, 67, "M"),
    ("1852", 49, 73, "M"),
    ("1853", 49, 77, "M"),

    # Bottom-center-right
    ("1860", 54, 73, "S"),
    ("1864", 56, 75, "S"),
    ("1865", 56, 79, "S"),
    ("1866", 56, 81, "S"),
    ("1868", 61, 83, "S"),
    ("1874", 64, 83, "S"),
    ("1878", 69, 83, "S"),
    ("1877", 71, 79, "S"),
    ("1879", 66, 77, "M"),
    ("1884", 72, 72, "XL"),

    # Bottom-right
    ("1885", 79, 61, "M"),
    ("1896", 83, 69, "M"),
    ("1897", 86, 73, "M"),
    ("1898", 88, 75, "M"),
    ("1903", 89, 79, "S"),
    ("1901", 88, 81, "S"),
    ("1905", 91, 81, "S"),
    ("1908", 94, 83, "M"),
    ("1913", 93, 71, "M"),
    ("1910", 94, 77, "M"),
    ("1914", 97, 79, "S"),
    ("1915", 97, 83, "S"),
    ("1888", 89, 61, "S"),
    ("1889", 89, 63, "S"),
    ("1894", 86, 66, "M"),
]


# ═══════════════════════════════════════════════════════════════════════
# Zone Classification
# ═══════════════════════════════════════════════════════════════════════

# Explicitly mark some plots as commercial (market / bazaar area)
COMMERCIAL_PLOTS = {
    "1397", "1398", "1399", "1401", "1392", "1391",
    "1381", "1388", "1408", "1409", "1405", "1406",
    "1726", "1723", "1728", "1707", "1708",
}

# Explicitly mark some plots as government / institutional
GOVT_PLOTS = {
    "5111", "1326", "1343", "1387", "1886", "1884",
    "1518", "1478", "1696",
}


def classify_zone(plot_num, norm_x, norm_y, size_cat):
    """Classify a plot into a development zone."""
    if plot_num in COMMERCIAL_PLOTS:
        return "COM"
    if plot_num in GOVT_PLOTS:
        return "GOV"
    if size_cat == "XL":
        return "AGR"   # agricultural / open
    if size_cat == "L":
        return "GOV"
    if size_cat == "S":
        return "RES_DENSE"
    return "RES_MED"


def zone_to_building_params(zone, size_cat):
    """
    Returns (min_floors, max_floors, units_per_floor, building_type_label).
    """
    if zone == "RES_DENSE":
        return (3, 7, random.choice([2, 4]), "Multi-Storey Residential Apartments")
    elif zone == "RES_MED":
        return (2, 4, 2, "Residential Duplex / Walk-Up Flats")
    elif zone == "COM":
        return (2, 4, random.choice([2, 3, 4]), "Commercial Market / Shops & Offices")
    elif zone == "GOV":
        return (1, 2, 1, "Government / Institutional Building")
    elif zone == "AGR":
        return (1, 1, 1, "Agricultural Land / Open Plot")
    else:
        return (2, 3, 2, "Mixed Use Building")


# ═══════════════════════════════════════════════════════════════════════
# Owner Name Generator
# ═══════════════════════════════════════════════════════════════════════

_owner_counter = 0


def _random_owner():
    global _owner_counter
    _owner_counter += 1
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def _get_owner(zone, unit_index=0):
    if zone == "COM":
        return random.choice(COMMERCIAL_OWNERS)
    elif zone == "GOV":
        return random.choice(GOVT_OWNERS)
    else:
        return _random_owner()


# ═══════════════════════════════════════════════════════════════════════
# ULPIN Generator
# ═══════════════════════════════════════════════════════════════════════

def make_ulpin(plot_num, building_id, floor_no, unit_id, space_type):
    """
    Construct a unique 3D ULPIN string.
    Format: STATE-DISTRICT-TEHSIL-VILLAGE-PLOTxxxx-BLDxx-Fxx-UNITxx-TYPE
    """
    floor_code = f"F{floor_no:02d}" if floor_no >= 0 else f"FB{abs(floor_no)}"
    return f"{STATE}-{DISTRICT}-{TEHSIL}-{VILLAGE}-PLOT{plot_num}-{building_id}-{floor_code}-{unit_id}-{space_type}"


# ═══════════════════════════════════════════════════════════════════════
# World Coordinate Mapper
# ═══════════════════════════════════════════════════════════════════════

MAP_WORLD_WIDTH = 470.0    # meters
MAP_WORLD_DEPTH = 390.0    # meters


def norm_to_world(norm_x, norm_y):
    """Convert normalised (0-100) map position to 3D world coordinates (x, z)."""
    world_x = (norm_x / 100.0) * MAP_WORLD_WIDTH - MAP_WORLD_WIDTH / 2.0
    world_z = (norm_y / 100.0) * MAP_WORLD_DEPTH - MAP_WORLD_DEPTH / 2.0
    return round(world_x, 1), round(world_z, 1)


def size_to_dimensions(size_cat):
    """Return approximate (width_m, depth_m) for a building footprint."""
    if size_cat == "S":
        w = random.uniform(8, 14)
        d = random.uniform(8, 12)
    elif size_cat == "M":
        w = random.uniform(12, 20)
        d = random.uniform(10, 16)
    elif size_cat == "L":
        w = random.uniform(18, 30)
        d = random.uniform(15, 24)
    else:  # XL
        w = random.uniform(28, 45)
        d = random.uniform(22, 35)
    return round(w, 1), round(d, 1)


# ═══════════════════════════════════════════════════════════════════════
# Main City Generator
# ═══════════════════════════════════════════════════════════════════════

def generate_cadastral_city():
    """
    Generate a full hypothetical city dataset from the cadastral map.
    Returns data in the same format as city_generator.generate_society_dataset().
    """
    random.seed(2026)
    np.random.seed(2026)

    buildings_meta = []
    units = []
    conflict_count = 0

    for plot_num, nx, ny, size_cat in CADASTRAL_PLOTS:
        zone = classify_zone(plot_num, nx, ny, size_cat)
        min_fl, max_fl, units_per_floor, btype = zone_to_building_params(zone, size_cat)
        num_floors = random.randint(min_fl, max_fl)

        world_x, world_z = norm_to_world(nx, ny)
        bld_w, bld_d = size_to_dimensions(size_cat)

        building_id = f"PLT{plot_num}"
        building_name = f"Plot {plot_num} — {btype}"

        # Space type for units
        space_type = "RES"
        if zone == "COM":
            space_type = "COM"
        elif zone == "GOV":
            space_type = "GOV"
        elif zone == "AGR":
            space_type = "AGR"

        rate = CIRCLE_RATES.get(space_type, CIRCLE_RATES["RES"])

        # Floor list: optional basement + ground + upper floors
        has_basement = zone in ("RES_DENSE", "COM") and num_floors >= 4
        floor_list = []
        if has_basement:
            floor_list.append(-1)
        floor_list.extend(list(range(0, num_floors + 1)))  # 0=ground, 1..N

        buildings_meta.append({
            "building_id": building_id,
            "name": building_name,
            "type": btype,
            "floors": floor_list,
            "center_pos": [world_x, 0, world_z],
            "dimensions": [bld_w, bld_d],
            "plot_number": plot_num,
            "zone": zone,
        })

        # ── Generate Basement Parking (if applicable) ──
        if has_basement:
            z_min_b = -1 * FLOOR_HEIGHT
            z_max_b = 0.0
            for p_idx in range(1, 3):
                p_id = f"PRK-{plot_num}-B{p_idx:02d}"
                units.append({
                    "building_id": building_id,
                    "building_name": building_name,
                    "floor_no": -1,
                    "unit_id": p_id,
                    "flat_label": f"Basement Parking Bay B-{p_idx:02d} (Plot {plot_num})",
                    "space_type": "PRK",
                    "owner": f"Resident Plot-{plot_num}",
                    "area_sqm": 25.0,
                    "height_m": FLOOR_HEIGHT,
                    "valuation_inr": int(25.0 * CIRCLE_RATES["PRK"]),
                    "z_min": round(z_min_b, 2),
                    "z_max": round(z_max_b, 2),
                    "plan_x1": 0.5 if p_idx == 1 else 5.2,
                    "plan_x2": 4.8 if p_idx == 1 else 9.5,
                    "plan_y1": 0.5,
                    "plan_y2": 4.8,
                    "ulpin": make_ulpin(plot_num, building_id, -1, p_id, "PRK"),
                    "conflict": False,
                    "conflict_details": None,
                })

        # ── Generate Ground Floor ──
        if zone == "COM":
            # Commercial ground floor: shops
            num_shops = min(units_per_floor, 4)
            shop_width = 9.0 / num_shops
            for s_idx in range(1, num_shops + 1):
                s_id = f"SHOP-{plot_num}-G{s_idx:02d}"
                area = round(random.uniform(30, 80), 1)
                units.append({
                    "building_id": building_id,
                    "building_name": building_name,
                    "floor_no": 0,
                    "unit_id": s_id,
                    "flat_label": f"Shop G-{s_idx:02d} ({_get_owner('COM')})",
                    "space_type": "COM",
                    "owner": _get_owner("COM"),
                    "area_sqm": area,
                    "height_m": FLOOR_HEIGHT,
                    "valuation_inr": int(area * CIRCLE_RATES["COM"]),
                    "z_min": 0.0,
                    "z_max": FLOOR_HEIGHT,
                    "plan_x1": round(0.5 + (s_idx - 1) * shop_width, 1),
                    "plan_x2": round(0.5 + s_idx * shop_width, 1),
                    "plan_y1": 0.5,
                    "plan_y2": 9.5,
                    "ulpin": make_ulpin(plot_num, building_id, 0, s_id, "COM"),
                    "conflict": False,
                    "conflict_details": None,
                })
        elif zone in ("GOV", "AGR"):
            # Single-unit ground floor
            g_id = f"G-{plot_num}-01"
            area = round(random.uniform(80, 300), 1) if zone == "GOV" else round(random.uniform(200, 1000), 1)
            owner = _get_owner(zone)
            units.append({
                "building_id": building_id,
                "building_name": building_name,
                "floor_no": 0,
                "unit_id": g_id,
                "flat_label": f"{owner}" if zone == "GOV" else f"Open Agricultural Land (Plot {plot_num})",
                "space_type": space_type,
                "owner": owner,
                "area_sqm": area,
                "height_m": FLOOR_HEIGHT,
                "valuation_inr": int(area * rate),
                "z_min": 0.0,
                "z_max": FLOOR_HEIGHT,
                "plan_x1": 0.5,
                "plan_x2": 9.5,
                "plan_y1": 0.5,
                "plan_y2": 9.5,
                "ulpin": make_ulpin(plot_num, building_id, 0, g_id, space_type),
                "conflict": False,
                "conflict_details": None,
            })
        else:
            # Residential ground floor — lobby / stairwell
            lobby_id = f"LOBBY-{plot_num}"
            units.append({
                "building_id": building_id,
                "building_name": building_name,
                "floor_no": 0,
                "unit_id": lobby_id,
                "flat_label": f"Entrance Lobby & Stairwell (Plot {plot_num})",
                "space_type": "UTL",
                "owner": f"RWA Plot-{plot_num}",
                "area_sqm": round(random.uniform(30, 80), 1),
                "height_m": FLOOR_HEIGHT,
                "valuation_inr": 0,
                "z_min": 0.0,
                "z_max": FLOOR_HEIGHT,
                "plan_x1": 0.5,
                "plan_x2": 9.5,
                "plan_y1": 0.5,
                "plan_y2": 9.5,
                "ulpin": make_ulpin(plot_num, building_id, 0, lobby_id, "UTL"),
                "conflict": False,
                "conflict_details": None,
            })

        # ── Generate Upper Floors (1 to num_floors) ──
        for fl in range(1, num_floors + 1):
            z_min_f = fl * FLOOR_HEIGHT
            z_max_f = z_min_f + FLOOR_HEIGHT

            actual_units = units_per_floor
            if zone in ("GOV", "AGR"):
                actual_units = 1
            if fl == num_floors and zone in ("RES_DENSE",) and num_floors >= 5:
                # Top floor = larger penthouse
                actual_units = 1

            unit_width = 9.0 / actual_units

            # Introduce rare boundary conflicts on dense residential plots
            is_conflict_floor = False
            if zone == "RES_DENSE" and fl == 2 and actual_units >= 2 and random.random() < 0.08:
                is_conflict_floor = True
                conflict_count += 1

            for u_idx in range(1, actual_units + 1):
                u_id = f"{plot_num}-{fl}{u_idx:02d}"

                if zone == "COM":
                    st = "COM"
                    label = f"Office/Shop {fl}{u_idx:02d} (Plot {plot_num})"
                    area = round(random.uniform(25, 70), 1)
                elif zone in ("GOV", "AGR"):
                    st = space_type
                    label = f"Room {fl}{u_idx:02d} (Plot {plot_num})"
                    area = round(random.uniform(60, 200), 1)
                else:
                    st = "RES"
                    bhk = random.choice(["1BHK", "2BHK", "3BHK"]) if size_cat == "S" else random.choice(["2BHK", "3BHK", "4BHK"])
                    if actual_units == 1 and fl == num_floors:
                        bhk = "4BHK Penthouse"
                        area = round(random.uniform(130, 200), 1)
                    else:
                        area = round(random.uniform(45, 120), 1)
                    label = f"Flat {fl}{u_idx:02d} ({bhk}) — Plot {plot_num}"

                valuation = int(area * rate * (1 + fl * 0.015))  # higher floors = premium

                # Boundary conflict overlap
                x1 = round(0.5 + (u_idx - 1) * unit_width, 1)
                x2 = round(0.5 + u_idx * unit_width, 1)
                if is_conflict_floor and u_idx == 1:
                    x2 = round(x2 + 0.6, 1)  # overlap into neighbour
                if is_conflict_floor and u_idx == 2:
                    x1 = round(x1 - 0.3, 1)  # overlap from neighbour

                conflict_detail = None
                if is_conflict_floor:
                    conflict_detail = f"Boundary overlap with adjacent flat on Floor {fl} (Plot {plot_num})"

                ulpin = make_ulpin(plot_num, building_id, fl, u_id, st)

                units.append({
                    "building_id": building_id,
                    "building_name": building_name,
                    "floor_no": fl,
                    "unit_id": u_id,
                    "flat_label": label,
                    "space_type": st,
                    "owner": _get_owner(zone),
                    "area_sqm": area,
                    "height_m": FLOOR_HEIGHT,
                    "valuation_inr": valuation,
                    "z_min": round(z_min_f, 2),
                    "z_max": round(z_max_f, 2),
                    "plan_x1": x1,
                    "plan_x2": x2,
                    "plan_y1": 0.5,
                    "plan_y2": 9.5,
                    "ulpin": ulpin,
                    "conflict": is_conflict_floor,
                    "conflict_details": conflict_detail,
                })

    # ── Synthetic LiDAR Point Cloud ──
    point_cloud = _generate_point_cloud(buildings_meta)

    # ── Summary ──
    total_floors_detected = max(
        (max(b["floors"]) for b in buildings_meta if b["floors"]),
        default=5
    ) + 2  # +basements

    return {
        "id": "RJ_JPR_MAP01",
        "name": CITY_NAME,
        "city": "Jaipur",
        "state": STATE,
        "district": DISTRICT,
        "village": VILLAGE,
        "surface_parcel": "CADASTRAL_MAP_2026",
        "gov_authority": GOV_AUTHORITY,
        "buildings": buildings_meta,
        "units": units,
        "point_cloud": point_cloud[:3000],
        "total_ulpins": len(units),
        "total_conflicts": conflict_count,
        "detected_floor_count": total_floors_detected,
    }


def _generate_point_cloud(buildings_meta, points_per_floor=30, noise=0.3):
    """Generate synthetic LiDAR point cloud for the cadastral city."""
    all_points = []

    for b in buildings_meta:
        for fl in b["floors"]:
            if fl < 0:
                continue
            center_z = (fl + 1) * FLOOR_HEIGHT - FLOOR_HEIGHT / 2.0
            z_vals = np.random.normal(loc=center_z, scale=noise, size=points_per_floor)
            for z in z_vals:
                dx = b["dimensions"][0] / 2.0
                dy = b["dimensions"][1] / 2.0
                px = b["center_pos"][0] + np.random.uniform(-dx, dx)
                py = b["center_pos"][2] + np.random.uniform(-dy, dy)
                all_points.append({
                    "x": round(float(px), 2),
                    "y": round(float(py), 2),
                    "z": round(float(z), 2),
                })

    # Ground scatter
    for _ in range(1200):
        px = np.random.uniform(-MAP_WORLD_WIDTH / 2, MAP_WORLD_WIDTH / 2)
        py = np.random.uniform(-MAP_WORLD_DEPTH / 2, MAP_WORLD_DEPTH / 2)
        pz = np.random.normal(0.0, 0.1)
        all_points.append({
            "x": round(float(px), 2),
            "y": round(float(py), 2),
            "z": round(float(pz), 2),
        })

    random.shuffle(all_points)
    return all_points


# ═══════════════════════════════════════════════════════════════════════
# CLI Entry Point
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    data = generate_cadastral_city()
    print(f"\n{'='*70}")
    print(f" CADASTRAL MAP → 3D CITY GENERATION COMPLETE")
    print(f"{'='*70}")
    print(f" City: {data['name']}")
    print(f" Total Plots (Buildings): {len(data['buildings'])}")
    print(f" Total 3D ULPINs Generated: {data['total_ulpins']}")
    print(f" Boundary Conflicts Detected: {data['total_conflicts']}")
    print(f" LiDAR Points: {len(data['point_cloud'])}")
    print(f"\n Sample ULPINs:")
    for u in data["units"][:10]:
        print(f"   {u['ulpin']}")
    print(f"{'='*70}\n")
