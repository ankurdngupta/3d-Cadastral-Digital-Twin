"""
City Map → Diverse 3D Buildings Generator
==========================================
Creates a hypothetical city from a bird's-eye city map with:
- 80 visually distinct buildings across 8 architectural types
- City blocks separated by streets and piazzas
- Each building has unique: height, color, shape, roof, facade
- Each apartment has room-level floor plans for 3D interior
- Full 3D ULPIN for every spatial unit
"""

import math, random, json
import numpy as np

random.seed(42)
np.random.seed(42)

FLOOR_HEIGHT = 3.2
STATE, DISTRICT, CITY = "RJ", "JPR", "Nagar Vatika"
VILLAGE, TEHSIL = "WRD01", "AMER"
GOV_AUTH = "Govt of Rajasthan · 3D Cadastral Digital Twin Platform (SIH 2026)"

# ─── Architectural Types ─────────────────────────────────────────────
ARCH_TYPES = {
    "modern_glass_tower":  {"label": "Modern Glass Tower",       "floors": (10, 20), "upf": (4, 6), "roof": "flat",    "shape": "rectangle"},
    "art_deco_tower":      {"label": "Art Deco High-Rise",       "floors": (8, 16),  "upf": (3, 4), "roof": "stepped", "shape": "rectangle"},
    "residential_block":   {"label": "Traditional Apartments",   "floors": (4, 7),   "upf": (2, 4), "roof": "pitched", "shape": "rectangle"},
    "low_rise_walk_up":    {"label": "Low-Rise Walk-Up Flats",   "floors": (3, 5),   "upf": (2, 3), "roof": "terrace", "shape": "rectangle"},
    "commercial_plaza":    {"label": "Commercial Market Complex","floors": (2, 4),   "upf": (3, 6), "roof": "flat",    "shape": "wide"},
    "heritage_palazzo":    {"label": "Heritage Palazzo",         "floors": (3, 5),   "upf": (2, 3), "roof": "dome",    "shape": "courtyard"},
    "civic_landmark":      {"label": "Civic / Govt Landmark",    "floors": (2, 4),   "upf": (1, 2), "roof": "dome",    "shape": "wide"},
    "villa_bungalow":      {"label": "Residential Villa",        "floors": (1, 3),   "upf": (1, 1), "roof": "pitched", "shape": "square"},
}

# ─── Facade Color Palettes (distinct per building) ────────────────────
FACADE_COLORS = [
    0xFAF8F5, 0xE8D5B7, 0xCC7A5A, 0xF5C4A1, 0xF5E6D3, 0xBFD7EA, 0xB2BDA0,
    0xD4A5A5, 0xC9A87C, 0xB0B7C0, 0xFFFFF0, 0xD2B48C, 0xF0EAD6, 0xF7E7CE,
    0xC0C0C0, 0xE0D2C3, 0xDDD5C8, 0xCDB79E, 0xBC8F8F, 0xD3C4A8, 0xA0522D,
    0xE6C9A8, 0xC8AD7F, 0xBDB395, 0x87CEEB, 0xDEB887, 0xFFE4C4, 0xF4A460,
    0xDAA520, 0xCD853F, 0xD2691E, 0x8B4513,
]
ACCENT_COLORS = [
    0x8B7355, 0x614B36, 0x4A3728, 0x6B5344, 0x5C4033, 0x3E2723, 0x795548,
    0x6D4C41, 0x5D4037, 0x4E342E, 0x3E2723, 0x2C1810,
]
GLASS_COLORS = [0x1C2833, 0x2C3E50, 0x1A5276, 0x154360, 0x0E3655, 0x212F3D]

