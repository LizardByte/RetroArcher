"""conftest.py

fixtures for pytest
"""
# standard imports
import os
import sys

# lib imports
import pytest

# local imports
from pyra import config
from pyra import definitions
from pyra import tray_icon
from pyra import webapp


@pytest.fixture(scope='module')
def test_client():
    """Create a test client for testing webapp endpoints"""
    app = webapp.app
    app.testing = True

    # disable flask warning banner - https://stackoverflow.com/a/57989189/11214013
    cli = sys.modules['flask.cli']
    cli.show_server_banner = lambda *x: None

    client = app.test_client()

    # Create a test client using the Flask application configured for testing
    with client as test_client:
        # Establish an application context
        with app.app_context():
            yield test_client  # this is where the testing happens!


@pytest.fixture(scope='module')
def test_config_file():
    """Set a test config file path"""
    test_config_file = os.path.join(definitions.Paths().DATA_DIR, definitions.Files().CONFIG)

    yield test_config_file


@pytest.fixture(scope='module')
def test_config_object(test_config_file):
    """Create a test config object"""
    test_config_object = config.create_config(config_file=test_config_file)

    yield test_config_object


@pytest.fixture(scope='module')
def test_tray_icon():
    """Initialize and run a test tray icon"""
    test_tray_icon = tray_icon.tray_initialize()

    tray_icon.tray_run()

    yield test_tray_icon

    # teardown
    test_tray_icon.stop()
