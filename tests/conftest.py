"""
..
   conftest.py

Fixtures for pytest.
"""
# standard imports
import os

# lib imports
import pytest

# local imports
import pyra
from pyra import config
from pyra import definitions
from pyra import webapp


@pytest.fixture(scope='function')
def test_config_file():
    """Set a test config file path"""
    test_config_file = os.path.join(definitions.Paths.DATA_DIR, 'test_config.ini')  # use a dummy ini file

    yield test_config_file


@pytest.fixture(scope='function')
def test_config_object(test_config_file):
    """Create a test config object"""
    test_config_object = config.create_config(config_file=test_config_file)

    config.CONFIG = test_config_object

    yield test_config_object


@pytest.fixture(scope='function')
def test_pyra_init(test_config_file):
    test_pyra_init = pyra.initialize(config_file=test_config_file)

    yield test_pyra_init

    pyra._INITIALIZED = False
    pyra.SIGNAL = 'shutdown'


@pytest.fixture(scope='function')
def test_client(test_pyra_init):
    """Create a test client for testing webapp endpoints"""
    app = webapp.app
    app.testing = True

    client = app.test_client()

    # Create a test client using the Flask application configured for testing
    with client as test_client:
        # Establish an application context
        with app.app_context():
            yield test_client  # this is where the testing happens!
