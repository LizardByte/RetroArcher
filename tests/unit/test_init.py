"""test_init.py

unit tests for pyra.__init__.py
"""
# local imports
import pyra


def test_initialize(test_config_file):
    """Tests initializing retroarcher"""
    initialized = pyra.initialize(config_file=test_config_file)
    assert initialized


def test_stop():
    # todo - how to test this as it has a sys.exit() event and won't actually return...
    pass
