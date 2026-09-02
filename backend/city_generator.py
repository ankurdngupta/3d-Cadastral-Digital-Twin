"""
Automated Multi-City & Society Cadastral Generator Engine
=========================================================
Generates entire multi-tower residential societies, multi-tier underground parking,
subterranean metro corridors, elevated flyovers, and 3D utility infrastructure
in seconds without manual data entry.
"""

import math
import random
import json
import argparse
import numpy as np

FLOOR_HEIGHT = 3.0  # standard ceiling-to-ceiling height in meters

# Real-world Indian City Circle Rate Baselines (INR per sq.m)
CITY_CIRCLE_RATES = {
    "MUM": {"RES": 140000, "COM": 190000, "PRK": 60000},
    "GGN": {"RES": 110000, "COM": 150000, "PRK": 50000},
    "NOI": {"RES": 90000,  "COM": 130000, "PRK": 45000},
    "BLR": {"RES": 95000,  "COM": 135000, "PRK": 45000},
    "JPR": {"RES": 75000,  "COM": 110000, "PRK": 35000},
    "DEFAULT": {"RES": 80000, "COM": 120000, "PRK": 40000}
}

# Pre-Configured Premier Real-World Indian Societies
PRESET_SOCIETIES = [
    {
        "id": "HR_GGN_01",
        "name": "DLF The Magnolias & Golf Links",
        "city": "Gurugram",
        "state": "HR",
        "district": "GGN",
        "village": "SEC054",
        "surface_parcel": "P00892",
        "gov_authority": "Govt of Haryana · GMDA Urban Cadastre",
        "towers_count": 4,
        "floors_per_tower": 16,
        "has_flyover": True,
        "has_metro": True,
        "has_utilities": True,
        "conflict_tower": "T01",
        "conflict_floor": 2
    },
    {
        "id": "MH_MUM_01",
        "name": "Hiranandani Gardens & Lake View",
        "city": "Mumbai",
        "state": "MH",
        "district": "MUM",
        "village": "POW007",
        "surface_parcel": "CTS1048",
        "gov_authority": "Govt of Maharashtra · BMC / SRA 3D Cadastre",
        "towers_count": 4,
        "floors_per_tower": 18,
        "has_flyover": True,
        "has_metro": True,
        "has_utilities": True,
        "conflict_tower": "T02",
        "conflict_floor": 3
    },
    {
        "id": "KA_BLR_01",
        "name": "Prestige Shantiniketan Tech Society",
        "city": "Bengaluru",
        "state": "KA",
        "district": "BLR",
        "village": "WTF012",
        "surface_parcel": "SY0088",
        "gov_authority": "Govt of Karnataka · BBMP / Bhoomi 3D Cadastre",
        "towers_count": 4,
        "floors_per_tower": 15,
        "has_flyover": True,
        "has_metro": True,
        "has_utilities": True,
        "conflict_tower": "T01",
        "conflict_floor": 2
    },
    {
        "id": "UP_NOI_01",
        "name": "ATS Knightsbridge & Express Towers",
        "city": "Noida",
        "state": "UP",
        "district": "NOI",
        "village": "SEC150",
        "surface_parcel": "GH0001",
        "gov_authority": "Govt of Uttar Pradesh · NOIDA Revenue Authority",
        "towers_count": 4,
        "floors_per_tower": 16,
        "has_flyover": True,
        "has_metro": True,
        "has_utilities": True,
        "conflict_tower": "T03",
        "conflict_floor": 2
    },
    {
        "id": "RJ_JPR_01",
        "name": "Surya Heights & Royal Crest Society",
        "city": "Jaipur",
        "state": "RJ",
        "district": "JPR",
        "village": "VLG023",
        "surface_parcel": "P00456",
        "gov_authority": "Govt of Rajasthan · Revenue Dept / SIH 2026",
        "towers_count": 4,
        "floors_per_tower": 14,
        "has_flyover": True,
        "has_metro": True,
        "has_utilities": True,
        "conflict_tower": "T01",
        "conflict_floor": 2
    }
]


