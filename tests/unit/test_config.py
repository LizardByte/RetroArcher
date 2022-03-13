"""test_config.py

unit tests for pyra.config
"""
# lib imports
from configobj import ConfigObj

# local imports
from pyra import config


def test_create_config(test_config_file):
    """Tests creating a new config file using default config spec"""
    test_config = config.create_config(config_file=test_config_file)
    assert test_config

    assert isinstance(test_config, dict)  # test if test_config is a dictionary
    assert isinstance(test_config, ConfigObj)  # test if test_config is a ConfigObj


def test_validate_config(test_config_file):
    """Creates a new config file using default config spec, and validates it"""
    test_config = config.create_config(config_file=test_config_file)
    config_valid = config.validate_config(config=test_config)
    assert config_valid

    # todo test invalid config
