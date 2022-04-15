"""
..
   test_logger.py

Unit tests for pyra.logger.py.
"""
# standard imports
import logging

# local imports
from pyra import logger


def test_blacklist_config():
    # todo
    pass


def test_filers():
    # todo
    pass


def test_listener():
    # todo
    pass


def test_init_multiprocessing():
    # todo
    pass


def test_get_logger():
    """Test that logger object can be created"""
    log = logger.get_logger(name='pyra')
    assert isinstance(log, logging.Logger)


def test_setup_loggers():
    # todo
    pass


def test_init_logger():
    """Test that logger can be initialized"""
    log = logger.init_logger(log_name='pyra')
    assert isinstance(log, logging.Logger)


def test_init_hooks():
    # todo
    pass


def test_shutdown():
    """Shuts down logging, tests not setup yet"""
    logger.shutdown()

    # todo
