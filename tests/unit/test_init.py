"""
..
   test_init.py

Unit tests for pyra.__init__.py.
"""


def test_initialize(test_pyra_init):
    """Tests initializing retroarcher"""
    assert test_pyra_init


def test_stop():
    # todo - how to test this as it has a sys.exit() event and won't actually return...
    pass
