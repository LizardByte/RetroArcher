"""
src/common/definitions.py

Contains classes with attributes to common definitions (paths and filenames).
"""
# standard imports
import os
import platform
import sys


class Names:
    """
    Class representing common names.

    The purpose of this class is to ensure consistency when using these names.

    name : str
        The application's name. i.e. `RetroArcher`.

    Examples
    --------
    >>> Names.name
    'RetroArcher'
    """
    name = 'RetroArcher'


class Platform:
    """
    Class representing the machine platform.

    The purpose of this class is to ensure consistency when there is a need for platform specific functions.

    bits : str
        Operating system bitness. e.g. 64.
    operating_system : str
        Operating system name. e.g. 'Windows'.
    os_platform : str
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
    >>> Platform.os_platform
    ...
    """
    bits = 64 if sys.maxsize > 2**32 else 32
    operating_system = platform.system()
    os_platform = sys.platform.lower()
    processor = platform.processor()
    machine = platform.machine()
    node = platform.node()
    release = platform.release()
    version = platform.version()

    # Windows only
    edition = platform.win32_edition() if os_platform == 'win32' else None
    iot = platform.win32_is_iot() if os_platform == 'win32' else False


class Modes:
    """
    Class representing runtime variables.

    FROZEN : bool
        ``True`` if running pyinstaller bundle version, otherwise ``False``.
    DOCKER : bool
        ``True`` if running Docker version, otherwise ``False``.
    SPLASH : bool
        ``True`` if capable of displaying a splash image on start, otherwise, ``False``.

    Examples
    --------
    >>> Modes.FROZEN
    False
    """
    FROZEN = False
    DOCKER = False
    SPLASH = False

    if hasattr(sys, 'frozen') and hasattr(sys, '_MEIPASS'):  # only when using the pyinstaller build
        FROZEN = True

        if Platform.os_platform != 'darwin':  # pyi_splash is not available on macos
            SPLASH = True

    if os.getenv('RETROARCHER_DOCKER', False):  # the environment variable is set in the Dockerfile
        DOCKER = True


class Files:
    """
    Class representing common Files.

    The purpose of this class is to ensure consistency when using these files.

    CONFIG : str
        The default config file name. i.e. `config.ini`.

    Examples
    --------
    >>> Files.CONFIG
    'config.ini'
    """
    CONFIG = 'config.ini'


class Paths:
    """
    Class representing common Paths.

    The purpose of this class is to ensure consistency when using these paths.

    COMMON_DIR : str
        The directory containing the common python files.
    SRC_DIR : str
        The directory containing the application python files
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
    >>> Paths.LOG_DIR
    '.../logs'
    """
    COMMON_DIR = os.path.dirname(os.path.abspath(__file__))
    SRC_DIR = os.path.dirname(COMMON_DIR)
    ROOT_DIR = os.path.dirname(SRC_DIR)
    DATA_DIR = ROOT_DIR
    BINARY_PATH = os.path.abspath(os.path.join(SRC_DIR, 'retroarcher.py'))

    if Modes.FROZEN:  # pyinstaller build
        DATA_DIR = os.path.dirname(sys.executable)
        BINARY_PATH = os.path.abspath(sys.executable)
    if Modes.DOCKER:  # docker install
        DATA_DIR = '/config'  # overwrite the value that was already set
        CONFIG_DIR = DATA_DIR
    else:
        CONFIG_DIR = os.path.join(DATA_DIR, 'config')

    DOCS_DIR = os.path.join(ROOT_DIR, 'docs', 'build', 'html')
    LOCALE_DIR = os.path.join(ROOT_DIR, 'locale')
    LOG_DIR = os.path.join(CONFIG_DIR, 'logs')