# ─── Apartment Room Templates ────────────────────────────────────────
ROOM_TEMPLATES = {
    "1BHK": [
        {"type": "living", "label": "Living Room", "w": 4.5, "d": 4.0},
        {"type": "bedroom", "label": "Bedroom", "w": 3.5, "d": 3.5},
        {"type": "kitchen", "label": "Kitchen", "w": 2.5, "d": 2.5},
        {"type": "bathroom", "label": "Bathroom", "w": 2.0, "d": 1.8},
    ],
    "2BHK": [
        {"type": "living", "label": "Living + Dining", "w": 5.0, "d": 4.5},
        {"type": "bedroom", "label": "Master Bedroom", "w": 4.0, "d": 3.5},
        {"type": "bedroom", "label": "Bedroom 2", "w": 3.5, "d": 3.0},
        {"type": "kitchen", "label": "Kitchen", "w": 3.0, "d": 2.5},
        {"type": "bathroom", "label": "Bathroom 1", "w": 2.2, "d": 2.0},
        {"type": "bathroom", "label": "Bathroom 2", "w": 1.8, "d": 1.8},
    ],
    "3BHK": [
        {"type": "living", "label": "Drawing + Dining Hall", "w": 6.0, "d": 5.0},
        {"type": "bedroom", "label": "Master Suite", "w": 4.5, "d": 4.0},
        {"type": "bedroom", "label": "Bedroom 2", "w": 3.8, "d": 3.5},
        {"type": "bedroom", "label": "Bedroom 3", "w": 3.5, "d": 3.0},
        {"type": "kitchen", "label": "Modular Kitchen", "w": 3.5, "d": 3.0},
        {"type": "bathroom", "label": "Master Bath", "w": 2.5, "d": 2.5},
        {"type": "bathroom", "label": "Common Bath", "w": 2.0, "d": 2.0},
        {"type": "balcony", "label": "Balcony", "w": 4.0, "d": 1.5},
    ],
    "4BHK": [
        {"type": "living", "label": "Grand Living Hall", "w": 7.0, "d": 5.5},
        {"type": "bedroom", "label": "Master Suite", "w": 5.0, "d": 4.5},
        {"type": "bedroom", "label": "Bedroom 2", "w": 4.0, "d": 3.8},
        {"type": "bedroom", "label": "Bedroom 3", "w": 4.0, "d": 3.5},
        {"type": "bedroom", "label": "Guest Room", "w": 3.5, "d": 3.5},
        {"type": "kitchen", "label": "Island Kitchen", "w": 4.0, "d": 3.5},
        {"type": "bathroom", "label": "Master Bath", "w": 3.0, "d": 2.8},
        {"type": "bathroom", "label": "Common Bath", "w": 2.2, "d": 2.0},
        {"type": "bathroom", "label": "Guest Bath", "w": 2.0, "d": 1.8},
        {"type": "balcony", "label": "Terrace Balcony", "w": 5.0, "d": 2.0},
    ],
    "shop": [
        {"type": "shop_floor", "label": "Retail Area", "w": 6.0, "d": 5.0},
        {"type": "store", "label": "Storage", "w": 3.0, "d": 2.5},
    ],
    "office": [
        {"type": "open_plan", "label": "Open Office", "w": 8.0, "d": 6.0},
        {"type": "cabin", "label": "Manager Cabin", "w": 3.5, "d": 3.0},
        {"type": "meeting", "label": "Conference Room", "w": 4.0, "d": 3.5},
        {"type": "pantry", "label": "Pantry", "w": 2.5, "d": 2.0},
    ],
    "govt_hall": [
        {"type": "hall", "label": "Main Hall", "w": 10.0, "d": 8.0},
        {"type": "office", "label": "Officer's Room", "w": 4.0, "d": 3.5},
        {"type": "reception", "label": "Reception", "w": 5.0, "d": 3.0},
    ],
}

OWNER_FIRST = [
    "Rajesh","Sunil","Manoj","Vikram","Amit","Priya","Sunita","Kavita","Deepak",
    "Ramesh","Sanjay","Pooja","Neha","Ankit","Ravi","Mohan","Pankaj","Mahesh",
    "Nisha","Arjun","Kiran","Vikas","Suman","Dinesh","Harsh","Ajay","Govind",
    "Bharat","Divya","Gaurav","Hemant","Jyoti","Kamal","Mukesh","Rahul","Renu",
]
OWNER_LAST = [
    "Sharma","Verma","Gupta","Singh","Agarwal","Joshi","Meena","Yadav","Patel",
    "Chauhan","Malhotra","Saxena","Mishra","Rajput","Soni","Mathur","Shekhawat",
    "Rathore","Choudhary","Saini","Jain","Goyal","Bansal","Kapoor","Tandon",
]
SHOP_NAMES = [
    "Sharma General Store","Gupta Electronics","Rajasthan Sweets & Namkeen",
    "New Fashion Garments","Royal Medical Store","Jaipur Books & Stationery",
    "Verma Mobile Centre","Heritage Jewellers","Fresh Mart Groceries",
    "Digital Zone Computers","Sunrise Bakery","Metro Shoes","Modern Furniture House",
    "Star Beauty Parlour","Mehta Hardware","National Tailors","City Optics",
    "Green Pharmacy","Laxmi Cloth House","Quick Bite Restaurant",
]
GOVT_NAMES = [
    "Tehsil Revenue Office","Gram Panchayat Bhawan","Police Station",
    "Primary Health Centre","Govt Sr Sec School","Community Hall",
    "Post Office","Public Library","Jal Nigam Office","PWD Rest House",
]

