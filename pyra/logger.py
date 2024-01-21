"""
..
   logger.py

Responsible for logging related functions.
"""
# future imports
from __future__ import annotations

# standard imports
import contextlib
import errno
import logging
import multiprocessing
import os
import pkgutil
import re
import sys
import threading
import traceback
from logging import handlers
from logging.handlers import QueueHandler, QueueListener

# lib imports
from configobj import ConfigObj

# local imports
import pyra
from pyra import definitions
from pyra import helpers

# These settings are for file logging only
py_name = 'pyra'
MAX_SIZE = 5000000  # 5 MB
MAX_FILES = 5

# used for log filters
_BLACKLIST_KEYS = ['_APITOKEN', '_TOKEN', '_KEY', '_SECRET', '_PASSWORD', '_APIKEY', '_ID', '_HOOK']
_WHITELIST_KEYS = ['HTTPS_KEY']

LOG_BLACKLIST = []

_BLACKLIST_WORDS = set()

# Global queue for multiprocessing logging
queue = None


def blacklist_config(config: ConfigObj):
    """
    Update blacklist words.

    In order to filter words out of the logs, it is required to call this function.

    Values in the config for keys containing the following terms will be removed.

    - HOOK
    - APIKEY
    - KEY
    - PASSWORD
    - TOKEN

    Parameters
    ----------
    config : ConfigObj
        Config to parse.

    Examples
    --------
    >>> config_object = pyra.config.create_config(config_file='config.ini')
    >>> blacklist_config(config=config_object)
    """
    blacklist = set()
    blacklist_keys = ['HOOK', 'APIKEY', 'KEY', 'PASSWORD', 'TOKEN']

    for k, v in config.items():
        for key, value in v.items():
            if isinstance(value, str) and len(value.strip()) > 5 and \
                    key.upper() not in _WHITELIST_KEYS and (key.upper() in blacklist_keys or
                                                            any(bk in key.upper() for bk in _BLACKLIST_KEYS)):
                blacklist.add(value.strip())

    _BLACKLIST_WORDS.update(blacklist)


class NoThreadFilter(logging.Filter):
    """
    Log filter for the current thread.

    .. todo:: This documentation needs to be improved.

    Parameters
    ----------
    threadName : str
        The name of the thread.

    Methods
    -------
    filter:
        Filter the given record.

    Examples
    --------
    >>> NoThreadFilter('main')
    <pyra.logger.NoThreadFilter object at 0x...>
    """

    def __init__(self, threadName):
        super(NoThreadFilter, self).__init__()

        self.threadName = threadName

    def filter(self, record) -> bool:
        """
        Filter the given record.

        .. todo:: This documentation needs to be improved.

        Parameters
        ----------
        record : NoThreadFilter
            The record to filter.

        Returns
        -------
        bool
            True if record.threadName is not equal to self.threadName, otherwise False.

        Examples
        --------
        >>> NoThreadFilter('main').filter(record=NoThreadFilter('test'))
        True

        >>> NoThreadFilter('main').filter(record=NoThreadFilter('main'))
        False
        """
        return not record.threadName == self.threadName


# Taken from Hellowlol/HTPC-Manager
class BlacklistFilter(logging.Filter):
    """
    Filter logs for blacklisted words.

    Log filter for blacklisted tokens and passwords.

    Methods
    -------
    filter:
        Filter the given record.

    Examples
    --------
    >>> BlacklistFilter()
    <pyra.logger.BlacklistFilter object at 0x...>
    """

    def __init__(self):
        super(BlacklistFilter, self).__init__()

    def filter(self, record) -> bool:
        """
        Filter the given record.

        .. todo:: This documentation needs to be improved.

        Parameters
        ----------
        record : BlacklistFilter
            The record to filter.

        Returns
        -------
        bool
            True in all cases.

        Examples
        --------
        >>> BlacklistFilter().filter(record=BlacklistFilter())
        True
        """
        if not LOG_BLACKLIST:
            return True

        for item in _BLACKLIST_WORDS:
            try:
                if item in record.msg:
                    record.msg = record.msg.replace(item, 16 * '*')

                args = []
                for arg in record.args:
                    try:
                        arg_str = str(arg)
                        if item in arg_str:
                            arg_str = arg_str.replace(item, 16 * '*')
                            arg = arg_str
                    except Exception:
                        pass
                    args.append(arg)
                record.args = tuple(args)
            except Exception:
                pass

        return True


