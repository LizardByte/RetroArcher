"""
..
   __init__.py

Responsible for initialization of RetroArcher.
"""
# future imports
from __future__ import annotations

# standard imports
import os
import sys
import threading
from typing import Union

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
SIGNAL = None  # Signal to watch for
INIT_LOCK = threading.Lock()
QUIET = False


def initialize(config_file: str) -> bool:
    """
    Initialize RetroArcher.

    Sets up config, loggers, and http port.

    Parameters
    ----------
    config_file : str
        The path to the config file.

    Returns
    -------
    bool
        True if initialize succeeds, otherwise False.

    Raises
    ------
    SystemExit
        If unable to correct possible issues with config file.

    Examples
    --------
    >>> initialize(config_file='config.ini')
    True
    """
    with INIT_LOCK:

        global CONFIG
        global CONFIG_FILE
        global DEBUG
        global _INITIALIZED

        try:
            CONFIG = config.create_config(config_file=config_file)
        except Exception:
            raise SystemExit("Unable to initialize due to a corrupted config file. Exiting...")

        CONFIG_FILE = config_file

        assert CONFIG is not None

        logger.blacklist_config(config=CONFIG)  # setup log blacklist

        if _INITIALIZED:
            return False

        # create logs folder
        definitions.Paths.LOG_DIR, log_writable = helpers.check_folder_writable(
            folder=definitions.Paths.LOG_DIR,
            fallback=os.path.join(definitions.Paths.DATA_DIR, 'logs'),
            name='logs'
        )
        if not log_writable and not QUIET:
            sys.stderr.write("Unable to create the log directory. Logging to screen only.\n")

        # setup loggers... cannot use logging until this is finished
        logger.setup_loggers()

        if CONFIG['Network']['HTTP_PORT'] < 21 or CONFIG['Network']['HTTP_PORT'] > 65535:
            log.warning(msg=f"HTTP_PORT out of bounds: 21 < {CONFIG['Network']['HTTP_PORT']} < 65535")
            CONFIG['Network']['HTTP_PORT'] = 9696

        DEBUG = DEBUG or bool(CONFIG['Logging']['DEBUG_LOGGING'])

        _INITIALIZED = True
        return True


def stop(exit_code: Union[int, str] = 0, restart: bool = False):
    """
    Stop RetroArcher.

    This function ends the tray icon if it's running. Then restarts or shutdowns RetroArcher depending on the value of
    the `restart` parameter.

    Parameters
    ----------
    exit_code : Union[int, str], default = 0
        The exit code to send. Does not apply if `restart = True`.
    restart : bool, default = False
        Set to True to restart RetroArcher.

    Examples
    --------
    >>> stop(exit_code=0, restart=False)
    """
    # stop the tray icon
    from pyra.tray_icon import tray_end
    try:
        tray_end()
    except AttributeError:
        pass

    if restart:
        if definitions.Modes.FROZEN:
            args = [definitions.Paths.BINARY_PATH]
        else:
            args = [sys.executable, definitions.Paths.BINARY_PATH]
        args += sys.argv[1:]

        if '--nolaunch' not in args:  # don't launch the browser again
            args += ['--nolaunch']  # also os.execv requires at least one argument

        os.execv(sys.executable, args)
        # alternative to os.execv() ... requires `import subprocess`
        # subprocess.Popen(args=args, cwd=os.getcwd())

    else:
        sys.exit(exit_code)  # this isn't really needed, the code will terminate just after this moment either way
