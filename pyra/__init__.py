"""__init__.py

Responsible for initializing RetroArcher.
"""
# standard imports
import os
import sys
import threading

# local imports
from pyra import config
from pyra import definitions
from pyra import helpers
from pyra import logger

# get logger
log = logger.get_logger(name=__name__)

_INITIALIZED = False
CONFIG = None
CONFIG_FILE = None
DEBUG = False
DEV = False
DOCKER = False  # True if running in docker container (#todo)
FROZEN = False  # True if running pyinstaller package
INIT_LOCK = threading.Lock()
QUIET = False


def initialize(config_file: str) -> bool:
    """Initialize RetroArcher.

    :param config_file: str - Full filepath to config.ini file.
    :return: bool - True if initialize succeeds, otherwise False.
    :raise SystemExit: exception - If unable to correct possible issues with config file.
    """
    with INIT_LOCK:

        global CONFIG
        global CONFIG_FILE
        global DEBUG
        global _INITIALIZED

        try:
            CONFIG = config.create_config(config_file=config_file)
        except:
            raise SystemExit("Unable to initialize due to a corrupted config file. Exiting...")

        CONFIG_FILE = config_file

        assert CONFIG is not None

        logger.blacklist_config(config=CONFIG)  # setup log blacklist

        if _INITIALIZED:
            return False

        # create logs folder
        definitions.Paths().LOG_DIR, log_writable = helpers.check_folder_writable(
            folder=definitions.Paths().LOG_DIR,
            fallback=os.path.join(definitions.Paths().DATA_DIR, 'logs'),
            name='logs'
        )
        if not log_writable and not QUIET:
            sys.stderr.write(s="Unable to create the log directory. Logging to screen only.\n")

        # setup loggers... cannot use logging until this is finished
        logger.setup_loggers()

        if CONFIG['Network']['HTTP_PORT'] < 21 or CONFIG['Network']['HTTP_PORT'] > 65535:
            log.warning(msg=f"HTTP_PORT out of bounds: 21 < {CONFIG['Network']['HTTP_PORT']} < 65535")
            CONFIG['Network']['HTTP_PORT'] = 9696

        DEBUG = DEBUG or bool(CONFIG['Logging']['DEBUG_LOGGING'])

        _INITIALIZED = True
        return True
