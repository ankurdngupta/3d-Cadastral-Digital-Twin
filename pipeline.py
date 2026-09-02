"""
3D ULPIN Prototype Launcher
Redirects execution to the modular backend pipeline.
"""

import sys
import os

backend_dir = os.path.join(os.path.dirname(__file__), "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from pipeline import run_pipeline

if __name__ == "__main__":
    run_pipeline()
