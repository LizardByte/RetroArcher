"""
..
   test_webapp.py

Unit tests for common.webapp.
"""
# standard imports
import sys

# local imports
from common import threads
from common import webapp


def test_start_webapp():
    """Test start_webapp function"""
    app = webapp.app
    app.testing = True

    # disable flask warning banner - https://stackoverflow.com/a/57989189/11214013
    cli = sys.modules['flask.cli']
    cli.show_server_banner = lambda *x: None

    client = app.test_client()

    threads.run_in_thread(target=webapp.start_webapp, name='Flask', daemon=True).start()

    # Create a test client using the Flask application configured for testing
    with client as test_client:
        # Establish an application context
        # with app.app_context():
        response = test_client.get('/')
        assert response.status_code == 200
