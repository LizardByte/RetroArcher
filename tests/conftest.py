"""
tests/conftest.py

Fixtures for pytest.
"""
# standard imports
import os
import sys

# lib imports
import pytest

pytest.root_dir = root_dir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
pytest.src_dir = src_dir = os.path.join(root_dir, 'src')

if os.path.isdir(src_dir):  # avoid flake8 E402 warning
    sys.path.insert(0, src_dir)

    # local imports
    import common
    from common import config
    from common import definitions
    from common import webapp


@pytest.fixture(scope='function')
def test_config_file():
    """Set a test config file path"""
    test_config_file = os.path.join(definitions.Paths.CONFIG_DIR, 'test_config.ini')  # use a dummy ini file

    yield test_config_file


@pytest.fixture(scope='function')
def test_config_object(test_config_file):
    """Create a test config object"""
    test_config_object = config.create_config(config_file=test_config_file)

    config.CONFIG = test_config_object

    yield test_config_object


@pytest.fixture(scope='function')
def test_common_init(test_config_file):
    test_common_init = common.initialize(config_file=test_config_file)

    yield test_common_init

    common._INITIALIZED = False
    common.SIGNAL = 'shutdown'


@pytest.fixture(scope='function')
def test_client(test_common_init):
    """Create a test client for testing webapp endpoints"""
    app = webapp.app
    app.testing = True

    client = app.test_client()

    # Create a test client using the Flask application configured for testing
    with client as test_client:
        # Establish an application context
        with app.app_context():
            yield test_client  # this is where the testing happens!
