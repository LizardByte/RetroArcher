"""
..
   test_webapp.py

Functional tests for pyra.webapp.
"""
# standard imports
import json


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
    data = json.loads(response.data)

    assert isinstance(data, dict)  # ensure the data is a dict
    assert isinstance(data['graphs'], list)  # ensure the data is a list
    for x in data['graphs']:
        assert x['data']
        assert x['layout']
        assert x['config']


def test_docs(test_client):
    """
    WHEN the '/docs/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/docs/')
    assert response.status_code == 200


def test_settings(test_client):
    """
    WHEN the '/settings/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/settings/')
    assert response.status_code == 200


def test_api_settings(test_client):
    """
    WHEN the '/api/settings' page is requested (GET or POST)
    THEN check that the response is valid
    """
    get_response = test_client.get('/api/settings')
    assert get_response.status_code == 200
    assert get_response.content_type == 'application/json'

    post_response = test_client.post('/api/settings')
    assert post_response.status_code == 200
    assert post_response.content_type == 'application/json'
    assert post_response.json['status'] == 'OK'
    assert post_response.json['message'] == 'Selected settings are valid.'

    # todo, test posting data (valid and invalid)


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