class RegexFilter(logging.Filter):
    """
    Base class for regex log filter.

    Log filter for regex.

    Attributes
    ----------
    regex : re.compile
        The compiled regex pattern.

    Methods
    -------
    filter:
        Filter the given record.

    Examples
    --------
    >>> RegexFilter()
    <pyra.logger.RegexFilter object at 0x...>
    """

    def __init__(self):
        super(RegexFilter, self).__init__()

        self.regex = re.compile(pattern=r'')

    def filter(self, record) -> bool:
        """
        Filter the given record.

        .. todo:: This documentation needs to be improved.

        Parameters
        ----------
        record : RegexFilter
            The record to filter.

        Returns
        -------
        bool
            True in all cases.

        Examples
        --------
        >>> RegexFilter().filter(record=RegexFilter())
        True
        """
        if not LOG_BLACKLIST:
            return True

        try:
            matches = self.regex.findall(record.msg)
            for match in matches:
                record.msg = self.replace(record.msg, match)

            args = []
            for arg in record.args:
                try:
                    arg_str = str(arg)
                    matches = self.regex.findall(arg_str)
                    if matches:
                        for match in matches:
                            arg_str = self.replace(arg_str, match)
                        arg = arg_str
                except Exception:
                    pass
                args.append(arg)
            record.args = tuple(args)
        except Exception:
            pass

        return True

    def replace(self, text, match):
        return text


class PublicIPFilter(RegexFilter):
    """
    Log filter for public IP addresses.

    Class responsible for filtering public IP addresses.

    Attributes
    ----------
    regex : re.compile
        The compiled regex pattern.

    Methods
    -------
    replace:
        Filter that replaces a string within another string.

    Examples
    --------
    >>> PublicIPFilter()
    <pyra.logger.PublicIPFilter object at 0x...>
    """

    def __init__(self):
        super(PublicIPFilter, self).__init__()

        # Currently only checking for ipv4 addresses
        self.regex = re.compile(pattern=r'[0-9]+(?:[.-][0-9]+){3}(?!\d*-[a-z0-9]{6})')

    def replace(self, text: str, ip: str) -> str:
        """
        Filter a public address.

        Filter the given ip address out of the given text. The ip address will only be filter if it is public.

        Parameters
        ----------
        text : str
            The text to replace the ip address within.
        ip : str
            The ip address to replace with asterisks.

        Returns
        -------
        str
            The original text with the ip address replaced.

        Examples
        --------
        >>> PublicIPFilter().replace(text='Testing 172.1.7.5', ip='172.1.7.5')
        'Testing ***.***.***.***'
        """
        if helpers.is_public_ip(ip.replace('-', '.')):
            partition = '-' if '-' in ip else '.'
            return text.replace(ip, partition.join(['***'] * 4))
        return text


class EmailFilter(RegexFilter):
    """
    Log filter for email addresses.

    Class responsible for filtering email addresses.

    Attributes
    ----------
    regex : re.compile
        The compiled regex pattern.

    Methods
    -------
    replace:
        Filter that replaces a string within another string.

    Examples
    --------
    >>> EmailFilter()
    <pyra.logger.EmailFilter object at 0x...>
    """

    def __init__(self):
        super(EmailFilter, self).__init__()

        self.regex = re.compile(pattern=r'([a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*@'
                                r'(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)',
                                flags=re.IGNORECASE)

    def replace(self, text: str, email: str) -> str:
        """
        Filter an email address.

        Filter the given email address out of the given text.

        Parameters
        ----------
        text : str
            The text to replace the email address within.
        email : str
            The email address to replace with asterisks.

        Returns
        -------
        str
            The original text with the email address replaced.

        Examples
        --------
        >>> EmailFilter().replace(text='Testing example@example.com', email='example@example.com')
        'Testing ****************@********'
        """
        email_parts = email.partition('@')
        return text.replace(email, 16 * '*' + email_parts[1] + 8 * '*')