# ═══════════════════════════════════════════════════════════════════════
# CITY BUILDING DEFINITIONS — 80 unique buildings in city blocks
# ═══════════════════════════════════════════════════════════════════════
#
# Road grid (buildings must NOT be placed on these):
#   Horizontal roads at z: -150(w8), -100(w12), -60(w6), 0(w10), 35(w6), 65(w8), 140(w8)
#   Vertical roads at x: -100(w10), 0(w10), 100(w10)
#
# Safe block zones (x_min, x_max, z_min, z_max):
#   Row A: z -144 to -108    Row B: z -92 to -65    Row C: z -55 to -7
#   Row D: z  7 to  30       Row E: z  40 to  59    Row F: z  71 to 134    Row G: z 146 to 185
#   Col 1: x -185 to -107    Col 2: x -88 to -7     Col 3: x  7 to  88    Col 4: x 107 to 185
#
# Format: (id, name, x, z, w, d, floors, arch_type, facade_idx, accent_idx, roof, zone, rotation)

_B = [
    # ═══ BLOCK A1 (NW far): x -185..-107, z -144..-108 ═══
    ("B01","Palazzo Municipale",       -160, -130, 26, 20, 4, "heritage_palazzo",  2, 1, "dome","GOV",0),
    ("B02","Torre della Piazza",       -130, -115, 12, 12,14, "art_deco_tower",    7, 3, "stepped","RES",0),
    ("B03","Casa Antica Nord",         -155, -122, 18, 14, 5, "residential_block", 1, 0, "pitched","RES",0),

    # ═══ BLOCK A2 (N center-left): x -88..-7, z -144..-108 ═══
    ("B04","Residenza Centrale",        -60, -130, 18, 14, 6, "residential_block", 3, 2, "pitched","RES",0),
    ("B05","Botteghe Antiche",          -35, -120, 22, 12, 3, "commercial_plaza",  4, 1, "flat","COM",0),
    ("B06","Villa Giardino",            -65, -122, 14, 12, 2, "villa_bungalow",   13, 6, "pitched","RES",0),

    # ═══ BLOCK A3 (N center-right): x 7..88, z -144..-108 ═══
    ("B07","Lakshmi Niwas",              30, -130, 18, 16, 7, "residential_block",16, 3, "pitched","RES",0),
    ("B08","Raj Bhawan Flats",           60, -120, 20, 14, 5, "residential_block",17, 4, "pitched","RES",0),
    ("B09","Patel Complex",              40, -122, 20, 16, 4, "low_rise_walk_up",  6, 2, "terrace","RES",0),

    # ═══ BLOCK A4 (NE far): x 107..185, z -144..-108 ═══
    ("B10","Krishna Kunj Tower",        130, -130, 14, 14,10, "art_deco_tower",   20, 3, "stepped","RES",0),
    ("B11","Saraswati Enclave",         155, -120, 18, 14, 4, "low_rise_walk_up", 21, 5, "terrace","RES",0),
    ("B12","Shanti Nagar Villa A",      130, -120, 12, 10, 2, "villa_bungalow",  18, 6, "pitched","RES",0),

    # ═══ BLOCK B1 (W upper): x -185..-107, z -92..-65 ═══
    ("B13","Govt Hospital Wing A",     -160, -80, 28, 14, 4, "civic_landmark",    0, 4, "flat","GOV",0),
    ("B14","Govt Hospital Wing B",     -135, -78, 20, 12, 3, "residential_block",15, 2, "flat","GOV",0),

    # ═══ BLOCK B2 (center-left upper): x -88..-7, z -92..-65 ═══
    ("B15","Central Library",           -60, -82, 20, 14, 3, "heritage_palazzo", 25, 1, "dome","GOV",0),
    ("B16","Corner Cafe Block",         -35, -75, 14, 10, 2, "commercial_plaza",  2, 1, "flat","COM",0),
    ("B17","Art Gallery",               -65, -75, 14, 10, 2, "heritage_palazzo", 12, 1, "flat","COM",0),

    # ═══ BLOCK B3 (center-right upper): x 7..88, z -92..-65 ═══
    ("B18","Student Hostel",             30, -82, 18, 14, 5, "low_rise_walk_up", 14, 2, "terrace","RES",0),
    ("B19","Fire Station",               60, -72, 16, 12, 2, "civic_landmark",    2, 0, "flat","GOV",0),

    # ═══ BLOCK B4 (E upper): x 107..185, z -92..-65 ═══
    ("B20","Metro Tech Hub",            130, -82, 16, 14,10, "modern_glass_tower", 0,11, "flat","COM",0),
    ("B21","Azure Heights",             155, -72, 12, 12,12, "modern_glass_tower", 0, 9, "flat","COM",0),

    # ═══ BLOCK C1 (W center): x -185..-107, z -55..-7 ═══
    ("B22","District Collectorate",    -160, -40, 26, 20, 3, "civic_landmark",    0, 4, "dome","GOV",0),
    ("B23","Municipal Corporation",    -140, -20, 22, 16, 3, "civic_landmark",   17, 1, "dome","GOV",0),
    ("B24","Police Headquarters",      -125, -30, 18, 14, 3, "heritage_palazzo", 10, 5, "flat","GOV",0),

    # ═══ BLOCK C2 (center-left center — OLD TOWN): x -88..-7, z -55..-7 ═══
    ("B25","Grand Cathedral",           -55, -40, 24, 20, 5, "heritage_palazzo",  0, 4, "dome","GOV",0),
    ("B26","Tempio Civico",             -30, -35, 20, 18, 3, "civic_landmark",    0, 4, "dome","GOV",0),
    ("B27","Heritage Haveli",           -60, -20, 20, 14, 3, "heritage_palazzo", 25, 1, "dome","RES",0),
    ("B28","Appartamenti Rosa",         -30, -18, 16, 12, 5, "low_rise_walk_up",  6, 2, "terrace","RES",0),

    # ═══ BLOCK C3 (center-right center): x 7..88, z -55..-7 ═══
    ("B29","Opera House",                35, -40, 24, 18, 4, "heritage_palazzo", 17, 1, "dome","GOV",0),
    ("B30","Torre Moderna Alpha",        65, -35, 14, 14,15, "modern_glass_tower", 0, 8, "flat","COM",0),
    ("B31","Victory Column Tower",       35, -18, 10, 10,22, "modern_glass_tower", 0, 8, "flat","GOV",0),
    ("B32","Prism Residences",           65, -20, 16, 12, 8, "residential_block", 14, 2, "pitched","RES",0),

    # ═══ BLOCK C4 (E center): x 107..185, z -55..-7 ═══
    ("B33","Crystal Business Tower",    130, -40, 16, 14,20, "modern_glass_tower", 0, 9, "flat","COM",0),
    ("B34","Sapphire Office Park",      160, -35, 18, 16,12, "modern_glass_tower", 0,10, "flat","COM",0),
    ("B35","Emerald Residence",         130, -20, 14, 12,16, "art_deco_tower",    8, 3, "stepped","RES",0),
    ("B36","Diamond Plaza Mall",        160, -18, 22, 14, 4, "commercial_plaza", 11, 5, "flat","COM",0),

    # ═══ BLOCK D1 (W market): x -185..-107, z 7..30 ═══
    ("B37","Rajasthan Emporium",       -155,  15, 24, 16, 3, "commercial_plaza",  2, 1, "flat","COM",0),
    ("B38","Revenue Court Complex",    -130,  22, 22, 14, 2, "civic_landmark",   13, 4, "dome","GOV",0),

    # ═══ BLOCK D2 (center-left market): x -88..-7, z 7..30 ═══
    ("B39","Mercato Coperto",           -60,  15, 26, 16, 2, "commercial_plaza", 10, 5, "flat","COM",0),
    ("B40","Jewellers Row",             -30,  20, 18, 12, 3, "commercial_plaza", 12, 1, "flat","COM",0),

    # ═══ BLOCK D3 (center-right market): x 7..88, z 7..30 ═══
    ("B41","Bazaar Street Shops",        30,  15, 22, 12, 2, "commercial_plaza", 10, 4, "flat","COM",0),
    ("B42","Sports Club",                65,  20, 20, 16, 2, "civic_landmark",   21, 4, "flat","COM",0),

    # ═══ BLOCK D4 (E market): x 107..185, z 7..30 ═══
    ("B43","Sky Loft Apartments",       130,  15, 14, 12,14, "art_deco_tower",    9, 7, "stepped","RES",0),
    ("B44","Nova Business Suites",      160,  22, 18, 12, 6, "commercial_plaza", 15, 5, "flat","COM",0),

    # ═══ BLOCK E1 (W mid): x -185..-107, z 40..59 ═══
    ("B45","Spice Market Block",       -155,  48, 20, 14, 2, "commercial_plaza", 31, 6, "flat","COM",0),
    ("B46","Public School Campus",     -130,  52, 24, 14, 2, "civic_landmark",    1, 0, "flat","GOV",0),

    # ═══ BLOCK E2 (center-left mid): x -88..-7, z 40..59 ═══
    ("B47","City Centre Mall",          -55,  48, 28, 14, 4, "commercial_plaza", 11, 5, "flat","COM",0),
    ("B48","Textile Traders Hub",       -25,  50, 22, 12, 3, "commercial_plaza",  4, 2, "flat","COM",0),

    # ═══ BLOCK E3 (center-right mid): x 7..88, z 40..59 ═══
    ("B49","Torre Vetro Centrale",       25,  48, 14, 14,18, "modern_glass_tower", 0, 8, "flat","COM",0),
    ("B50","Hotel Royal Palace",         60,  50, 16, 14, 8, "art_deco_tower",   13, 3, "stepped","COM",0),

    # ═══ BLOCK E4 (E mid): x 107..185, z 40..59 ═══
    ("B51","Zenith Corporate Center",   130,  48, 14, 12,18, "modern_glass_tower", 0, 8, "flat","COM",0),
    ("B52","Golden Square Mall",        160,  50, 22, 14, 3, "commercial_plaza",  4, 5, "flat","COM",0),

    # ═══ BLOCK F1 (SW): x -185..-107, z 71..134 ═══
    ("B53","Aravalli Villa 1",         -170,  80, 14, 12, 2, "villa_bungalow",   18, 6, "pitched","RES",0),
    ("B54","Aravalli Villa 2",         -150,  95, 12, 10, 1, "villa_bungalow",   19, 7, "pitched","RES",0),
    ("B55","Aravalli Villa 3",         -170, 110, 14, 12, 2, "villa_bungalow",   23, 6, "pitched","RES",0),
    ("B56","Aravalli Villa 4",         -140, 120, 14, 12, 2, "villa_bungalow",   24, 7, "pitched","RES",0),
    ("B57","Hilltop Bungalow A",       -120,  85, 14, 12, 1, "villa_bungalow",   26, 6, "pitched","RES",0),
    ("B58","Hilltop Bungalow B",       -115, 115, 14, 12, 2, "villa_bungalow",   27, 7, "pitched","RES",0),

    # ═══ BLOCK F2 (S center-left): x -88..-7, z 71..134 ═══
    ("B59","Tulsi Apartments",          -65,  80, 18, 14, 5, "residential_block", 7, 1, "pitched","RES",0),
    ("B60","Marigold Heights",          -35,  85, 16, 12, 6, "residential_block",22, 2, "pitched","RES",0),
    ("B61","Neem Garden Homes",         -55, 105, 16, 14, 4, "low_rise_walk_up", 24, 4, "terrace","RES",0),
    ("B62","Orchid Towers",             -30, 120, 14, 14,12, "art_deco_tower",   28, 7, "stepped","RES",0),

    # ═══ BLOCK F3 (S center-right): x 7..88, z 71..134 ═══
    ("B63","Banyan Court",               30,  82, 20, 16, 5, "heritage_palazzo", 25, 1, "dome","RES",0),
    ("B64","Gulmohar Residency",         65,  80, 16, 14, 7, "residential_block",26, 3, "pitched","RES",0),
    ("B65","Palm View Flats",            35, 105, 14, 12, 5, "low_rise_walk_up", 27, 2, "terrace","RES",0),
    ("B66","Cedar Heights",              65, 120, 16, 14, 8, "residential_block",29, 0, "pitched","RES",0),

    # ═══ BLOCK F4 (SE): x 107..185, z 71..134 ═══
    ("B67","Fortuna Towers",            130,  82, 14, 14,16, "modern_glass_tower", 0, 9, "flat","RES",0),
    ("B68","Eastern Block Apts",        160,  85, 18, 14, 6, "residential_block", 22, 2, "pitched","RES",0),
    ("B69","Amber Heights",             130, 110, 14, 12, 8, "art_deco_tower",    8, 3, "stepped","RES",0),
    ("B70","Royal Garden Flats",        160, 115, 16, 14, 5, "low_rise_walk_up", 29, 2, "terrace","RES",0),

    # ═══ BLOCK G1 (far SW): x -185..-107, z 146..185 ═══
    ("B71","Jasmine Villa",            -160, 160, 14, 12, 2, "villa_bungalow",  23, 6, "pitched","RES",0),
    ("B72","Sunrise Apartments A",     -135, 165, 20, 14, 6, "residential_block", 1, 0, "pitched","RES",0),

    # ═══ BLOCK G2 (far S center-left): x -88..-7, z 146..185 ═══
    ("B73","Sunrise Apartments B",      -55, 160, 20, 14, 5, "residential_block", 3, 1, "pitched","RES",0),
    ("B74","Green Valley Homes",        -30, 165, 16, 14, 4, "low_rise_walk_up",  5, 2, "terrace","RES",0),

    # ═══ BLOCK G3 (far S center-right): x 7..88, z 146..185 ═══
    ("B75","Sunset Residences",          30, 160, 16, 14, 6, "residential_block",28, 3, "pitched","RES",0),
    ("B76","Lotus Enclave",              65, 165, 16, 14, 4, "low_rise_walk_up", 30, 5, "terrace","RES",0),

    # ═══ BLOCK G4 (far SE): x 107..185, z 146..185 ═══
    ("B77","East End Villas",           130, 160, 14, 12, 2, "villa_bungalow",   30, 6, "pitched","RES",0),
    ("B78","Auto Market Complex",       160, 165, 24, 14, 2, "commercial_plaza", 15, 5, "flat","COM",0),

    # ═══ SPECIAL: Central Avenue Landmarks (within blocks, away from roads) ═══
    ("B79","Telecom Tower",             155, -82, 10, 10,25, "modern_glass_tower", 0,11, "flat","COM",0),
    ("B80","Central Railway Station",   -80, -82, 20, 16, 3, "civic_landmark",   10, 5, "flat","GOV",0),
]

