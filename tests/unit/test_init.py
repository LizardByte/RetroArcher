"""test_init.py

unit tests for pyra.__init__.py
"""
# local imports
import pyra


def test_initialize(test_config_file):
    """Tests initializing retroarcher"""
    initialized = pyra.initialize(config_file=test_config_file)
    assert initialized
