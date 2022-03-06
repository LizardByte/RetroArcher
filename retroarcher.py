#!/usr/bin/env python3
"""retroarcher.py

Responsible for starting RetroArcher.
"""
# future imports
from __future__ import annotations

# standard imports
import argparse
import os
import sys
import time

# local imports
import pyra
from pyra import config
from pyra import definitions
from pyra import logger
from pyra import webapp

py_name = 'pyra'


class IntRange(object):
    """Custom IntRange class for argparse.

    Prevents printing out large list of possible choices for integer ranges.

    Raises argparse.ArgumentTypeError if provided value is outside the accepted range.
    """
    def __init__(self, stop: int, start: int = 0,):
        """Initialize the IntRange class object.

        If stop is less than start, the values will be corrected automatically.

        :param stop: int - Range maximum value (required)
        :param start: int - Range minimum value (optional). Default = 0
        """
        if stop < start:
            stop, start = start, stop
        self.start, self.stop = start, stop

    def __call__(self, value: int | str) -> int:
        """Validates value is within accepted range.

        :param value: int | str - The value to validate.
        :return: int - Returned if value is valid, otherwise argparse.ArgumentTypeError is raised.
        """
        value = int(value)
        if value < self.start or value >= self.stop:
            raise argparse.ArgumentTypeError(f'Value outside of range: ({self.start}, {self.stop})')
        return value


def main():
    """Application entry point.

    Parses arguments and initializes the application.
    """
    # Fixed paths to RetroArcher
    if hasattr(sys, 'frozen') and hasattr(sys, '_MEIPASS'):
        pyra.FROZEN = True

        import pyi_splash  # module cannot be installed and is only available when using the pyinstaller build
        pyi_splash.update_text("Attempting to start RetroArcher")

    # Set up and gather command line arguments
    parser = argparse.ArgumentParser(description='RetroArcher is a Python based game streaming server.\n'
                                                 'Arguments supplied here are meant to be temporary.')

    parser.add_argument('--config', help='Specify a config file to use')
    parser.add_argument('--debug', action='store_true', help='Use debug logging level')
    parser.add_argument('--dev', action='store_true', help='Start RetroArcher in the development environment')
    parser.add_argument(
        '-p', '--port', default=9696, type=IntRange(21, 65535),
        help='Force RetroArcher to run on a specified port, default=9696'
    )
    parser.add_argument('-q', '--quiet', action='store_true', help='Turn off console logging')
    parser.add_argument(
        '-v', '--version', action='store_true',
        help='Print the version details and exit.'
    )

    args = parser.parse_args()

    if args.version:
        print('todo_v')  # todo
        SystemExit()

    if args.config:
        config_file = args.config
    else:
        config_file = os.path.join(definitions.Paths().DATA_DIR, definitions.Files().CONFIG)
    if args.debug:
        pyra.DEBUG = True
    if args.dev:
        pyra.DEV = True
    if args.quiet:
        pyra.QUIET = True

    # initialize retroarcher
    pyra.initialize(config_file=config_file)

    # get logger
    log = logger.get_logger(name=py_name)

    if args.config:
        log.info(msg=f"RetroArcher is using custom config file: {config_file}.")
    if args.debug:
        log.info(msg="RetroArcher will log debug messages.")
    if args.dev:
        log.info(msg="RetroArcher is running in the dev environment.")
    if args.quiet:
        log.info(msg="RetroArcher is running in quiet mode. Nothing will be printed to console.")

    if args.port != 9696:
        config.CONFIG['Network']['HTTP_PORT'] = args.port
        config.CONFIG.write()

    # start the webapp
    if pyra.FROZEN:  # pyinstaller build only
        pyi_splash.update_text("Starting the webapp")
        time.sleep(3)  # show splash screen for a min of 3 seconds
        pyi_splash.close()  # close the splash screen
    webapp.app.run(
        host=config.CONFIG['Network']['HTTP_HOST'],
        port=config.CONFIG['Network']['HTTP_PORT'],
        debug=pyra.DEV
    )


if __name__ == "__main__":
    main()
