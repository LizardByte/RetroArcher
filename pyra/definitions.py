"""definitions.py

Contains classes with attributes to common definitions (paths and filenames).
"""
# standard imports
import os
import platform
import sys

# local imports
import pyra


class Platform:
    """This is a class representing the machine platform.

    Attributes:
        bits (str): Operating system name. e.g. Windows
        operating_system (str): Operating system name. e.g. Windows
        platform (str): Operating system platform. e.g. win32, darwin, linux
        machine (str): Machine architecture. e.g. AMD64
        node (str): Machine name
        release (str): Operating system release. e.g. 10
        version (str): Operating system version. e.g. 10.0.22000
        edition (str): Windows edition. e.g. Core, None for non Windows platforms.
        iot (bool): True if Windows IOT, otherwise False
    """

    def __init__(self):
        self.bits = 64 if sys.maxsize > 2**32 else 32
        self.operating_system = platform.system()
        self.platform = sys.platform.lower()
        self.processor = platform.processor()
        self.machine = platform.machine()
        self.node = platform.node()
        self.release = platform.release()
        self.version = platform.version()

        # Windows only
        self.edition = platform.win32_edition() if self.platform == 'win32' else None
        self.iot = platform.win32_is_iot() if self.platform == 'win32' else False


class Files:
    """This is a class representing constant filenames used by RetroArcher.

    Attributes:
        CONFIG (str): The config filename.
    """

    def __init__(self):
        self.CONFIG = 'config.ini'


class Paths:
    """This is a class representing constant paths used by RetroArcher.

    Attributes:
        PYRA_DIR (str): The directory containing the retroarcher python files.
        ROOT_DIR (str): The root directory of the application. This is where the source files exist.
        DATA_DIR (str): The data directory of the application.
        LOCALE_DIR (str): The directory containing localization files.
        LOG_DIR (str): The directory containing log files.
    """

    def __init__(self):
        self.PYRA_DIR = os.path.dirname(os.path.abspath(__file__))
        self.ROOT_DIR = os.path.dirname(self.PYRA_DIR)

        if pyra.FROZEN:  # pyinstaller build
            self.DATA_DIR = os.path.dirname(sys.executable)
        else:
            self.DATA_DIR = self.ROOT_DIR

        self.LOCALE_DIR = os.path.join(self.ROOT_DIR, 'locale')
        self.LOG_DIR = os.path.join(self.DATA_DIR, 'logs')
