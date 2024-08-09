"""
..
   test_config.py

Unit tests for common.config.
"""
# standard imports
import time

# lib imports
from configobj import ConfigObj
import pytest

# local imports
from common import config


def test_create_config(test_config_file):
    """Tests creating a new config file using default config spec"""
    test_config = config.create_config(config_file=test_config_file)
    assert test_config

    assert isinstance(test_config, dict)  # test if test_config is a dictionary
    assert isinstance(test_config, ConfigObj)  # test if test_config is a ConfigObj


def test_save_config(test_config_object):
    saved = config.save_config(config=test_config_object)
    assert saved


def test_validate_config(test_config_object):
    """Creates a new config file using default config spec, and validates it"""
    config_valid = config.validate_config(config=test_config_object)
    assert config_valid

    # todo test invalid config


def test_convert_config():
    result = config.convert_config()

    assert isinstance(result, list)


def test_on_change_tray_toggle():
    """Tests the on_change_tray_toggle function"""
    from common import tray_icon

    if not tray_icon.icon_supported:
        pytest.skip("tray icon not supported")

    original_value = tray_icon.icon_running

    result = config.on_change_tray_toggle()
    assert result is True

    time.sleep(1)
    assert tray_icon.icon_running is not original_value
