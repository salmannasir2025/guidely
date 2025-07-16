"""
Tests for the utility functions.
"""

from api.utils import get_project_root_path


def test_get_project_root_path():
    """
    Ensures that get_project_root_path correctly resolves a known file (requirements.txt).
    """
    # We test by resolving the path to a file we know exists: requirements.txt
    requirements_path = get_project_root_path("requirements.txt")
    assert requirements_path.exists(), "The path to requirements.txt should exist."
    assert requirements_path.is_file(), "The resolved path should point to a file."