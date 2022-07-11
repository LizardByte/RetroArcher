"""
..
   version.py

Module containing constants related to version numbers.

Constants
---------
version : str
    Semantic version of RetroArcher. i.e. `0.1.0`

Examples
--------
>>> version
0.1.0
"""

_version_major = 0
_version_minor = 1
_version_patch = 0

version = f'{_version_major}.{_version_minor}.{_version_patch}'
