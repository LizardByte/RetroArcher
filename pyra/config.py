"""config.py

Responsible for config related functions.
"""
# standard imports
import sys

# lib imports
from configobj import ConfigObj
from validate import Validator, ValidateError

# local imports
from pyra import definitions
from pyra import helpers

# get log
log = helpers.get_logger(name=__name__)  # must use helpers.get_log due to circular import

# get the config filename
FILENAME = definitions.Files().CONFIG

# access the config dictionary here
CONFIG = None

# increase CONFIG_VERSION default when changing default values
# then do `if CONFIG_VERSION == x:` something to change the old default value to the new default value
# then update the CONFIG_VERSION number
_CONFIG_SPEC = [
    '[Hidden]',
    'CONFIG_VERSION = integer(min=0, default=0)',
    'FIRST_RUN_COMPLETE = boolean(default=False)',  # todo
    '[Logging]',
    'LOG_DIR = string',
    'DEBUG_LOGGING = boolean(default=True)',
    '[Network]',
    'HTTP_HOST = string(default="0.0.0.0")',
    'HTTP_PORT = integer(min=21, max=65535, default=9696)',
    'HTTP_ROOT = string',
    '[Updater]',
    'AUTO_UPDATE = boolean(default=False)',
]

# used for log filters
_BLACKLIST_KEYS = ['_APITOKEN', '_TOKEN', '_KEY', '_SECRET', '_PASSWORD', '_APIKEY', '_ID', '_HOOK']
_WHITELIST_KEYS = ['HTTPS_KEY']

LOG_BLACKLIST = []


def create_config(config_file: str, config_spec: list=_CONFIG_SPEC) -> ConfigObj:
    """Create a config file and ConfigObj using a config spec.

    The created config is validated against a Validator object. This function will remove keys from the user's
    config.ini if they no longer exist in the config spec.

    :param config_file: str - Full filename of config file
    :param config_spec: list - Config spec to use
    :return config: ConfigObj
    :raise SystemExit: exception - If config_spec is not valid
    """
    config = ConfigObj(
        configspec=config_spec,
        encoding='UTF-8',
        list_values=True,
        stringify=True,
        write_empty_values=False
    )
    config_valid = validate_config(config=config)

    if not config_valid:
        # logger may not be initialized
        log_msg = "Unable to initialize due to a corrupted config spec. Exiting..."
        log.error(msg=log_msg)
        raise SystemExit(log_msg)

    user_config = ConfigObj(
        infile=config_file,
        configspec=config_spec,
        encoding='UTF-8',
        list_values=True,
        stringify=True,
        write_empty_values=False
    )
    user_config_valid = validate_config(config=user_config)
    if not user_config_valid:
        # write to stderr and logger
        log_msg = "Invalid 'config.ini' file, attempting to correct.\n"
        log.error(msg=log_msg)
        sys.stderr.write(s=log_msg)

    # dictionary comprehension
    if config_valid and user_config_valid:
        # remove values from user config that are no longer in the spec
        user_config = {
            key: {
                k: v for k, v in value.items() if k in config.get(key, {})
            } for key, value in user_config.items()
        }

        # remove sections from user config that are no longer in the spec
        user_config = {key: value for key, value in user_config.items() if key in config}

        # merge user config into default config
        config.merge(indict=user_config)

        # validate merged config
        validate_config(config=config)

    config.filename = config_file
    config.write()  # write the config file

    if config_spec == _CONFIG_SPEC:  # set CONFIG dictionary
        global CONFIG
        CONFIG = config

    return config


def validate_config(config: ConfigObj) -> bool:
    """Validates ConfigObj dictionary.

    :param config: ConfigObj - Config to validate
    :return: bool - True if validation passes, otherwise False
    """
    validator = Validator()
    try:
        config.validate(
            validator=validator,
            copy=False  # don't write out default values
        )
        return True
    except ValidateError as e:
        log_msg = f"Config validation error: {e}.\n"
        log.error(msg=log_msg)
        sys.stderr.write(s=log_msg)
        return False
