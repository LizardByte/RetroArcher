"""
..
   test_helpers.py

Unit tests for pyra.helpers.py.
"""
# standard imports
import datetime
import logging

# local imports
from pyra import helpers


def test_check_folder_writeable():
    """Tests that folder can be created if it doesn't exist"""
    folder, status = helpers.check_folder_writable(folder='temp', fallback='temp', name='temp')

    assert folder
    assert status


def test_get_logger():
    """Test that logger object can be created"""
    test_logger = helpers.get_logger(name='pyra')
    assert isinstance(test_logger, logging.Logger)


def test_is_public_ip():
    """Test if ip address is pubic, then tests if ip address is private"""
    # test public ip
    address = 'www.google.com'
    ip = helpers.get_ip(host=address)
    public_ip = helpers.is_public_ip(host=ip)
    assert public_ip

    # test private ip
    ip = '192.168.1.1'
    public_ip = helpers.is_public_ip(host=ip)
    assert not public_ip


def test_get_ip():
    """Tests getting ip address from web address, private address, and known bad address"""
    # test public address
    address = 'www.google.com'
    ip = helpers.get_ip(host=address)
    assert ip

    # test private address
    address = '192.168.1.1'
    ip = helpers.get_ip(host=address)
    assert ip

    # test bad address
    address = '0.0.0.0.0'
    ip = helpers.get_ip(host=address)
    assert not ip


def test_is_valid_ip():
    """Test if ip is valid for web address, private address, and known bad address"""
    # test public address
    address = 'www.google.com'
    ip = helpers.get_ip(host=address)
    valid_ip = helpers.is_valid_ip(address=ip)
    assert valid_ip

    # test private address
    ip = '192.168.1.1'
    valid_ip = helpers.is_valid_ip(address=ip)
    assert valid_ip

    # test bad address
    ip = '0.0.0.0.0'
    valid_ip = helpers.is_valid_ip(address=ip)
    assert not valid_ip


def test_now():
    """Tests if now function returns string in proper format"""
    now = helpers.now(separate=False)
    assert isinstance(now, str)
    assert '-' not in now  # ensure separator is not in now

    now = helpers.now(separate=True)
    assert isinstance(now, str)
    assert '-' in now  # ensure separator is in now


def test_open_url_in_browser():
    """Tests if open_url_in_browser function completes without error"""
    result = helpers.open_url_in_browser(url='https://www.google.com')
    assert result


def test_timestamp():
    """Tests if timestamp is returned as an integer"""
    timestamp = helpers.timestamp()
    assert timestamp
    assert isinstance(timestamp, int)  # ensure timestamp is int


def test_timestamp_to_YMDHMS():
    """Tests if converted timestamp is a string and contains a '-' or not"""
    timestamp = helpers.timestamp()
    converted_timestamp = helpers.timestamp_to_YMDHMS(ts=timestamp, separate=False)
    assert isinstance(converted_timestamp, str)
    assert int(converted_timestamp)  # ensure timestamp string can be converted to int
    assert '-' not in converted_timestamp  # ensure separator is not in converted_timestamp

    converted_timestamp = helpers.timestamp_to_YMDHMS(ts=timestamp, separate=False)
    assert isinstance(converted_timestamp, str)
    assert '-' not in converted_timestamp  # ensure separator is not in converted_timestamp


def test_timestamp_to_datetime():
    """Tests if timestamp is converted to datetime object"""
    test_datetime = helpers.timestamp_to_datetime(ts=helpers.timestamp())
    assert test_datetime
    assert isinstance(test_datetime, datetime.datetime)
