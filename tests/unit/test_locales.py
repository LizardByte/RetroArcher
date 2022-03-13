"""test_locales.py

unit tests for pyra.locales.py
"""
# local imports
from pyra import locales


def test_get_all_locales():
    """Tests if locales returns a dictionary and if it contains certain keys"""
    test_locales = locales.get_all_locales()
    assert test_locales
    assert isinstance(test_locales, dict)
    assert test_locales['en']
    assert test_locales['en_US']
