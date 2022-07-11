"""
..
   test_locales.py

Unit tests for pyra.locales.py.
"""
# standard imports
import inspect

# local imports
from pyra import locales


def test_get_all_locales():
    """Tests if locales returns a dictionary and if it contains certain keys"""
    test_locales = locales.get_all_locales()
    assert test_locales
    assert isinstance(test_locales, dict)
    assert test_locales['en']
    assert test_locales['en_US']


def test_get_locale():
    locale = locales.get_locale()
    assert locale == 'en'


def test_get_text():
    get_text = locales.get_text()
    assert get_text

    assert inspect.ismethod(get_text)  # ensure get_text is a method