# ─── Street Definitions (for 3D rendering) ───────────────────────────
CITY_STREETS = [
    # Main horizontal roads (x1, z, x2, width)
    {"x1": -190, "z": -100, "x2": 190, "w": 12, "name": "National Highway"},
    {"x1": -190, "z":   0,  "x2": 190, "w": 10, "name": "Main Bazaar Road"},
    {"x1": -190, "z":  65,  "x2": 190, "w": 8,  "name": "Market Street"},
    {"x1": -190, "z": 140,  "x2": 190, "w": 8,  "name": "Southern Ring Road"},
    {"x1": -190, "z": -150, "x2": 190, "w": 8,  "name": "Northern Ring Road"},
    # Main vertical roads
    {"x1": -100, "z": -180, "x2": -100, "w": 10, "name": "Station Road", "vertical": True, "z2": 160},
    {"x1":    0, "z": -180, "x2":    0, "w": 10, "name": "Central Avenue", "vertical": True, "z2": 160},
    {"x1":  100, "z": -180, "x2":  100, "w": 10, "name": "East Boulevard", "vertical": True, "z2": 160},
    # Secondary streets
    {"x1": -160, "z": -60, "x2": 60, "w": 6, "name": "Heritage Lane"},
    {"x1":  60,  "z": -60, "x2": 180, "w": 6, "name": "Commerce Way"},
    {"x1": -180, "z":  35, "x2": 180, "w": 6, "name": "Garden Path"},
]

