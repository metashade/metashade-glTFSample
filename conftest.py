"""Pytest configuration for metashade-glTF sample."""
import sys
from pathlib import Path

# Add metashade to Python path for tests
repo_root = Path(__file__).parent
metashade_path = repo_root / "metashade"

if str(metashade_path) not in sys.path:
    sys.path.insert(0, str(metashade_path))