def generate_society_dataset(config: dict) -> dict:
    """
    Algorithmically generates a complete 3D Cadastral Digital Twin for a given society config:
    - Building metadata & 3D layout coordinates
    - Multi-floor apartment parcels with realistic carpet areas & valuations
    - 2-Tier underground parking bays
    - Subterranean Metro transit tunnel
    - Elevated Highway Flyover
    - 3D Subsurface Utility networks (Water, Gas, Power)
    - Synthetic LiDAR point clouds
    """
    random.seed(42)
    np.random.seed(42)

    soc_id = config.get("id", "SOC_01")
    soc_name = config.get("name", "Royal Society")
    city = config.get("city", "Jaipur")
    state = config.get("state", "RJ")
    district = config.get("district", "JPR")
    village = config.get("village", "VLG001")
    surface_parcel = config.get("surface_parcel", "P001")
    gov_auth = config.get("gov_authority", "Govt of India · 3D Cadastre")
    towers_count = config.get("towers_count", 4)
    floors_per_tower = config.get("floors_per_tower", 14)
    conflict_tower = config.get("conflict_tower", "T01")
    conflict_floor = config.get("conflict_floor", 2)

    rates = CITY_CIRCLE_RATES.get(district, CITY_CIRCLE_RATES["DEFAULT"])

    # Standard Tower Coordinates arranged in an aesthetic crescent around central park
    TOWER_COORDS = [
        {"id": "T01", "name": f"{soc_name} - Tower A", "center": [-32, 0, -16]},
        {"id": "T02", "name": f"{soc_name} - Tower B", "center": [-12, 0, -26]},
        {"id": "T03", "name": f"{soc_name} - Tower C", "center": [12, 0, -26]},
        {"id": "T04", "name": f"{soc_name} - Tower D", "center": [32, 0, -16]},
        {"id": "T05", "name": f"{soc_name} - Tower E", "center": [48, 0, 4]}
    ]

    buildings_meta = []
    units = []

    # 1. Generate Residential Towers & Apartments
    for i in range(min(towers_count, len(TOWER_COORDS))):
        tc = TOWER_COORDS[i]
        tower_id = tc["id"]
        tower_name = tc["name"]
        
        # Tower Floors: -2, -1, 0, 1 ... N
        floors_list = [-2, -1, 0] + list(range(1, floors_per_tower + 1))
        buildings_meta.append({
            "building_id": tower_id,
            "name": tower_name,
            "type": "Luxury High-Rise Apartments",
            "floors": floors_list,
            "center_pos": tc["center"],
            "dimensions": [16, 14]
        })

        # Basement Parking Levels (B1 & B2)
        for b_floor in [-2, -1]:
            z_min = b_floor * FLOOR_HEIGHT
            z_max = z_min + FLOOR_HEIGHT
            b_label = "B2" if b_floor == -2 else "B1"
            
            # 2 Dedicated Parking Bays per basement
            for p_num, px in enumerate([(0.5, 4.8), (5.2, 9.5)], 1):
                p_id = f"P-{tower_id}-{b_label}{p_num:02d}"
                ulpin = f"{state}-{district}-{village}-{surface_parcel}-{tower_id}-F-{abs(b_floor)}-{p_id}-PRK"
                units.append({
                    "building_id": tower_id,
                    "building_name": tower_name,
                    "floor_no": b_floor,
                    "unit_id": p_id,
                    "flat_label": f"Parking Bay {b_label}-{p_num:02d} ({tower_id})",
                    "space_type": "PRK",
                    "owner": f"Resident {tower_id}-{p_num}",
                    "area_sqm": 28.0,
                    "height_m": 3.0,
                    "valuation_inr": int(28.0 * rates["PRK"]),
                    "z_min": round(z_min, 2),
                    "z_max": round(z_max, 2),
                    "plan_x1": px[0], "plan_x2": px[1],
                    "plan_y1": 0.5, "plan_y2": 4.8,
                    "ulpin": ulpin,
                    "conflict": False,
                    "conflict_details": None
                })

        # Ground Floor: Grand Double-Height Lobby & Concierge
        g_ulpin = f"{state}-{district}-{village}-{surface_parcel}-{tower_id}-F00-LOBBY-UTL"
        units.append({
            "building_id": tower_id,
            "building_name": tower_name,
            "floor_no": 0,
            "unit_id": f"{tower_id}-LOBBY",
            "flat_label": f"{tower_name} Grand Lobby & Concierge",
            "space_type": "UTL",
            "owner": f"{soc_name} Condominium RWA",
            "area_sqm": 120.0,
            "height_m": 3.0,
            "valuation_inr": int(120.0 * rates["COM"] * 0.7),
            "z_min": 0.0,
            "z_max": 3.0,
            "plan_x1": 0.5, "plan_x2": 9.5,
            "plan_y1": 0.5, "plan_y2": 9.5,
            "ulpin": g_ulpin,
            "conflict": False,
            "conflict_details": None
        })

        # Residential Apartment Floors (1 to floors_per_tower)
        for fl in range(1, floors_per_tower + 1):
            z_min = fl * FLOOR_HEIGHT
            z_max = z_min + FLOOR_HEIGHT
            
            # Floor 14+ is Sky Villa Penthouse
            if fl == floors_per_tower:
                pent_id = f"{tower_id}-PENT{fl}"
                pent_ulpin = f"{state}-{district}-{village}-{surface_parcel}-{tower_id}-F{fl:02d}-{pent_id}-RES"
                units.append({
                    "building_id": tower_id,
                    "building_name": tower_name,
                    "floor_no": fl,
                    "unit_id": pent_id,
                    "flat_label": f"Royal Sky Villa Penthouse {fl}01",
                    "space_type": "RES",
                    "owner": f"Dr. {soc_name[:8]} Family & Trusts",
                    "area_sqm": 240.0,
                    "height_m": 3.0,
                    "valuation_inr": int(240.0 * rates["RES"] * 1.5),
                    "z_min": round(z_min, 2),
                    "z_max": round(z_max, 2),
                    "plan_x1": 0.5, "plan_x2": 9.5,
                    "plan_y1": 0.5, "plan_y2": 9.5,
                    "ulpin": pent_ulpin,
                    "conflict": False,
                    "conflict_details": None
                })
            else:
                # 2 Units per floor: Flat 01 and Flat 02
                is_conf = (tower_id == conflict_tower and fl == conflict_floor)
                x_mid_1 = 5.4 if is_conf else 4.8
                x_mid_2 = 5.1 if is_conf else 5.2

                # Flat 01
                f1_id = f"{tower_id}-{fl}01"
                f1_ulpin = f"{state}-{district}-{village}-{surface_parcel}-{tower_id}-F{fl:02d}-{f1_id}-RES"
                units.append({
                    "building_id": tower_id,
                    "building_name": tower_name,
                    "floor_no": fl,
                    "unit_id": f1_id,
                    "flat_label": f"Apartment {tower_id[1:]}-{fl}01 ({3 if fl < 10 else 4}BHK Luxury)",
                    "space_type": "RES",
                    "owner": "ABC" if (tower_id == "T01" and fl == 3) else f"Resident {tower_id}-{fl}01",
                    "area_sqm": 110.0,
                    "height_m": 3.0,
                    "valuation_inr": int(110.0 * (rates["RES"] + fl * 1200)),
                    "z_min": round(z_min, 2),
                    "z_max": round(z_max, 2),
                    "plan_x1": 0.5, "plan_x2": x_mid_1,
                    "plan_y1": 0.5, "plan_y2": 9.5,
                    "ulpin": f1_ulpin,
                    "conflict": is_conf,
                    "conflict_details": f"Overlaps with Apartment {tower_id[1:]}-{fl}02 by 5.4 sq m" if is_conf else None
                })

                # Flat 02
                f2_id = f"{tower_id}-{fl}02"
                f2_ulpin = f"{state}-{district}-{village}-{surface_parcel}-{tower_id}-F{fl:02d}-{f2_id}-RES"
                units.append({
                    "building_id": tower_id,
                    "building_name": tower_name,
                    "floor_no": fl,
                    "unit_id": f2_id,
                    "flat_label": f"Apartment {tower_id[1:]}-{fl}02 ({3 if fl < 10 else 4}BHK Luxury)",
                    "space_type": "RES",
                    "owner": f"Resident {tower_id}-{fl}02",
                    "area_sqm": 110.0,
                    "height_m": 3.0,
                    "valuation_inr": int(110.0 * (rates["RES"] + fl * 1200)),
                    "z_min": round(z_min, 2),
                    "z_max": round(z_max, 2),
                    "plan_x1": x_mid_2, "plan_x2": 9.5,
                    "plan_y1": 0.5, "plan_y2": 9.5,
                    "ulpin": f2_ulpin,
                    "conflict": is_conf,
                    "conflict_details": f"Overlaps with Apartment {tower_id[1:]}-{fl}01 by 5.4 sq m" if is_conf else None
                })

    # 2. Commercial Galleria Arcade
    com_id = "COM01"
    com_name = f"{soc_name} Galleria & Commercial Arcade"
    buildings_meta.append({
        "building_id": com_id,
        "name": com_name,
        "type": "Commercial & Retail Arcade",
        "floors": [-1, 0, 1],
        "center_pos": [0, 0, 26],
        "dimensions": [24, 12]
    })
    units.append({
        "building_id": com_id,
        "building_name": com_name,
        "floor_no": 0,
        "unit_id": "SHOP-01",
        "flat_label": "State Bank of India & 24/7 ATM",
        "space_type": "COM",
        "owner": "State Bank of India",
        "area_sqm": 120.0,
        "height_m": 3.0,
        "valuation_inr": int(120.0 * rates["COM"]),
        "z_min": 0.0, "z_max": 3.0,
        "plan_x1": 0.5, "plan_x2": 4.8, "plan_y1": 0.5, "plan_y2": 9.5,
        "ulpin": f"{state}-{district}-{village}-{surface_parcel}-{com_id}-F00-SHOP-01-COM",
        "conflict": False, "conflict_details": None
    })
    units.append({
        "building_id": com_id,
        "building_name": com_name,
        "floor_no": 0,
        "unit_id": "SHOP-02",
        "flat_label": "Apollo Pharmacy & Healthcare",
        "space_type": "COM",
        "owner": "Apollo Medicos Retail Ltd",
        "area_sqm": 110.0,
        "height_m": 3.0,
        "valuation_inr": int(110.0 * rates["COM"]),
        "z_min": 0.0, "z_max": 3.0,
        "plan_x1": 5.2, "plan_x2": 9.5, "plan_y1": 0.5, "plan_y2": 9.5,
        "ulpin": f"{state}-{district}-{village}-{surface_parcel}-{com_id}-F00-SHOP-02-COM",
        "conflict": False, "conflict_details": None
    })

    # 3. Infrastructure: Metro, Flyover & Utility Grid
    if config.get("has_metro", True):
        mtr_id = "INF_MTR"
        mtr_name = f"{city} Metro Line 3 Transit Tunnel"
        buildings_meta.append({
            "building_id": mtr_id,
            "name": mtr_name,
            "type": "Subterranean Rail Transit",
            "floors": [-5],
            "center_pos": [0, -15, -42],
            "dimensions": [180, 8]
        })
        units.append({
            "building_id": mtr_id,
            "building_name": mtr_name,
            "floor_no": -5,
            "unit_id": "METRO-T01",
            "flat_label": "Metro Underground Transit Right-of-Way",
            "space_type": "MTR",
            "owner": f"{city} Metro Rail Corporation (Govt)",
            "area_sqm": 1440.0,
            "height_m": 4.0,
            "valuation_inr": 55000000,
            "z_min": -17.0, "z_max": -13.0,
            "plan_x1": -70.0, "plan_x2": 70.0, "plan_y1": -46.0, "plan_y2": -38.0,
            "ulpin": f"{state}-{district}-{village}-{surface_parcel}-{mtr_id}-F-5-METRO-T01-MTR",
            "conflict": False, "conflict_details": None
        })

    if config.get("has_flyover", True):
        fly_id = "INF_FLY"
        fly_name = f"{city} Elevated Expressway Flyover Corridor"
        buildings_meta.append({
            "building_id": fly_id,
            "name": fly_name,
            "type": "Elevated Highway Infrastructure",
            "floors": [3],
            "center_pos": [0, 9, 54],
            "dimensions": [160, 12]
        })
        units.append({
            "building_id": fly_id,
            "building_name": fly_name,
            "floor_no": 3,
            "unit_id": "FLYOVR-S01",
            "flat_label": "Elevated Flyover Expressway Deck (Air Rights)",
            "space_type": "FLY",
            "owner": "National Highways Authority of India (NHAI)",
            "area_sqm": 1600.0,
            "height_m": 3.0,
            "valuation_inr": 78000000,
            "z_min": 7.5, "z_max": 10.5,
            "plan_x1": -80.0, "plan_x2": 80.0, "plan_y1": 48.0, "plan_y2": 60.0,
            "ulpin": f"{state}-{district}-{village}-{surface_parcel}-{fly_id}-F03-FLYOVR-S01-FLY",
            "conflict": False, "conflict_details": None
        })

    if config.get("has_utilities", True):
        utl_id = "INF_UTL"
        utl_name = f"{soc_name} Subsurface Utility Grid"
        buildings_meta.append({
            "building_id": utl_id,
            "name": utl_name,
            "type": "Underground Municipal Utilities",
            "floors": [-1],
            "center_pos": [0, -3, 0],
            "dimensions": [120, 120]
        })
        units.append({
            "building_id": utl_id,
            "building_name": utl_name,
            "floor_no": -1,
            "unit_id": "UTL-WTR",
            "flat_label": f"Municipal Potable Water Supply Line ({city})",
            "space_type": "UTL",
            "owner": f"{state} Public Health Engineering Board",
            "area_sqm": 320.0,
            "height_m": 1.5,
            "valuation_inr": 11000000,
            "z_min": -3.5, "z_max": -2.0,
            "plan_x1": -60.0, "plan_x2": 60.0, "plan_y1": 42.0, "plan_y2": 46.0,
            "ulpin": f"{state}-{district}-{village}-{surface_parcel}-{utl_id}-F-1-UTL-WTR-UTL",
            "conflict": False, "conflict_details": None
        })

    # Synthetic LiDAR point clouds
    point_cloud = []
    for b in buildings_meta:
        if b["building_id"].startswith("INF_MTR"):
            continue
        for fl in b["floors"]:
            if fl < 0:
                continue
            center_z = (fl + 1) * FLOOR_HEIGHT - FLOOR_HEIGHT / 2
            z_vals = np.random.normal(loc=center_z, scale=0.22, size=140)
            for z in z_vals:
                dx = b["dimensions"][0] / 2
                dy = b["dimensions"][1] / 2
                px = b["center_pos"][0] + np.random.uniform(-dx, dx)
                py = b["center_pos"][2] + np.random.uniform(-dy, dy)
                point_cloud.append({"x": round(float(px), 2), "y": round(float(py), 2), "z": round(float(z), 2)})

    for _ in range(600):
        px = np.random.uniform(-70, 70)
        py = np.random.uniform(-50, 70)
        pz = np.random.normal(0.0, 0.08)
        point_cloud.append({"x": round(float(px), 2), "y": round(float(py), 2), "z": round(float(pz), 2)})

    random.shuffle(point_cloud)

    return {
        "id": soc_id,
        "name": soc_name,
        "city": city,
        "state": state,
        "district": district,
        "village": village,
        "surface_parcel": surface_parcel,
        "gov_authority": gov_auth,
        "buildings": buildings_meta,
        "units": units,
        "point_cloud": point_cloud[:2200],
        "total_ulpins": len(units),
        "total_conflicts": sum(1 for u in units if u.get("conflict", False)),
        "detected_floor_count": floors_per_tower + 3  # + basements & ground
    }


