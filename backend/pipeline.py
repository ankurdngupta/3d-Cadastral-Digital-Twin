"""
3D ULPIN Main Processing Pipeline (Multi-City & Society Integrated)
===================================================================
Coordinates automated generation across Indian cities (Gurugram, Mumbai, Bengaluru, Noida, Jaipur),
AI floor detection, 3D ULPIN code assignment, topology validation, database persistence, and dashboard compilation.

Now includes: Cadastral Map → 3D City generator for hypothetical village/town layouts.
"""

import json
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from city_generator import build_all_societies_dataset
from city_map_generator import generate_city_map_dataset
from floor_detector import detect_floors
from topology import validate_topology
from db_manager import save_to_sqlite


def export_dashboard(all_societies: dict, active_id: str = "HR_GGN_01"):
    """
    Exports clean JSON data with all multi-city societies and compiles the standalone interactive 3D dashboard.
    """
    active_soc = all_societies.get(active_id, list(all_societies.values())[0])

    data = {
        "active_society_id": active_id,
        "societies": all_societies,
        # Default active society properties for immediate rendering
        "buildings": active_soc["buildings"],
        "units": active_soc["units"],
        "point_cloud": active_soc["point_cloud"],
        "detected_floor_count": active_soc["detected_floor_count"],
        "total_ulpins": active_soc["total_ulpins"],
        "total_conflicts": active_soc["total_conflicts"],
        "society_name": active_soc["name"],
        "city": active_soc["city"],
        "state": active_soc["state"],
        "district": active_soc["district"],
        "village": active_soc["village"],
        "surface_parcel": active_soc["surface_parcel"],
        "gov_authority": active_soc["gov_authority"]
    }

    json_path = os.path.join(PROJECT_ROOT, "building_data.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    # Read frontend template components
    html_template_path = os.path.join(PROJECT_ROOT, "frontend", "index.html")
    css_path = os.path.join(PROJECT_ROOT, "frontend", "css", "style.css")
    js_app_path = os.path.join(PROJECT_ROOT, "frontend", "js", "app.js")
    js_three_path = os.path.join(PROJECT_ROOT, "frontend", "js", "three.min.js")

    if not os.path.exists(js_three_path):
        js_three_path = os.path.join(PROJECT_ROOT, "three.min.js")

    with open(html_template_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    with open(css_path, "r", encoding="utf-8") as f:
        css_content = f.read()
    with open(js_app_path, "r", encoding="utf-8") as f:
        app_js_content = f.read()
    with open(js_three_path, "r", encoding="utf-8") as f:
        three_js_content = f.read()

    final_html = html_content.replace("/* __STYLES__ */", css_content)
    final_html = final_html.replace("// __THREEJS_LIBRARY__", three_js_content)
    final_html = final_html.replace("window.__BUILDING_DATA__ = null;", f"window.__BUILDING_DATA__ = {json.dumps(data)};")
    final_html = final_html.replace("// __APP_LOGIC__", app_js_content)

    out_html = os.path.join(PROJECT_ROOT, "dashboard.html")
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(final_html)

    # Also write to index.html so VS Code Live Server opens directly
    index_html = os.path.join(PROJECT_ROOT, "index.html")
    with open(index_html, "w", encoding="utf-8") as f:
        f.write(final_html)


def run_pipeline():
    print("=" * 70)
    print(" [3D ULPIN GENERATION & INDIAN CADASTRE DIGITAL TWIN PIPELINE]")
    print("=" * 70)

    print("\n[1/7] Running Automated Multi-City & Society Cadastral Engine ...")
    all_societies = build_all_societies_dataset()

    # ── 3D City Map (Diverse Buildings) ──
    print("      -> Generating 3D City Map with diverse architecture ...")
    city_data = generate_city_map_dataset()
    all_societies[city_data["id"]] = city_data
    print(f"      -> City: {city_data['total_ulpins']} 3D ULPINs from {len(city_data['buildings'])} distinct buildings")

    print(f"      -> Generated {len(all_societies)} datasets across Indian States:")
    for s_id, s_data in all_societies.items():
        print(f"         - {s_data['city']} ({s_data['state']}): {s_data['name']} [{s_data['total_ulpins']} 3D ULPINs]")

    print("\n[2/7] Detecting floors from Point Cloud per society (AI Height Clustering) ...")
    active_soc = all_societies["HR_GGN_01"]
    z_points = [p["z"] for p in active_soc["point_cloud"]]
    detected_floors = detect_floors(z_points)
    print(f"      -> Detected {len(detected_floors)} vertical levels across active complex:")
    for i, fl in enumerate(detected_floors[:8]):
        print(f"         Level {i}: Elevation {fl['z_min']}m to {fl['z_max']}m ({fl['point_count']} points)")
    if len(detected_floors) > 8:
        print(f"         ... and {len(detected_floors) - 8} more upper floor levels detected.")

    print("\n[3/7] Defining 3D Building Floor & Unit Parcel Layouts for Towers & Infrastructure ...")
    for s_id, s_data in all_societies.items():
        s_data["units"] = validate_topology(s_data["units"])
    print(f"      -> Total {sum(len(s['units']) for s in all_societies.values())} 3D parcels validated across all cities")

    print("\n[4/7] Generating unique 3D ULPINs for each spatial unit ...")
    sample_ulpin = active_soc["units"][0]["ulpin"]
    print(f"      -> Example 3D ULPIN (Gurugram): {sample_ulpin}")

    print("\n[5/7] Running 3D Topology & Encroachment Validation ...")
    conflicts = [u for u in active_soc["units"] if u.get("conflict", False)]
    print(f"      -> {len(conflicts)} boundary conflict(s) identified in active society")
    for c in conflicts:
        print(f"         [!] CONFLICT: {c['ulpin']} ({c.get('conflict_details', '')})")

    print("\n[6/7] Storing Cadastral records into SQLite Database ...")
    db_file = os.path.join(PROJECT_ROOT, "ulpin_3d.db")
    all_units_flattened = []
    for s in all_societies.values():
        all_units_flattened.extend(s["units"])
    save_to_sqlite(all_units_flattened, db_file)
    print(f"      -> Saved {len(all_units_flattened)} 3D ULPIN records to ulpin_3d.db")

    print("\n[7/7] Exporting JSON and compiling 3D Web Dashboard ...")
    export_dashboard(all_societies, active_id="RJ_JPR_CITY01")
    print("      -> Exported building_data.json")
    print("      -> Generated standalone dashboard.html & index.html")

    print("\n" + "=" * 70)
    print(" PIPELINE COMPLETE! Open index.html in your browser.")
    print("=" * 70)


if __name__ == "__main__":
    run_pipeline()
