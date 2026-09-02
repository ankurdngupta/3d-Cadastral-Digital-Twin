"""
Multi-Tower Luxury High-Rise Cadastral Data Generator for 3D ULPIN
==================================================================
Models a premier Indian high-rise gated society (Golf Course / DLF / Noida style)
with grand residential towers (Towers A, B, C, D), central landscaped lagoon & fountain plaza,
multi-level underground parking, subterranean metro transit, elevated flyover, and utility infrastructure.
"""

import math
import random
import numpy as np

random.seed(42)
np.random.seed(42)

FLOOR_HEIGHT = 3.0  # meters per floor

BUILDINGS_META = [
    {
        "building_id": "T01",
        "name": "Tower A (Royal Crest - 14 Storeys)",
        "type": "Luxury High-Rise Apartments",
        "floors": [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
        "center_pos": [-32, 0, -16],
        "dimensions": [16, 14]
    },
    {
        "building_id": "T02",
        "name": "Tower B (Imperial Palm - 16 Storeys)",
        "type": "Luxury High-Rise Apartments",
        "floors": [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
        "center_pos": [-12, 0, -26],
        "dimensions": [16, 14]
    },
    {
        "building_id": "T03",
        "name": "Tower C (Grand Horizon - 16 Storeys)",
        "type": "Luxury High-Rise Apartments",
        "floors": [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
        "center_pos": [12, 0, -26],
        "dimensions": [16, 14]
    },
    {
        "building_id": "T04",
        "name": "Tower D (Emerald Heights - 14 Storeys)",
        "type": "Luxury High-Rise Apartments",
        "floors": [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
        "center_pos": [32, 0, -16],
        "dimensions": [16, 14]
    },
    {
        "building_id": "COM01",
        "name": "Society Galleria & Commercial Arcade",
        "type": "Commercial & Retail Arcade",
        "floors": [-1, 0, 1, 2],
        "center_pos": [0, 0, 26],
        "dimensions": [24, 12]
    },
    {
        "building_id": "INF_FLY",
        "name": "NH-21 Elevated Flyover Corridor",
        "type": "Elevated Highway Infrastructure",
        "floors": [3],
        "center_pos": [0, 9, 54],
        "dimensions": [160, 12]
    },
    {
        "building_id": "INF_MTR",
        "name": "City Metro Line 3 Transit Tunnel",
        "type": "Subterranean Rail Transit",
        "floors": [-5],
        "center_pos": [0, -15, -42],
        "dimensions": [180, 8]
    },
    {
        "building_id": "INF_UTL",
        "name": "Society Central Subsurface Utility Grid",
        "type": "Underground Municipal Utilities",
        "floors": [-1],
        "center_pos": [0, -3, 0],
        "dimensions": [120, 120]
    }
]


def generate_point_cloud(points_per_floor: int = 180, noise: float = 0.22):
    """
    Generates synthetic 3D LiDAR point cloud returns across the high-rise society towers,
    flyover, and landscaped grounds.
    """
    all_points = []
    for b in BUILDINGS_META:
        if b["building_id"].startswith("INF_MTR"):
            continue
        for floor_no in b["floors"]:
            if floor_no < 0:
                continue
            center_z = (floor_no + 1) * FLOOR_HEIGHT - FLOOR_HEIGHT / 2
            z_vals = np.random.normal(loc=center_z, scale=noise, size=points_per_floor)
            for z in z_vals:
                dx = b["dimensions"][0] / 2
                dy = b["dimensions"][1] / 2
                px = b["center_pos"][0] + np.random.uniform(-dx, dx)
                py = b["center_pos"][2] + np.random.uniform(-dy, dy)
                all_points.append({"x": round(float(px), 2), "y": round(float(py), 2), "z": round(float(z), 2)})

    # Landscape ground points
    for _ in range(800):
        px = np.random.uniform(-70, 70)
        py = np.random.uniform(-50, 70)
        pz = np.random.normal(0.0, 0.08)
        all_points.append({"x": round(float(px), 2), "y": round(float(py), 2), "z": round(float(pz), 2)})

    random.shuffle(all_points)
    return all_points


def make_building_layout():
    """
    Generates 3D Cadastral parcels across:
    - Tower A (Royal Crest) 14 Storeys
    - Tower B (Imperial Palm) 16 Storeys
    - Tower C (Grand Horizon) 16 Storeys
    - Tower D (Emerald Heights) 14 Storeys
    - Commercial Galleria
    - Underground Parking Levels B1 & B2
    - Subterranean Metro Transit Tunnel
    - Elevated Highway Flyover
    - Utility Infrastructure Corridors
    """
    layout = []

    def add_parcels(building_id, building_name, floor_no, units):
        z_min = floor_no * FLOOR_HEIGHT
        z_max = z_min + FLOOR_HEIGHT
        for u in units:
            u["building_id"] = building_id
            u["building_name"] = building_name
            u["floor_no"] = floor_no
            if "z_min" not in u:
                u["z_min"] = round(z_min, 2)
            if "z_max" not in u:
                u["z_max"] = round(z_max, 2)
            u["height_m"] = round(u["z_max"] - u["z_min"], 1)
            width = abs(u["plan_x2"] - u["plan_x1"])
            depth = abs(u["plan_y2"] - u["plan_y1"])
            if "area_sqm" not in u:
                u["area_sqm"] = round(width * depth * 2.2, 1)
            if "valuation_inr" not in u:
                rate = 85000 if u.get("space_type") == "RES" else (125000 if u.get("space_type") == "COM" else 40000)
                u["valuation_inr"] = int(u["area_sqm"] * rate)
        layout.extend(units)

    # -------------------------------------------------------------
    # 1. TOWER A (Royal Crest - 14 Storeys)
    # -------------------------------------------------------------
    b_id = "T01"
    b_name = "Tower A (Royal Crest - 14 Storeys)"

    # Basements
    add_parcels(b_id, b_name, -2, [
        { "unit_id": "TA-P201", "flat_label": "Parking Bay TA-P201 (EV)", "space_type": "PRK", "owner": "Rajesh Sharma", "area_sqm": 28.0, "valuation_inr": 550000, "plan_x1": 0.5, "plan_x2": 4.8, "plan_y1": 0.5, "plan_y2": 4.8 },
        { "unit_id": "TA-P202", "flat_label": "Parking Bay TA-P202", "space_type": "PRK", "owner": "Priya Verma", "area_sqm": 28.0, "valuation_inr": 500000, "plan_x1": 5.2, "plan_x2": 9.5, "plan_y1": 0.5, "plan_y2": 4.8 }
    ])
    add_parcels(b_id, b_name, -1, [
        { "unit_id": "TA-P101", "flat_label": "Parking Bay TA-P101", "space_type": "PRK", "owner": "Vikram Malhotra", "area_sqm": 28.0, "valuation_inr": 550000, "plan_x1": 0.5, "plan_x2": 4.8, "plan_y1": 0.5, "plan_y2": 4.8 },
        { "unit_id": "TA-UTL", "flat_label": "Tower A Plant & HVAC Substation", "space_type": "UTL", "owner": "Society RWA Maintenance", "area_sqm": 65.0, "valuation_inr": 2000000, "plan_x1": 5.2, "plan_x2": 9.5, "plan_y1": 5.2, "plan_y2": 9.5 }
    ])

    # Ground: Grand Double-Height Lobby & Concierge
    add_parcels(b_id, b_name, 0, [
        { "unit_id": "TA-G01", "flat_label": "Tower A Grand Lobby & Concierge", "space_type": "UTL", "owner": "Society Condominium RWA", "area_sqm": 120.0, "valuation_inr": 8500000, "plan_x1": 0.5, "plan_x2": 9.5, "plan_y1": 0.5, "plan_y2": 9.5 }
    ])

    # Floors 1 to 14: Luxury Apartments (3BHK / 4BHK)
    for fl in range(1, 14):
        # Intentional encroachment conflict on Floor 2
        is_conf = (fl == 2)
        x_mid_1 = 5.4 if is_conf else 4.8
        x_mid_2 = 5.1 if is_conf else 5.2

        add_parcels(b_id, b_name, fl, [
            {
                "unit_id": f"A{fl}01",
                "flat_label": f"Apartment A-{fl}01 (3BHK Luxury)",
                "space_type": "RES",
                "owner": "ABC" if fl == 3 else f"Resident A{fl}01",
                "area_sqm": 110.0,
                "valuation_inr": 9200000 + fl * 120000,
                "plan_x1": 0.5, "plan_x2": x_mid_1, "plan_y1": 0.5, "plan_y2": 9.5
            },
            {
                "unit_id": f"A{fl}02",
                "flat_label": f"Apartment A-{fl}02 (3BHK Luxury)",
                "space_type": "RES",
                "owner": f"Resident A{fl}02",
                "area_sqm": 110.0,
                "valuation_inr": 9200000 + fl * 120000,
                "plan_x1": x_mid_2, "plan_x2": 9.5, "plan_y1": 0.5, "plan_y2": 9.5
            }
        ])

    # Floor 14: Sky Villa Penthouse
    add_parcels(b_id, b_name, 14, [
        {
            "unit_id": "TA-PENT14",
            "flat_label": "Royal Sky Villa Penthouse 1401",
            "space_type": "RES",
            "owner": "Dr. Arvind Joshi & Family",
            "area_sqm": 240.0,
            "valuation_inr": 28500000,
            "plan_x1": 0.5, "plan_x2": 9.5, "plan_y1": 0.5, "plan_y2": 9.5
        }
    ])

    # -------------------------------------------------------------
    # 2. TOWER B (Imperial Palm - 16 Storeys)
    # -------------------------------------------------------------
    b_id = "T02"
    b_name = "Tower B (Imperial Palm - 16 Storeys)"

    add_parcels(b_id, b_name, 0, [
        { "unit_id": "TB-G01", "flat_label": "Tower B Reception & Resident Lounge", "space_type": "UTL", "owner": "Society RWA", "area_sqm": 120.0, "valuation_inr": 8500000, "plan_x1": 0.5, "plan_x2": 9.5, "plan_y1": 0.5, "plan_y2": 9.5 }
    ])
    for fl in range(1, 17):
        add_parcels(b_id, b_name, fl, [
            {
                "unit_id": f"B{fl}01",
                "flat_label": f"Apartment B-{fl}01 (4BHK Golf View)",
                "space_type": "RES",
                "owner": f"Resident B{fl}01",
                "area_sqm": 125.0,
                "valuation_inr": 11500000 + fl * 150000,
                "plan_x1": 0.5, "plan_x2": 4.8, "plan_y1": 0.5, "plan_y2": 9.5
            },
            {
                "unit_id": f"B{fl}02",
                "flat_label": f"Apartment B-{fl}02 (4BHK Golf View)",
                "space_type": "RES",
                "owner": f"Resident B{fl}02",
                "area_sqm": 125.0,
                "valuation_inr": 11500000 + fl * 150000,
                "plan_x1": 5.2, "plan_x2": 9.5, "plan_y1": 0.5, "plan_y2": 9.5
            }
        ])

    # -------------------------------------------------------------
    # 3. TOWER C (Grand Horizon - 16 Storeys)
    # -------------------------------------------------------------
    b_id = "T03"
    b_name = "Tower C (Grand Horizon - 16 Storeys)"

    add_parcels(b_id, b_name, 0, [
        { "unit_id": "TC-G01", "flat_label": "Tower C Grand Portico Lobby", "space_type": "UTL", "owner": "Society RWA", "area_sqm": 120.0, "valuation_inr": 8500000, "plan_x1": 0.5, "plan_x2": 9.5, "plan_y1": 0.5, "plan_y2": 9.5 }
    ])
    for fl in range(1, 17):
        add_parcels(b_id, b_name, fl, [
            {
                "unit_id": f"C{fl}01",
                "flat_label": f"Apartment C-{fl}01 (3BHK Park View)",
                "space_type": "RES",
                "owner": f"Resident C{fl}01",
                "area_sqm": 115.0,
                "valuation_inr": 10200000 + fl * 130000,
                "plan_x1": 0.5, "plan_x2": 4.8, "plan_y1": 0.5, "plan_y2": 9.5
            },
            {
                "unit_id": f"C{fl}02",
                "flat_label": f"Apartment C-{fl}02 (3BHK Park View)",
                "space_type": "RES",
                "owner": f"Resident C{fl}02",
                "area_sqm": 115.0,
                "valuation_inr": 10200000 + fl * 130000,
                "plan_x1": 5.2, "plan_x2": 9.5, "plan_y1": 0.5, "plan_y2": 9.5
            }
        ])

    # -------------------------------------------------------------
    # 4. TOWER D (Emerald Heights - 14 Storeys)
    # -------------------------------------------------------------
    b_id = "T04"
    b_name = "Tower D (Emerald Heights - 14 Storeys)"

    add_parcels(b_id, b_name, 0, [
        { "unit_id": "TD-G01", "flat_label": "Tower D Clubhouse & Aerobics Center", "space_type": "UTL", "owner": "Society RWA", "area_sqm": 140.0, "valuation_inr": 9500000, "plan_x1": 0.5, "plan_x2": 9.5, "plan_y1": 0.5, "plan_y2": 9.5 }
    ])
    for fl in range(1, 15):
        add_parcels(b_id, b_name, fl, [
            {
                "unit_id": f"D{fl}01",
                "flat_label": f"Apartment D-{fl}01 (3BHK Luxury)",
                "space_type": "RES",
                "owner": f"Resident D{fl}01",
                "area_sqm": 110.0,
                "valuation_inr": 9500000 + fl * 120000,
                "plan_x1": 0.5, "plan_x2": 4.8, "plan_y1": 0.5, "plan_y2": 9.5
            },
            {
                "unit_id": f"D{fl}02",
                "flat_label": f"Apartment D-{fl}02 (3BHK Luxury)",
                "space_type": "RES",
                "owner": f"Resident D{fl}02",
                "area_sqm": 110.0,
                "valuation_inr": 9500000 + fl * 120000,
                "plan_x1": 5.2, "plan_x2": 9.5, "plan_y1": 0.5, "plan_y2": 9.5
            }
        ])

    # -------------------------------------------------------------
    # 5. COMMERCIAL GALLERIA & ARCADE
    # -------------------------------------------------------------
    b_id = "COM01"
    b_name = "Society Galleria & Commercial Arcade"

    add_parcels(b_id, b_name, 0, [
        { "unit_id": "SHOP-01", "flat_label": "State Bank of India & 24/7 ATM", "space_type": "COM", "owner": "State Bank of India", "area_sqm": 120.0, "valuation_inr": 16000000, "plan_x1": 0.5, "plan_x2": 4.8, "plan_y1": 0.5, "plan_y2": 9.5 },
        { "unit_id": "SHOP-02", "flat_label": "Apollo Pharmacy & Health Mart", "space_type": "COM", "owner": "Apollo Medicos Retail", "area_sqm": 110.0, "valuation_inr": 14000000, "plan_x1": 5.2, "plan_x2": 9.5, "plan_y1": 0.5, "plan_y2": 9.5 }
    ])
    add_parcels(b_id, b_name, 1, [
        { "unit_id": "OFF-01", "flat_label": "TechEdge IT & Innovation Hub", "space_type": "COM", "owner": "TechEdge Software Corp", "area_sqm": 115.0, "valuation_inr": 12500000, "plan_x1": 0.5, "plan_x2": 4.8, "plan_y1": 0.5, "plan_y2": 9.5 },
        { "unit_id": "OFF-02", "flat_label": "Vertex Financial & Wealth Advisory", "space_type": "COM", "owner": "Vertex Capital Pvt Ltd", "area_sqm": 115.0, "valuation_inr": 12500000, "plan_x1": 5.2, "plan_x2": 9.5, "plan_y1": 0.5, "plan_y2": 9.5 }
    ])

    # -------------------------------------------------------------
    # 6. INFRASTRUCTURE: Metro, Flyover & Utility Grid
    # -------------------------------------------------------------
    add_parcels("INF_MTR", "City Metro Line 3 Transit Tunnel", -5, [
        {
            "unit_id": "METRO-T01",
            "flat_label": "Metro Underground Transit Right-of-Way",
            "space_type": "MTR",
            "owner": "Metro Rail Corporation Ltd (Govt of Rajasthan)",
            "area_sqm": 1440.0,
            "valuation_inr": 55000000,
            "z_min": -17.0,
            "z_max": -13.0,
            "plan_x1": -70.0, "plan_x2": 70.0, "plan_y1": -46.0, "plan_y2": -38.0
        }
    ])

    add_parcels("INF_FLY", "NH-21 Elevated Flyover Corridor", 3, [
        {
            "unit_id": "FLYOVR-S01",
            "flat_label": "Elevated Flyover Expressway Deck (Air Rights)",
            "space_type": "FLY",
            "owner": "National Highways Authority of India (NHAI)",
            "area_sqm": 1600.0,
            "valuation_inr": 78000000,
            "z_min": 7.5,
            "z_max": 10.5,
            "plan_x1": -80.0, "plan_x2": 80.0, "plan_y1": 48.0, "plan_y2": 60.0
        }
    ])

    add_parcels("INF_UTL", "Society Central Subsurface Utility Grid", -1, [
        { "unit_id": "UTL-WTR", "flat_label": "Municipal Potable Water Supply Trunk Line", "space_type": "UTL", "owner": "Rajasthan PHED Water Board", "area_sqm": 320.0, "valuation_inr": 11000000, "z_min": -3.5, "z_max": -2.0, "plan_x1": -60.0, "plan_x2": 60.0, "plan_y1": 42.0, "plan_y2": 46.0 },
        { "unit_id": "UTL-GAS", "flat_label": "Piped Natural Gas (PNG) High-Pressure Grid", "space_type": "UTL", "owner": "Rajasthan State Gas Limited (RSGL)", "area_sqm": 240.0, "valuation_inr": 12000000, "z_min": -2.8, "z_max": -1.8, "plan_x1": -60.0, "plan_x2": 60.0, "plan_y1": 36.0, "plan_y2": 40.0 },
        { "unit_id": "UTL-PWR", "flat_label": "11kV Subterranean Power Distribution Conduit", "space_type": "UTL", "owner": "Jaipur Vidyut Vitran Nigam Ltd (JVVNL)", "area_sqm": 200.0, "valuation_inr": 14000000, "z_min": -2.2, "z_max": -1.2, "plan_x1": -30.0, "plan_x2": 30.0, "plan_y1": 6.0, "plan_y2": 10.0 }
    ])

    return layout
