"""
3D ULPIN Prototype Runner
=========================
Entry point to execute the backend data processing, AI floor detection,
topology validation, and 3D web dashboard compilation.
"""

import sys
import os

# Add backend directory to module search path
backend_path = os.path.join(os.path.dirname(__file__), "backend")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from pipeline import run_pipeline

if __name__ == "__main__":
    run_pipeline()
