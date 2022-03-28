"""test_threads.py

unit tests for pyra.threads
"""
# local imports
from pyra import threads


def test_run_in_thread():
    """Tests that run_in_thread is a class of type.

    This can probably be improved somehow.
    """
    test_thread = threads.run_in_thread
    assert isinstance(test_thread, type)
