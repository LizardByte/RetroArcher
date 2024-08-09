"""
src/common/helpers.py

Many reusable helper functions.
"""
# standard imports
import datetime
import ipaddress
import logging
import re
import os
import requests
import socket
import time
from typing import Optional, Union
import webbrowser

# lib imports
from IPy import IP


def check_folder_writable(fallback: str, name: str, folder: Optional[str] = None) -> tuple[str, Optional[bool]]:
    """
    Check if folder or fallback folder is writeable.

    This function ensures that the folder can be created, if it doesn't exist. It also ensures there are sufficient
    permissions to write to the folder. If the primary `folder` fails, it falls back to the `fallback` folder.

    Parameters
    ----------
    fallback : str
        Secondary folder to check, if the primary folder fails.
    name : str
        Short name of folder.
    folder : str, optional
        Primary folder to check.

    Returns
    -------
    tuple[str, Optional[bool]]
        A tuple containing:
            folder : str
                The original or fallback folder.
            Optional[bool]
                True if writeable, otherwise False. Nothing is returned if there is an error attempting to create the
                directory.

    Examples
    --------
    >>> check_folder_writable(
    ...     folder='logs',
    ...     fallback='backup_logs',
    ...     name='logs'
    ...     )
    ('logs', True)
    """
    if not folder:
        folder = fallback

    try:
        os.makedirs(name=folder)  # try to make the directory
    except OSError as e:
        log.error(msg=f"Could not create {name} dir '{folder}': {e}")
        if fallback and folder != fallback:
            log.warning(msg=f"Falling back to {name} dir '{fallback}'")
            return check_folder_writable(folder=None, fallback=fallback, name=name)
        else:
            return folder, None

    if not os.access(path=folder, mode=os.W_OK):
        log.error(msg=f"Cannot write to {name} dir '{folder}'")
        if fallback and folder != fallback:
            log.warning(msg=f"Falling back to {name} dir '{fallback}'")
            return check_folder_writable(folder=None, fallback=fallback, name=name)
        else:
            return folder, False

    return folder, True


def docker_healthcheck() -> bool:
    """
    Check the health of the docker container.

    .. Warning:: This is only meant to be called by `retroarcher.py`, and the interpreter should be immediate exited
       following the result.

    The default port is used considering that the container will use the default port internally.
    The external port should not make any difference.

    Returns
    -------
    bool
        True if status okay, otherwise False.

    Examples
    --------
    >>> docker_healthcheck()
    True
    """
    protocols = ['http', 'https']

    for p in protocols:
        try:
            response = requests.get(url=f'{p}://localhost:9696/status')
        except requests.exceptions.ConnectionError:
            pass
        else:
            if response.status_code == 200:
                return True

    return False  # did not get a valid response, so return False


def get_logger(name: str) -> logging.Logger:
    """
    Get the logger for the given name.

    This function also exists in `logger.py` to prevent circular imports.

    Parameters
    ----------
    name : str
        Name of logger.

    Returns
    -------
    logging.Logger
        The logging.Logger object.

    Examples
    --------
    >>> get_logger(name='my_log')
    <Logger my_log (WARNING)>
    """
    return logging.getLogger(name=name)


def is_public_ip(host: str) -> bool:
    """
    Check if ip address is public or not.

    This function is used to determine if the given host address is a public ip address or not.

    Parameters
    ----------
    host : str
        IP address to check.

    Returns
    -------
    bool
        True if ip address is public, otherwise False.

    Examples
    --------
    >>> is_public_ip(host='www.google.com')
    True

    >>> is_public_ip(host='192.168.1.1')
    False
    """
    ip = is_valid_ip(address=get_ip(host=host))

    # use built in ipaddress module to check if address is private since IPy does not work IPv6 addresses
    if ip:
        ip_obj = ipaddress.ip_address(address=ip)
        return not ip_obj.is_private
    else:
        return False


