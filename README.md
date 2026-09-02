# 3D ULPIN & Vertical Cadastral Mapping System
### SIH 2026 (Problem Statement 26011)

This repository contains a modular prototype for **3D ULPIN (Unique Land Parcel Identification Number) Generation, AI Floor Detection, 3D Topology Validation, and Vertical Property Mapping**.

---

## 📁 Project Architecture & Folder Structure

The project is modularized into backend processing scripts and frontend dashboard assets:

```
3D_ULPIN_Prototype/
│
├── backend/                       # Python Data Processing & AI Modules
│   ├── __init__.py                # Package initialization
│   ├── data_generator.py          # Synthetic LiDAR/Drone point clouds & 3D parcel layout
│   ├── floor_detector.py          # AI height-clustering floor boundary detection
│   ├── ulpin_generator.py         # Standardized 3D ULPIN generator
│   ├── topology.py                # Shapely polygon intersection & encroachment validation
│   ├── db_manager.py              # SQLite storage & PostgreSQL/PostGIS 3D schema
│   └── pipeline.py                # Main pipeline orchestrator & compiler
│
├── frontend/                      # Web Dashboard Source Code
│   ├── css/
│   │   └── style.css              # Glassmorphic UI styles & visual tokens
│   ├── js/
│   │   ├── app.js                 # Three.js realistic building, GIS environment & interactions
│   │   └── three.min.js           # Three.js 3D library
│   └── index.html                 # HTML dashboard template
│
├── pipeline_runner.py             # Root launcher script to run the pipeline
├── requirements.txt               # Dependencies (numpy, shapely)
├── building_data.json             # Exported JSON dataset
├── ulpin_3d.db                    # Generated SQLite Cadastral database
├── dashboard.html                 # Compiled standalone 3D Web Dashboard (Double-click to open!)
└── README.md                      # Documentation & instructions
```

---

## 🚀 How to Run

### 1. Install Dependencies
Ensure Python 3 is installed, then install the required libraries:
```bash
pip install -r requirements.txt
```

### 2. Execute the Pipeline
Run the root pipeline runner:
```bash
py pipeline_runner.py
```
*(or `python pipeline_runner.py`)*

This runs the 7-step pipeline:
1. Generates 3D Drone/LiDAR point clouds.
2. Runs AI Height-Clustering floor detection.
3. Maps multi-story parcels (Residential, Commercial, Utility).
4. Generates unique 3D ULPIN strings for each unit.
5. Runs automated 3D topology & encroachment validation.
6. Stores records in `ulpin_3d.db`.
7. Compiles the standalone `dashboard.html`.

### 3. Open the 3D Dashboard
Simply double-click `dashboard.html` to open it in your browser (no web server needed).

---

## ✨ Features & Visual Upgrades

1. **Realistic 3D Building**:
   - Reinforced concrete floor slabs with structural parapets.
   - Blue reflective glass windows with metallic frame borders.
   - Balconies with glass railings for residential units.
   - Rooftop elevator cabin, HVAC units, and commercial storefronts on Floor 0.
   - Transparent ground plane showing underground utility infrastructure (Basement).

2. **Rich Surrounding GIS Environment**:
   - Asphalt main road with white dashed center-line markings.
   - Sidewalks, streetlights, parked cars, and procedural 3D trees.
   - Surrounding contextual GIS buildings in elegant architectural style.

3. **2D Interactive Building Stack**:
   - A vertical floor stack on the left side of the dashboard displaying floors from top to bottom (Floor 3: Flat F7/F8, Floor 2: Flat F5/F6, Floor 1: Flat F1/F2, Ground: Shop C1/C2, Basement: Utility U1).
   - Selecting a unit highlights both the 2D button and the 3D unit mesh.

4. **Detailed Parcel Ownership Card**:
   - Clicking on any flat (e.g. **Flat F7**) displays:
     - **3D ULPIN**: `RJ-KRL-VLG023-P00456-B01-F03-F7-RES`
     - **Owner**: `ABC`
     - **Floor**: `3`
     - **Area**: `80 m²`
     - **Height**: `3.0 m`
     - **Status**: `✔ Valid Parcel`
   - Clicking on **Flat F5** or **Flat F6** highlights the overlap with an alert: `⚠ Encroachment Conflict (Overlaps with Flat F6 by 5.4 sq m)`.

5. **Explode View & Day/Night Mode**:
   - **Explode Floors Slider**: Smoothly separates floors vertically to inspect internal layouts.
   - **Day/Night Toggle**: Switches lighting and sky atmosphere.
