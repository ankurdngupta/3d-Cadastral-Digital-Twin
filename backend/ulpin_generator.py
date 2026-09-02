"""
3D ULPIN (Unique Land Parcel Identification Number) Generator
=============================================================
Encodes vertical 3D spatial parcels by combining administrative codes,
surface parcel IDs, building IDs, floor levels, and unit designations.
"""

STATE = "RJ"
DISTRICT = "KRL"
VILLAGE = "VLG023"
SURFACE_PARCEL = "P00456"


def generate_3d_ulpin(unit: dict) -> str:
    """
    Constructs a standardized 3D ULPIN string for a unit parcel.
    Format: [State]-[District]-[Village]-[SurfaceParcel]-[Building]-[Floor]-[Unit]-[SpaceType]
    """
    building_id = unit.get("building_id", "B01")
    floor_no = unit["floor_no"]
    floor_code = f"F{floor_no:02d}" if floor_no >= 0 else f"F-{abs(floor_no):01d}"
    unit_id = unit.get("unit_id", "U001")
    space_type = unit.get("space_type", "RES")

    return f"{STATE}-{DISTRICT}-{VILLAGE}-{SURFACE_PARCEL}-{building_id}-{floor_code}-{unit_id}-{space_type}"
