"""
Utility functions for the backend application.
"""

import os
from pathlib import Path

# The absolute path to the root of the 'api' package.
# We use Path(__file__).parent.resolve() to get the directory of the current file (utils.py)
# and then .parent to go up one level to the 'api' package root.
API_ROOT = Path(__file__).parent.resolve()


def get_project_root_path(*path_segments: str) -> Path:
    """
    Constructs an absolute path from the api package root.
    """
    return API_ROOT.joinpath(*path_segments)
