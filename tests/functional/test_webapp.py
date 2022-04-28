"""
..
   test_webapp.py

Functional tests for pyra.webapp.
"""


def test_home(test_client):
    """
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid

    Repeat for '/home'
    """
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
    response = test_client.get('/favicon.ico')
    assert response.status_code == 200
    assert response.content_type == 'image/vnd.microsoft.icon'


def test_callback_dashboard(test_client):
    """
    WHEN the '/callback/dashboard' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/callback/dashboard')
    assert response.status_code == 200
    assert response.data.startswith(b'[{"data": [')
    assert response.data.endswith(b'}]')


def test_docs(test_client):
    """
    WHEN the '/docs/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/docs/')
    assert response.status_code == 200


def test_status(test_client):
    """
    WHEN the '/status' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/status')
    assert response.status_code == 200
    assert response.content_type == 'application/json'


def test_test_logger(test_client):
    """
    WHEN the '/test_logger' route is requested (GET)
    THEN check that the response is valid
    THEN check the content is correct
    """
    response = test_client.get('/test_logger')
    assert response.status_code == 200
    assert b'Testing complete, check "logs/' in response.data