class PlexTokenFilter(RegexFilter):
    """
    Log filter for X-Plex-Token.

    Class responsible for filtering Plex tokens.

    Attributes
    ----------
    regex : re.compile
        The compiled regex pattern.

    Methods
    -------
    replace:
        Filter that replaces a string within another string.

    Examples
    --------
    >>> PlexTokenFilter()
    <pyra.logger.PlexTokenFilter object at 0x...>
    """

    def __init__(self):
        super(PlexTokenFilter, self).__init__()

        self.regex = re.compile(pattern=r'X-Plex-Token(?:=|%3D)([a-zA-Z0-9]+)')

    def replace(self, text: str, token: str) -> str:
        """
        Filter a token.

        Filter the given token out of the given text.

        Parameters
        ----------
        text : str
            The text to replace the token within.
        token : str
            The token to replace with asterisks.

        Returns
        -------
        str
            The original text with the token replaced.

        Examples
        --------
        >>> PlexTokenFilter().replace(text='x-plex-token=5FBCvHo9vFf9erz8ssLQ', token='5FBCvHo9vFf9erz8ssLQ')
        'x-plex-token=****************'
        """
        return text.replace(token, 16 * '*')


@contextlib.contextmanager
def listener(logger: logging.Logger):
    """
    Create a QueueListener.

    Wrapper that create a QueueListener, starts it and automatically stops it.
    To be used in a with statement in the main process, for multiprocessing.

    Parameters
    ----------
    logger : logging.Logger
        The logger object.

    Examples
    --------
    >>> logger = get_logger(name='retroarcher')
    >>> listener(logger=logger)
    """

    global queue

    # Initialize queue if not already done
    if queue is None:
        try:
            queue = multiprocessing.Queue()
        except OSError as e:
            queue = False

            # Some machines don't have access to /dev/shm. See
            # http://stackoverflow.com/questions/2009278 for more information.
            if e.errno == errno.EACCES:
                logger.warning('Multiprocess logging disabled, because current user cannot map shared memory. You '
                               'won\'t see any logging generated by the worker processed.')

    # Multiprocess logging may be disabled.
    if not queue:
        yield
    else:
        queue_listener = QueueListener(queue, *logger.handlers)

        try:
            queue_listener.start()
            yield
        finally:
            queue_listener.stop()


def init_multiprocessing(logger: logging.Logger):
    """
    Remove all handlers and add QueueHandler on top.

    This should only be called inside a multiprocessing worker process, since it changes the logger completely.

    Parameters
    ----------
    logger : logging.Logger
        The logger to initialize for multiprocessing.

    Examples
    --------
    >>> logger = get_logger(name='retroarcher')
    >>> init_multiprocessing(logger=logger)
    """

    # Multiprocess logging may be disabled.
    if not queue:
        return

    # Remove all handlers and add the Queue handler as the only one.
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    queue_handler = QueueHandler(queue)
    queue_handler.setLevel(logging.DEBUG)

    logger.addHandler(queue_handler)

    # Change current thread name for log record
    threading.current_thread().name = multiprocessing.current_process().name


def get_logger(name: str) -> logging.Logger:  # this also exists in helpers.py to prevent circular imports
    """
    Get a logger.

    Return the logging.Logger object for a given name. Additionally, replaces logger.warn with logger.warning.

    Parameters
    ----------
    name : str
        The name of the logger to get.

    Returns
    -------
    logging.Logger
        The logging.Logger object.

    Examples
    --------
    >>> get_logger(name='retroarcher')
    <Logger retroarcher (WARNING)>
    """
    logger = logging.getLogger(name)
    logger.warn = logger.warning  # replace warn with warning

    return logger


def setup_loggers():
    """
    Setup all loggers.

    Setup all the available loggers.

    Examples
    --------
    >>> setup_loggers()
    """
    loggers_list = [py_name, 'werkzeug']

    submodules = pkgutil.iter_modules(pyra.__path__)

    for submodule in submodules:
        loggers_list.append(f'{py_name}.{submodule[1]}')

    for logger_name in loggers_list:
        init_logger(log_name=logger_name)


