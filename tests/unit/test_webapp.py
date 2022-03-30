"""test_webapp.py

unit tests for pyra.webapp
"""
# standard imports
import sys

# local imports
from pyra import threads
from pyra import webapp


def test_start_webapp():
    """Test start_webapp function"""
    pass

    # app = webapp.app
    # app.testing = True
    #
    # # disable flask warning banner - https://stackoverflow.com/a/57989189/11214013
    # cli = sys.modules['flask.cli']
    # cli.show_server_banner = lambda *x: None
    #
    # client = app.test_client()
    #
    # threads.run_in_thread(target=webapp.start_webapp, name='Flask', daemon=True).start()
    #
    # # Create a test client using the Flask application configured for testing
    # with client as test_client:
    #     # Establish an application context
    #     # with app.app_context():
    #     response = test_client.get('/')
    #     assert response.status_code == 200