def build_all_societies_dataset():
    """
    Builds the multi-city dataset for all pre-configured societies.
    """
    all_societies = {}
    for cfg in PRESET_SOCIETIES:
        dataset = generate_society_dataset(cfg)
        all_societies[cfg["id"]] = dataset
    return all_societies


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automated Indian City & Society Cadastral Generator")
    parser.add_argument("--add-society", type=str, help="Name of new society")
    parser.add_argument("--city", type=str, default="Gurugram", help="City name")
    parser.add_argument("--state", type=str, default="HR", help="State code (e.g. HR, MH, KA, UP, RJ)")
    parser.add_argument("--district", type=str, default="GGN", help="District code")
    parser.add_argument("--towers", type=int, default=4, help="Number of residential towers")
    parser.add_argument("--floors", type=int, default=16, help="Floors per tower")
    args = parser.parse_args()

    if args.add_society:
        new_cfg = {
            "id": f"{args.state}_{args.district}_{random.randint(10, 99)}",
            "name": args.add_society,
            "city": args.city,
            "state": args.state,
            "district": args.district,
            "village": "SEC001",
            "surface_parcel": "P00100",
            "gov_authority": f"Govt of {args.state} · {args.city} 3D Cadastre",
            "towers_count": args.towers,
            "floors_per_tower": args.floors
        }
        res = generate_society_dataset(new_cfg)
        print(f"\n[SUCCESS] Generated 3D Cadastre for '{args.add_society}' in {args.city}!")
        print(f" -> Total 3D ULPINs generated: {res['total_ulpins']}")
        print(f" -> High-rise towers: {args.towers} towers ({args.floors} floors each)")
        print(f" -> Example 3D ULPIN: {res['units'][0]['ulpin']}")
    else:
        print("[INFO] Generating all pre-configured societies across India...")
        data = build_all_societies_dataset()
        for s_id, s_data in data.items():
            print(f" -> {s_data['city']} ({s_data['name']}): {s_data['total_ulpins']} 3D ULPINs")
        print("\nAll datasets built successfully!")