# ─── Piazza / Open Spaces ────────────────────────────────────────────
CITY_PIAZZAS = [
    {"x": -10, "z": -15, "r": 25, "name": "Piazza Centrale"},
    {"x":  40, "z":  50, "r": 18, "name": "Market Square"},
    {"x":-130, "z": -20, "r": 20, "name": "Collectorate Maidan"},
    {"x":  115,"z": -80, "r": 15, "name": "Business Park Garden"},
]


def _rand_owner():
    return f"{random.choice(OWNER_FIRST)} {random.choice(OWNER_LAST)}"


def _make_ulpin(bld_id, floor, unit_id, stype):
    fc = f"F{floor:02d}" if floor >= 0 else f"FB{abs(floor)}"
    return f"{STATE}-{DISTRICT}-{TEHSIL}-{VILLAGE}-{bld_id}-{fc}-{unit_id}-{stype}"


def _get_bhk(arch_type, floor, upf, is_top):
    if is_top and arch_type in ("art_deco_tower", "modern_glass_tower"):
        return "4BHK"
    if arch_type in ("villa_bungalow",):
        return "3BHK"
    if arch_type in ("commercial_plaza",):
        return "shop" if floor == 0 else "office"
    if arch_type in ("civic_landmark", "heritage_palazzo") and not arch_type == "heritage_palazzo":
        return "govt_hall"
    r = random.random()
    if upf >= 4:
        return "1BHK" if r < 0.3 else ("2BHK" if r < 0.7 else "3BHK")
    elif upf >= 3:
        return "2BHK" if r < 0.5 else "3BHK"
    else:
        return "3BHK" if r < 0.6 else "4BHK"


