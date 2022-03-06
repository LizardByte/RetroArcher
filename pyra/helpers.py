"""helpers.py

Lots of helper functions.
"""
# future imports
from __future__ import annotations

# standard imports
import datetime
import logging
import re
import os
import socket
import time

# lib imports
from IPy import IP


def check_folder_writable(folder: str | None, fallback: str, name: str) -> tuple[str, bool | None]:
    """Checks if folder or fallback folder is writeable.

    :param folder: str - Primary folder to check.
    :param fallback: str - Secondary folder to check.
    :param name: str - Short name of folder.
    :return bool - True if writeable, otherwise False.
    """
    if not folder:
        folder = fallback

    if not os.path.isdir(s=folder):
        try:
            os.makedirs(name=folder)
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


def get_logger(name: str) -> logging.Logger:
    """Return the logger for the given name.

    This function also exists in `logger.py` to prevent circular imports.

    :param name: str - name of logger
    :return: Logger object
    """
    return logging.getLogger(name=name)


def is_public_ip(host: str) -> bool:
    """Check if ip address is public or not.

    :param host: str - IP address
    :return: bool - True if ip address is public
    """
    ip = is_valid_ip(address=get_ip(host=host))
    if ip and ip.iptype() == 'PUBLIC':
        return True
    return False


def get_ip(host: str) -> str:
    """Get ip address from host name.

    :param host: str - Host name
    :return: str - IP address of host name
    """
    if is_valid_ip(address=host):
        return host
    elif not re.match(pattern=r'^[0-9]+(?:\.[0-9]+){3}(?!\d*-[a-z0-9]{6})$', string=host):
        try:
            ip_address = socket.getaddrinfo(host=host, port=None)[0][4][0]
        except:
            log.error(f"IP Checker :: Bad IP or hostname provided: {host}.")
        else:
            log.debug(f"IP Checker :: Resolved {host} to {ip_address}.")
            return ip_address


def is_valid_ip(address: str) -> IP | bool:
    """Check if address is a valid ip address.

    :param address: str - Address to check.
    :return: IP object | bool - IP object if address is an ip address, otherwise False.
    """
    try:
        return IP(address)
    except TypeError:
        return False
    except ValueError:
        return False


def now(separate: bool = False) -> str:
    """Function to get the current time, formatted.

    :param separate: bool - True to separate time with a combination of dashes (`-`) and colons (`:`). Default = False
    :return: str - The current time formatted as YMDHMS
    """
    return timestamp_to_YMDHMS(ts=timestamp(), separate=separate)


def timestamp() -> int:
    """Function to get the current time.

    :return: int - The current time as a timestamp integer.
    """
    return int(time.time())


def timestamp_to_YMDHMS(ts: int, separate: bool = False) -> str:
    """Function to convert timestamp to YMDHMS format.

    :param ts: int - The timestamp to convert.
    :param separate: bool - True to separate time with a combination of dashes (`-`) and colons (`:`). Default = False
    :return: str - The current time formatted as YMDHMS
    """
    dt = timestamp_to_datetime(ts=ts)
    if separate:
        return dt.strftime(fmt="%Y-%m-%d %H:%M:%S")
    return dt.strftime(fmt="%Y%m%d%H%M%S")


def timestamp_to_datetime(ts: float) -> datetime.datetime:
    """Function to convert timestamp to datetime object.

    :param ts: float - The timestamp to convert.
    :return: datetime object
    """
    return datetime.datetime.fromtimestamp(ts)


# get logger
log = get_logger(name=__name__)
