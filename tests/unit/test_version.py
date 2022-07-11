"""
..
   test_version.py

Unit tests for pyra.version.
"""
# local imports
from pyra import version


def test_run_in_thread():
    """Tests that a proper version number is returned."""
    test_version_major = version._version_major
    test_version_minor = version._version_minor
    test_version_patch = version._version_patch

    assert isinstance(test_version_major, int)
    assert isinstance(test_version_minor, int)
    assert isinstance(test_version_patch, int)

    test_version = version.version
    assert test_version == f'{test_version_major}.{test_version_minor}.{test_version_patch}'