def _circle_rate(zone, floor):
    base = {"RES": 65000, "COM": 110000, "GOV": 45000}.get(zone, 60000)
    return int(base * (1 + floor * 0.02))


def generate_city_map_dataset():
    """Generate complete 3D city dataset with 80 architecturally distinct buildings."""
    random.seed(42)
    np.random.seed(42)

    buildings_meta = []
    all_units = []
    conflict_count = 0

    for (bid, name, cx, cz, bw, bd, nfloors, arch_type, fci, aci, roof, zone, rot) in _B:
        atype = ARCH_TYPES[arch_type]
        actual_floors = nfloors
        upf_min, upf_max = atype["upf"]
        units_per_floor = random.randint(upf_min, upf_max)

        facade_color = FACADE_COLORS[fci % len(FACADE_COLORS)]
        accent_color = ACCENT_COLORS[aci % len(ACCENT_COLORS)]
        if arch_type == "modern_glass_tower":
            facade_color = GLASS_COLORS[fci % len(GLASS_COLORS)]

        floor_list = list(range(0, actual_floors + 1))
        has_basement = actual_floors >= 6
        if has_basement:
            floor_list = [-1] + floor_list

        buildings_meta.append({
            "building_id": bid,
            "name": name,
            "type": atype["label"],
            "arch_type": arch_type,
            "floors": floor_list,
            "center_pos": [cx, 0, cz],
            "dimensions": [bw, bd],
            "facade_color": facade_color,
            "accent_color": accent_color,
            "roof_type": roof,
            "shape": atype["shape"],
            "rotation": rot,
            "zone": zone,
            "units_per_floor": units_per_floor,
        })

        # ── Basement Parking ──
        if has_basement:
            for pidx in range(1, 3):
                pid = f"PRK-{bid}-B{pidx:02d}"
                all_units.append({
                    "building_id": bid, "building_name": name, "floor_no": -1,
                    "unit_id": pid, "flat_label": f"Parking Bay B-{pidx:02d}",
                    "space_type": "PRK", "owner": f"Allotted to {_rand_owner()}",
                    "area_sqm": 25.0, "height_m": FLOOR_HEIGHT,
                    "valuation_inr": 750000,
                    "z_min": -FLOOR_HEIGHT, "z_max": 0.0,
                    "plan_x1": 0.5 if pidx==1 else 5.2, "plan_x2": 4.8 if pidx==1 else 9.5,
                    "plan_y1": 0.5, "plan_y2": 4.8,
                    "ulpin": _make_ulpin(bid, -1, pid, "PRK"),
                    "conflict": False, "conflict_details": None,
                    "rooms": [], "bhk_type": "parking",
                })

        # ── Ground Floor ──
        if zone == "COM" or arch_type == "commercial_plaza":
            ns = min(units_per_floor, 4)
            sw = 9.0 / ns
            for si in range(1, ns+1):
                sid = f"SHOP-{bid}-G{si:02d}"
                sname = random.choice(SHOP_NAMES)
                area = round(random.uniform(25, 60), 1)
                rooms = [dict(r) for r in ROOM_TEMPLATES["shop"]]
                all_units.append({
                    "building_id": bid, "building_name": name, "floor_no": 0,
                    "unit_id": sid, "flat_label": sname,
                    "space_type": "COM", "owner": sname,
                    "area_sqm": area, "height_m": FLOOR_HEIGHT,
                    "valuation_inr": int(area * 110000),
                    "z_min": 0.0, "z_max": FLOOR_HEIGHT,
                    "plan_x1": round(0.5+(si-1)*sw,1), "plan_x2": round(0.5+si*sw,1),
                    "plan_y1": 0.5, "plan_y2": 9.5,
                    "ulpin": _make_ulpin(bid, 0, sid, "COM"),
                    "conflict": False, "conflict_details": None,
                    "rooms": rooms, "bhk_type": "shop",
                })
        elif zone == "GOV":
            gid = f"GOV-{bid}-G01"
            gname = random.choice(GOVT_NAMES)
            area = round(random.uniform(80, 250), 1)
            rooms = [dict(r) for r in ROOM_TEMPLATES["govt_hall"]]
            all_units.append({
                "building_id": bid, "building_name": name, "floor_no": 0,
                "unit_id": gid, "flat_label": gname,
                "space_type": "GOV", "owner": f"Govt of {STATE}",
                "area_sqm": area, "height_m": FLOOR_HEIGHT,
                "valuation_inr": int(area * 45000),
                "z_min": 0.0, "z_max": FLOOR_HEIGHT,
                "plan_x1": 0.5, "plan_x2": 9.5, "plan_y1": 0.5, "plan_y2": 9.5,
                "ulpin": _make_ulpin(bid, 0, gid, "GOV"),
                "conflict": False, "conflict_details": None,
                "rooms": rooms, "bhk_type": "govt_hall",
            })
        else:
            lid = f"LOBBY-{bid}"
            all_units.append({
                "building_id": bid, "building_name": name, "floor_no": 0,
                "unit_id": lid, "flat_label": f"Entrance Lobby — {name}",
                "space_type": "UTL", "owner": f"RWA {name}",
                "area_sqm": round(random.uniform(30, 80), 1), "height_m": FLOOR_HEIGHT,
                "valuation_inr": 0,
                "z_min": 0.0, "z_max": FLOOR_HEIGHT,
                "plan_x1": 0.5, "plan_x2": 9.5, "plan_y1": 0.5, "plan_y2": 9.5,
                "ulpin": _make_ulpin(bid, 0, lid, "UTL"),
                "conflict": False, "conflict_details": None,
                "rooms": [], "bhk_type": "lobby",
            })

        # ── Upper Floors ──
        for fl in range(1, actual_floors + 1):
            zmin = fl * FLOOR_HEIGHT
            zmax = zmin + FLOOR_HEIGHT
            is_top = (fl == actual_floors)

            n_units = 1 if is_top and arch_type in ("art_deco_tower","modern_glass_tower") else units_per_floor
            if zone == "GOV":
                n_units = max(1, n_units // 2)

            uw = 9.0 / n_units

            has_conflict = (zone=="RES" and fl==2 and n_units>=2 and random.random()<0.06)
            if has_conflict:
                conflict_count += 1

            for ui in range(1, n_units + 1):
                uid = f"{bid}-{fl}{ui:02d}"
                bhk = _get_bhk(arch_type, fl, n_units, is_top)
                rooms = [dict(r) for r in ROOM_TEMPLATES.get(bhk, ROOM_TEMPLATES["2BHK"])]

                if bhk in ("shop","office"):
                    stype = "COM"
                    label = f"Office Suite {fl}{ui:02d} — {name}"
                    area = round(random.uniform(40, 100), 1)
                elif zone == "GOV":
                    stype = "GOV"
                    label = f"Govt Office {fl}{ui:02d} — {name}"
                    area = round(random.uniform(60, 150), 1)
                else:
                    stype = "RES"
                    label = f"Flat {fl}{ui:02d} ({bhk}) — {name}"
                    if is_top and n_units == 1:
                        label = f"Penthouse ({bhk}) — {name}"
                    area = round(random.uniform(45, 160), 1)

                x1 = round(0.5 + (ui-1)*uw, 1)
                x2 = round(0.5 + ui*uw, 1)
                if has_conflict and ui == 1: x2 = round(x2 + 0.5, 1)
                if has_conflict and ui == 2: x1 = round(x1 - 0.3, 1)

                all_units.append({
                    "building_id": bid, "building_name": name, "floor_no": fl,
                    "unit_id": uid, "flat_label": label,
                    "space_type": stype, "owner": _rand_owner() if stype=="RES" else (random.choice(SHOP_NAMES) if stype=="COM" else f"Govt of {STATE}"),
                    "area_sqm": area, "height_m": FLOOR_HEIGHT,
                    "valuation_inr": int(area * _circle_rate(zone, fl)),
                    "z_min": round(zmin, 2), "z_max": round(zmax, 2),
                    "plan_x1": x1, "plan_x2": x2, "plan_y1": 0.5, "plan_y2": 9.5,
                    "ulpin": _make_ulpin(bid, fl, uid, stype),
                    "conflict": has_conflict, "conflict_details": f"Boundary overlap on Floor {fl}" if has_conflict else None,
                    "rooms": rooms, "bhk_type": bhk,
                })

    # ── Point Cloud ──
    pts = []
    for b in buildings_meta:
        for fl in b["floors"]:
            if fl < 0: continue
            cz_pt = (fl+1)*FLOOR_HEIGHT - FLOOR_HEIGHT/2
            for _ in range(20):
                px = b["center_pos"][0] + np.random.uniform(-b["dimensions"][0]/2, b["dimensions"][0]/2)
                pz = b["center_pos"][2] + np.random.uniform(-b["dimensions"][1]/2, b["dimensions"][1]/2)
                pts.append({"x": round(float(px),2), "y": round(float(pz),2), "z": round(float(np.random.normal(cz_pt,0.3)),2)})
    for _ in range(800):
        pts.append({"x": round(float(np.random.uniform(-200,200)),2), "y": round(float(np.random.uniform(-200,200)),2), "z": round(float(np.random.normal(0,0.1)),2)})
    random.shuffle(pts)

    return {
        "id": "RJ_JPR_CITY01",
        "name": CITY,
        "city": "Jaipur",
        "state": STATE,
        "district": DISTRICT,
        "village": VILLAGE,
        "surface_parcel": "CITY_MAP_2026",
        "gov_authority": GOV_AUTH,
        "buildings": buildings_meta,
        "units": all_units,
        "point_cloud": pts[:3000],
        "total_ulpins": len(all_units),
        "total_conflicts": conflict_count,
        "detected_floor_count": max(max(b["floors"]) for b in buildings_meta) + 2,
        "streets": CITY_STREETS,
        "piazzas": CITY_PIAZZAS,
    }


if __name__ == "__main__":
    d = generate_city_map_dataset()
    print(f"Buildings: {len(d['buildings'])}")
    print(f"ULPINs: {d['total_ulpins']}")
    print(f"Conflicts: {d['total_conflicts']}")
    for u in d["units"][:5]:
        print(f"  {u['ulpin']}  rooms={len(u.get('rooms',[]))}")