def get_ip(host: str) -> Optional[str]:
    """
    Get IP address from host name.

    This function is used to get the IP address of a given host name.

    Parameters
    ----------
    host : str
        Host name to get ip address of.

    Returns
    -------
    str
        IP address of host name if it is a valid ip address, otherwise ``None``.

    Examples
    --------
    >>> get_ip(host='192.168.1.1')
    '192.168.1.1'

    >>> get_ip(host='www.google.com')
    '172.253.63.147'
    """
    if is_valid_ip(address=host):
        return host
    elif not re.match(pattern=r'^[0-9]+(?:\.[0-9]+){3}(?!\d*-[a-z0-9]{6})$', string=host):
        try:
            ip_address = socket.getaddrinfo(host=host, port=None)[0][4][0]
        except Exception:
            log.error(f"IP Checker :: Bad IP or hostname provided: {host}.")
            return None
        else:
            log.debug(f"IP Checker :: Resolved {host} to {ip_address}.")
            return ip_address


def is_valid_ip(address: str) -> Union[IP, bool]:
    """
    Check if address is an ip address.

    This function is used to determine if the given address is an ip address or not.

    Parameters
    ----------
    address : str
        Address to check.

    Returns
    -------
    Union[IP, bool]
        IP object if address is an ip address, otherwise False.

    Examples
    --------
    >>> is_valid_ip(address='192.168.1.1')
    True

    >>> is_valid_ip(address='0.0.0.0.0')
    False
    """
    try:
        return IP(address)
    except TypeError:
        return False
    except ValueError:
        return False


def now(separate: bool = False) -> str:
    """
    Function to get the current time, formatted.

    This function will return the current time formatted as YMDHMS

    Parameters
    ----------
    separate : bool, default = False
        True to separate time with a combination of dashes (`-`) and colons (`:`).

    Returns
    -------
    str
        The current time formatted as YMDHMS.

    Examples
    --------
    >>> now()
    '20220410184531'

    >>> now(separate=True)
    '2022-04-10 18:46:12'
    """
    return timestamp_to_YMDHMS(ts=timestamp(), separate=separate)


def open_url_in_browser(url: str) -> bool:
    """
    Open a given url in the default browser.

    Attempt to open the given url in the default web browser, in a new tab.

    Parameters
    ----------
    url : str
        The url to open.

    Returns
    -------
    bool
        True if no error, otherwise False.

    Examples
    --------
    >>> open_url_in_browser(url='https://www.google.com')
    True
    """
    try:
        webbrowser.open(url=url, new=2)
    except webbrowser.Error:
        return False
    else:
        return True


def timestamp() -> int:
    """
    Function to get the current time.

    This function uses time.time() to get the current time.

    Returns
    -------
    int
        The current time as a timestamp integer.

    Examples
    --------
    >>> timestamp()
    1649631005
    """
    return int(time.time())


def timestamp_to_YMDHMS(ts: int, separate: bool = False) -> str:
    """
    Convert timestamp to YMDHMS format.

    Convert a given timestamp to YMDHMS format.

    Parameters
    ----------
    ts : int
        The timestamp to convert.
    separate : bool, default = False
        True to separate time with a combination of dashes (`-`) and colons (`:`).

    Returns
    -------
    str
        The timestamp formatted as YMDHMS.

    Examples
    --------
    >>> timestamp_to_YMDHMS(ts=timestamp(), separate=False)
    '20220410185142'

    >>> timestamp_to_YMDHMS(ts=timestamp(), separate=True)
    '2022-04-10 18:52:09'
    """
    dt = timestamp_to_datetime(ts=ts)
    if separate:
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    return dt.strftime("%Y%m%d%H%M%S")


def timestamp_to_datetime(ts: float) -> datetime.datetime:
    """
    Convert timestamp to datetime object.

    This function returns the result of `datetime.datetime.fromtimestamp()`.

    Parameters
    ----------
    ts : float
        The timestamp to convert.

    Returns
    -------
    datetime.datetime
        Object `datetime.datetime`.

    Examples
    --------
    >>> timestamp_to_datetime(ts=timestamp())
    datetime.datetime(20..., ..., ..., ..., ..., ...)
    """
    return datetime.datetime.fromtimestamp(ts)


# get logger
log = get_logger(name=__name__)