def init_logger(log_name: str) -> logging.Logger:
    """
    Create a logger.

    Creates a logging.Logger object from the given log name.

    Parameters
    ----------
    log_name : str
        The name of the log to create.

    Returns
    -------
    logging.Logger
        The logging.Logger object.

    Examples
    --------
    >>> init_logger(log_name='retroarcher')
    <Logger retroarcher (INFO)>
    """
    logger = logging.getLogger(name=log_name)

    # Close and remove old handlers. This is required to reinitialize the loggers at runtime
    log_handlers = logger.handlers
    for handler in log_handlers:
        # Just make sure it is cleaned up.
        if isinstance(handler, handlers.RotatingFileHandler):
            handler.close()
        elif isinstance(handler, logging.StreamHandler):
            handler.flush()

        logger.removeHandler(handler)

    # Configure the logger to accept all messages
    logger.propagate = False
    logger.setLevel(logging.DEBUG if pyra.DEBUG else logging.INFO)

    # Setup file logger
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)-7s :: %(threadName)s : %(message)s',
                                       '%Y-%m-%d %H:%M:%S')

    # Setup file logger
    log_dir = definitions.Paths.LOG_DIR
    if os.path.isdir(log_dir):
        filename = os.path.join(log_dir, f'{log_name}.log')
        file_handler = handlers.RotatingFileHandler(filename=filename, maxBytes=MAX_SIZE, backupCount=MAX_FILES,
                                                    encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)

        logger.addHandler(file_handler)

    # Setup console logger
    if not pyra.QUIET:
        console_formatter = logging.Formatter('%(asctime)s - %(levelname)s :: %(threadName)s : %(message)s',
                                              '%Y-%m-%d %H:%M:%S')
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(logging.DEBUG)

        logger.addHandler(console_handler)

    # Add filters to log handlers
    # Only add filters after the config file has been initialized
    # Nothing prior to initialization should contain sensitive information
    if not pyra.DEV and pyra.CONFIG:
        log_handlers = logger.handlers
        for handler in log_handlers:
            handler.addFilter(BlacklistFilter())
            handler.addFilter(PublicIPFilter())
            handler.addFilter(EmailFilter())
            handler.addFilter(PlexTokenFilter())

    # Install exception hooks
    if log_name == py_name:  # all tracebacks go to 'pyra.log'
        _init_hooks(logger)

    # replace warn
    # logger.warn = logger.warning

    return logger


def _init_hooks(logger: logging.Logger, global_exceptions: bool = True, thread_exceptions: bool = True,
                pass_original: bool = True):
    """This method installs exception catching mechanisms.

    Any exception caught will pass through the exception hook, and will be logged to the logger as an error.
    Additionally, a traceback is provided.

    This is very useful for crashing threads and any other bugs, that may not be exposed when running as daemon.

    The default exception hook is still considered, if pass_original is True.
    """

    def excepthook(*exception_info):
        # We should always catch this to prevent loops!
        try:
            message = "".join(traceback.format_exception(*exception_info))
            logger.error("Uncaught exception: %s", message)
        except Exception:
            pass

        # Original excepthook
        if pass_original:
            sys.__excepthook__(*exception_info)

    # Global exception hook
    if global_exceptions:
        sys.excepthook = excepthook

    # Thread exception hook
    if thread_exceptions:
        old_init = threading.Thread.__init__

        def new_init(self, *args, **kwargs):
            old_init(self, *args, **kwargs)
            old_run = self.run

            def new_run(*args, **kwargs):
                try:
                    old_run(*args, **kwargs)
                except (KeyboardInterrupt, SystemExit):
                    raise
                except Exception:
                    excepthook(*sys.exc_info())

            self.run = new_run

        # Monkey patch the run() by monkey patching the __init__ method
        threading.Thread.__init__ = new_init


def shutdown():
    """
    Stop logging.

    Shutdown logging.

    Examples
    --------
    >>> shutdown()
    """
    logging.shutdown()


# get logger
log = get_logger(name=__name__)
