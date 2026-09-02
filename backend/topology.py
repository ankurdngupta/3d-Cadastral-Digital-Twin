"""
Topology Validation Module
==========================
Performs automated 3D Cadastral boundary validation using Shapely polygon
intersection logic to detect horizontal encroachments and illegal overlaps across buildings.
"""

from shapely.geometry import Polygon


def validate_topology(layout: list) -> list:
    """
    Validates spatial units per building and floor, flagging conflicting units with overlapping footprints.
    """
    by_bldg_floor = {}
    for unit in layout:
        key = (unit.get("building_id", "B01"), unit["floor_no"])
        by_bldg_floor.setdefault(key, []).append(unit)
        unit["conflict"] = False
        unit["conflict_details"] = None

    for (b_id, floor_no), units in by_bldg_floor.items():
        for i in range(len(units)):
            for j in range(i + 1, len(units)):
                a, b = units[i], units[j]
                poly_a = Polygon([
                    (a["plan_x1"], a["plan_y1"]),
                    (a["plan_x2"], a["plan_y1"]),
                    (a["plan_x2"], a["plan_y2"]),
                    (a["plan_x1"], a["plan_y2"])
                ])
                poly_b = Polygon([
                    (b["plan_x1"], b["plan_y1"]),
                    (b["plan_x2"], b["plan_y1"]),
                    (b["plan_x2"], b["plan_y2"]),
                    (b["plan_x1"], b["plan_y2"])
                ])

                if poly_a.intersects(poly_b):
                    overlap_area = poly_a.intersection(poly_b).area
                    if overlap_area > 0.01:
                        a["conflict"] = True
                        b["conflict"] = True
                        msg = f"Overlaps with {b.get('flat_label', b['unit_id'])} by {round(overlap_area * 2.0, 2)} sq m"
                        a["conflict_details"] = msg
                        b["conflict_details"] = f"Overlaps with {a.get('flat_label', a['unit_id'])} by {round(overlap_area * 2.0, 2)} sq m"

    return layout
