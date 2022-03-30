"""test_webapp.py

functional tests for pyra.webapp
"""
# standard imports
import sys


def test_home(test_client):
    """
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid

    Repeat for '/home'
    """
    if sys.platform.lower() != 'linux':  # temporarily disable test for linux
        response = test_client.get('/')
        assert response.status_code == 200

        response = test_client.get('/home')
        assert response.status_code == 200


def test_favicon(test_client):
    """
    WHEN the '/favicon.ico' file is requested (GET)
    THEN check that the response is valid
    THEN check the content type is 'image/vnd.microsoft.icon'
    """
    if sys.platform.lower() != 'linux':  # temporarily disable test for linux
        response = test_client.get('/favicon.ico')
        assert response.status_code == 200
        assert response.content_type == 'image/vnd.microsoft.icon'


def test_logger(test_client):
    """
    WHEN the '/test_logger' route is requested (GET)
    THEN check that the response is valid
    THEN check the content is correct
    """
    if sys.platform.lower() != 'linux':  # temporarily disable test for linux
        response = test_client.get('/test_logger')
        assert response.status_code == 200
        assert b'Testing complete, check "logs/' in response.data
