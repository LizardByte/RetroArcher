"""
..
   test_threads.py

Unit tests for common.threads.
"""
# local imports
from common import threads


def test_run_in_thread():
    """Tests that run_in_thread is a class of type.

    This can probably be improved somehow.
    """
    test_thread = threads.run_in_thread
    assert isinstance(test_thread, type)
