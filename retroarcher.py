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
from pyra import helpers
from pyra import locales
from pyra import logger
from pyra import threads
from pyra import webapp

py_name = 'pyra'

# locales
_ = locales.get_text()

# get logger
log = logger.get_logger(name=py_name)


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
    if hasattr(sys, 'frozen') and hasattr(sys, '_MEIPASS'):  # only when using the pyinstaller build
        pyra.FROZEN = True

        if definitions.Platform().platform != 'darwin':  # pyi_splash is not available on macos
            pyra.SPLASH = True

        if pyra.SPLASH:
            import pyi_splash  # module cannot be installed outside of pyinstaller builds
            pyi_splash.update_text("Attempting to start RetroArcher")

    # Set up and gather command line arguments
    parser = argparse.ArgumentParser(description=_('RetroArcher is a Python based game streaming server.\n'
                                                   'Arguments supplied here are meant to be temporary.'))

    parser.add_argument('--config', help=_('Specify a config file to use'))
    parser.add_argument('--debug', action='store_true', help=_('Use debug logging level'))
    parser.add_argument('--dev', action='store_true', help=_('Start RetroArcher in the development environment'))
    parser.add_argument('--nolaunch', action='store_true', help=_('Do not open RetroArcher in browser'))
    parser.add_argument(
        '-p', '--port', default=9696, type=IntRange(21, 65535),
        help=_('Force RetroArcher to run on a specified port, default=9696')
    )
    parser.add_argument('-q', '--quiet', action='store_true', help=_('Turn off console logging'))
    parser.add_argument(
        '-v', '--version', action='store_true',
        help=_('Print the version details and exit.')
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
    pyra.initialize(config_file=config_file)  # logging should not occur until after this point

    if args.config:
        log.info(msg=f"RetroArcher is using custom config file: {config_file}.")
    if args.debug:
        log.info(msg="RetroArcher will log debug messages.")
    if args.dev:
        log.info(msg="RetroArcher is running in the dev environment.")
    if args.quiet:
        log.info(msg="RetroArcher is running in quiet mode. Nothing will be printed to console.")

    if args.port:
        config.CONFIG['Network']['HTTP_PORT'] = args.port
        config.CONFIG.write()

    if config.CONFIG['General']['SYSTEM_TRAY']:
        from pyra import tray_icon
        threads.run_in_thread(target=tray_icon.tray_run, name='pystray', daemon=True).start()  # may be a problem on mac

    if config.CONFIG['General']['LAUNCH_BROWSER'] and not args.nolaunch:
        url = f"http://127.0.0.1:{config.CONFIG['Network']['HTTP_PORT']}"
        helpers.open_url_in_browser(url=url)

    # start the webapp
    if pyra.SPLASH:  # pyinstaller build only, not darwin platforms
        pyi_splash.update_text("Starting the webapp")
        time.sleep(3)  # show splash screen for a min of 3 seconds
        pyi_splash.close()  # close the splash screen
    threads.run_in_thread(target=webapp.start_webapp, name='Flask', daemon=True).start()

    wait()  # wait for signal


def wait():
    """Waits for signal.

    Endlessly loop while `pyra.SIGNAL = None`.
    If `pyra.SIGNAL` is changed to `shutdown` or `restart` `pyra.stop()` will be executed.
    If KeyboardInterrupt signal is detected `pyra.stop()` will be executed.
    """
    log.info("RetroArcher is ready!")

    # Wait endlessly for a signal
    while True:
        if not pyra.SIGNAL:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                pyra.SIGNAL = 'shutdown'
        else:
            log.info(f'Received signal: {pyra.SIGNAL}')

            if pyra.SIGNAL == 'shutdown':
                pyra.stop()
            elif pyra.SIGNAL == 'restart':
                pyra.stop(restart=True)
            else:
                log.error('Unknown signal. Shutting down...')
                pyra.stop()

            pyra.SIGNAL = None

            break


if __name__ == "__main__":
    main()
