"""test_webapp.py

unit tests for pyra.webapp
"""
# local imports
from pyra import threads
from pyra import webapp


def test_start_webapp():
    """Test start_webapp function"""
    app = webapp.app
    app.testing = True
    client = app.test_client()

    threads.run_in_thread(target=webapp.start_webapp, name='Flask', daemon=True).start()

    # Create a test client using the Flask application configured for testing
    with client as test_client:
        # Establish an application context
        # with app.app_context():
        response = test_client.get('/')
        assert response.status_code == 200
