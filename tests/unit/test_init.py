"""
..
   test_init.py

Unit tests for pyra.__init__.py.
"""
import pytest


def test_initialize(test_pyra_init):
    """Tests initializing retroarcher"""
    print(test_pyra_init)
    assert test_pyra_init


@pytest.mark.skip(reason="impossible to test as it has a sys.exit() event and won't actually return")
def test_stop():
    pass
