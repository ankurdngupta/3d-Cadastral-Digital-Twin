"""
Database Management Module
==========================
Manages persistence for multi-city 3D Land Parcels and ULPIN records into SQLite
and provides PostGIS / PostgreSQL 3D geometry schema definitions.
"""

import os
import sqlite3


def save_to_sqlite(layout: list, db_path: str = "ulpin_3d.db"):
    """
    Stores 3D ULPIN parcels and cadastral ownership records into SQLite database.
    """
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except Exception:
            pass

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS ulpin_3d (
            ulpin_id TEXT PRIMARY KEY,
            building_id TEXT,
            building_name TEXT,
            unit_id TEXT,
            flat_label TEXT,
            owner TEXT,
            floor_no INTEGER,
            space_type TEXT,
            area_sqm REAL,
            height_m REAL,
            valuation_inr INTEGER,
            z_min REAL,
            z_max REAL,
            plan_x1 REAL,
            plan_x2 REAL,
            plan_y1 REAL,
            plan_y2 REAL,
            conflict INTEGER,
            conflict_details TEXT
        )
    """)

    for unit in layout:
        cur.execute("""
            INSERT OR REPLACE INTO ulpin_3d VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            unit.get("ulpin", "UNKNOWN"),
            unit.get("building_id", "T01"),
            unit.get("building_name", "Tower A"),
            unit.get("unit_id", "U001"),
            unit.get("flat_label", unit.get("unit_id", "U001")),
            unit.get("owner", "Unknown"),
            unit.get("floor_no", 0),
            unit.get("space_type", "RES"),
            unit.get("area_sqm", 110.0),
            unit.get("height_m", 3.0),
            unit.get("valuation_inr", 9500000),
            unit.get("z_min", 0.0),
            unit.get("z_max", 3.0),
            unit.get("plan_x1", 0.5),
            unit.get("plan_x2", 4.8),
            unit.get("plan_y1", 0.5),
            unit.get("plan_y2", 9.5),
            int(unit.get("conflict", False)),
            unit.get("conflict_details", "")
        ))

    conn.commit()
    conn.close()


def get_postgis_ddl() -> str:
    """
    Returns production-grade PostgreSQL / PostGIS 3D Cadastre DDL schema.
    """
    return """
-- PostgreSQL / PostGIS 3D Cadastral Schema for Multi-Building Society
CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS cadastre_3d_parcels (
    ulpin_id VARCHAR(64) PRIMARY KEY,
    building_id VARCHAR(16) NOT NULL,
    building_name VARCHAR(128) NOT NULL,
    unit_id VARCHAR(16) NOT NULL,
    flat_label VARCHAR(64),
    owner_name VARCHAR(128) NOT NULL,
    floor_number INT NOT NULL,
    space_type VARCHAR(16) NOT NULL,
    area_sqm NUMERIC(8,2) NOT NULL,
    height_m NUMERIC(5,2) NOT NULL,
    valuation_inr BIGINT NOT NULL,
    geom_3d GEOMETRY(POLYHEDRALSURFACEZ, 4326),
    has_conflict BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_cadastre_geom_3d ON cadastre_3d_parcels USING GIST (geom_3d);
"""
