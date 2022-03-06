"""definitions.py

Contains classes with attributes to common definitions (paths and filenames).
"""
# standard imports
import os
import sys

# local imports
import pyra


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
        LOG_DIR (str): The directory containing log files.
    """

    def __init__(self):
        self.PYRA_DIR = os.path.dirname(os.path.abspath(__file__))
        self.ROOT_DIR = os.path.dirname(self.PYRA_DIR)

        if pyra.FROZEN:  # pyinstaller build
            self.DATA_DIR = os.path.dirname(sys.executable)
        else:
            self.DATA_DIR = self.ROOT_DIR

        self.LOG_DIR = os.path.join(self.DATA_DIR, 'logs')
