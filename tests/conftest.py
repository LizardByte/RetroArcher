"""conftest.py

fixtures for pytest
"""
# standard imports
import os

# lib imports
import pytest

# local imports
from pyra import definitions
from pyra import webapp


@pytest.fixture(scope='module')
def test_client():

    app = webapp.app
    app.testing = True
    client = app.test_client()

    # Create a test client using the Flask application configured for testing
    with client as test_client:
        # Establish an application context
        with app.app_context():
            yield test_client  # this is where the testing happens!


@pytest.fixture(scope='module')
def test_config_file():
    test_config_file = os.path.join(definitions.Paths().DATA_DIR, definitions.Files().CONFIG)

    yield test_config_file
