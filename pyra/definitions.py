"""
..
   definitions.py

Contains classes with attributes to common definitions (paths and filenames).
"""
# standard imports
import os
import platform
import sys

# local imports
import pyra


class Names:
    """
    Class representing common names.

    The purpose of this class is to ensure consistency when using these names.

    Attributes
    ----------
    name : str
        The application's name. i.e. `RetroArcher`.

    Examples
    --------
    >>> Names()
    <pyra.definitions.Names object at 0x...>

    >>> Names().name
    'RetroArcher'
    """
    def __init__(self):
        self.name = 'RetroArcher'


class Platform:
    """
    Class representing the machine platform.

    The purpose of this class is to ensure consistency when there is a need for platform specific functions.

    Attributes
    ----------
    bits : str
        Operating system bitness. e.g. 64.
    operating_system : str
        Operating system name. e.g. 'Windows'.
    platform : str
        Operating system platform. e.g. 'win32', 'darwin', 'linux'.
    machine : str
        Machine architecture. e.g. 'AMD64'.
    node : str
        Machine name.
    release : str
        Operating system release. e.g. '10'.
    version : str
        Operating system version. e.g. '10.0.22000'.
    edition : str
        Windows edition. e.g. 'Core', None for non Windows platforms.
    iot : bool
        True if Windows IOT, otherwise False.

    Examples
    --------
    >>> Platform()
    <pyra.definitions.Platform object at 0x...>

    >>> Platform().bits
    64
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
    """
    Class representing common Files.

    The purpose of this class is to ensure consistency when using these files.

    Attributes
    ----------
    CONFIG : str
        The default config file name. i.e. `config.ini`.

    Examples
    --------
    >>> Files()
    <pyra.definitions.Files object at 0x...>

    >>> Files().CONFIG
    'config.ini'
    """
    def __init__(self):
        self.CONFIG = 'config.ini'


class Paths:
    """
    Class representing common Paths.

    The purpose of this class is to ensure consistency when using these paths.

    Attributes
    ----------
    PYRA_DIR : str
        The directory containing the retroarcher python files.
    ROOT_DIR : str
        The root directory of the application. This is where the source files exist.
    DATA_DIR : str
        The data directory of the application.
    DOCS_DIR : str
        The directory containing html documentation.
    LOCALE_DIR : str
        The directory containing localization files.
    LOG_DIR : str
        The directory containing log files.

    Examples
    --------
    >>> Paths()
    <pyra.definitions.Paths object at 0x...>

    >>> Paths().logs
    '.../logs'
    """
    def __init__(self):
        self.PYRA_DIR = os.path.dirname(os.path.abspath(__file__))
        self.ROOT_DIR = os.path.dirname(self.PYRA_DIR)

        if pyra.FROZEN:  # pyinstaller build
            self.DATA_DIR = os.path.dirname(sys.executable)
            self.BINARY_PATH = os.path.abspath(sys.executable)
        else:
            self.DATA_DIR = self.ROOT_DIR
            self.BINARY_PATH = os.path.abspath(os.path.join(self.DATA_DIR, 'retroarcher.py'))

        if pyra.DOCKER:  # docker install
            self.DATA_DIR = '/config'  # overwrite the value that was already set

        self.DOCS_DIR = os.path.join(self.ROOT_DIR, 'docs', 'build', 'html')
        self.LOCALE_DIR = os.path.join(self.ROOT_DIR, 'locale')
        self.LOG_DIR = os.path.join(self.DATA_DIR, 'logs')
