"""
..
   tray_icon.py

Responsible for system tray icon and related functions.
"""
# standard imports
import os
from typing import Union

# lib imports
from PIL import Image

# local imports
import pyra
from pyra import config
from pyra import definitions
from pyra import helpers
from pyra import locales
from pyra import logger

# setup
_ = locales.get_text()
icon_running = False
icon_supported = False
log = logger.get_logger(name=__name__)

# conditional imports
if definitions.Platform().platform == 'linux':
    try:
        import Xlib
    except Exception:
        pass
try:
    from pystray import Icon, MenuItem, Menu
except Xlib.error.DisplayNameError:
    Icon = None
else:
    icon_class = Icon  # avoids a messy import for pytest
    icon_supported = True

# additional setup
icon: Union[Icon, bool] = False


def tray_initialize() -> Union[Icon, bool]:
    """
    Initialize the system tray icon.

    Some features of the tray icon may not be available, depending on the operating system. An attempt is made to setup
    the tray icon with all the available features supported by the OS.

    Returns
    -------
    Union[Icon, bool]
        Icon
            Instance of pystray.Icon if icon is supported.
        bool
            False if icon is not supported.

    Examples
    --------
    >>> tray_initialize()
    """
    if not icon_supported:
        return False
    tray_icon = Icon(name='retroarcher')
    tray_icon.title = definitions.Names().name

    image = Image.open(os.path.join(definitions.Paths().ROOT_DIR, 'web', 'images', 'retroarcher.ico'))
    tray_icon.icon = image

    # NOTE: Open the application. "%(app_name)s" = "RetroArcher". Do not translate "%(app_name)s".
    first_menu_entry = MenuItem(text=_('Open %(app_name)s') % {'app_name': definitions.Names().name},
                                action=open_webapp, default=True if tray_icon.HAS_DEFAULT_ACTION else False)

    if tray_icon.HAS_MENU:
        menu = (
            first_menu_entry,
            Menu.SEPARATOR,
            # NOTE: Open Github Releases. "%(github)s" = "GitHUB". Do not translate "%(github)s".
            MenuItem(text=_('%(github)s Releases') % {'github': 'GitHub'}, action=github_releases),
            MenuItem(
                # NOTE: Donate to RetroArcher.
                text=_('Donate'), action=Menu(
                    MenuItem(text='GitHub Sponsors', action=donate_github),
                    MenuItem(text='MEE6', action=donate_mee6),
                    MenuItem(text='Patreon', action=donate_patreon),
                    MenuItem(text='PayPal', action=donate_paypal),
                )
            ),
            Menu.SEPARATOR,
            # NOTE: Open web browser when application starts. Do not translate "%(app_name)s".
            MenuItem(text=_('Open browser when %(app_name)s starts') % {'app_name': definitions.Names().name},
                     action=tray_browser, checked=lambda item: config.CONFIG['General']['LAUNCH_BROWSER']),
            # NOTE: Disable or turn off icon.
            MenuItem(text=_('Disable Icon'), action=tray_disable),
            Menu.SEPARATOR,
            # NOTE: Restart the program.
            MenuItem(text=_('Restart'), action=tray_restart),
            # NOTE: Quit, Stop, End, or Shutdown the program.
            MenuItem(text=_('Quit'), action=tray_quit),
        )

    else:
        menu = (
            first_menu_entry,
        )

    tray_icon.menu = menu

    return tray_icon


def tray_browser():
    """
    Toggle the config option 'LAUNCH_BROWSER'.

    This functions switches the `LAUNCH_BROWSER` config option from True to False, or False to True.

    Examples
    --------
    >>> tray_browser()
    """
    # toggle the value of LAUNCH_BROWSER
    config.CONFIG['General']['LAUNCH_BROWSER'] = not config.CONFIG['General']['LAUNCH_BROWSER']

    config.save_config(config.CONFIG)


def tray_disable():
    """
    Turn off the config option 'SYSTEM_TRAY'.

    This function ends and disables the `SYSTEM_TRAY` config option.

    Examples
    --------
    >>> tray_disable()
    """
    tray_end()
    config.CONFIG['General']['SYSTEM_TRAY'] = False
    config.save_config(config.CONFIG)


def tray_end():
    """
    End the system tray icon.

    Hide and then stop the system tray icon.

    Examples
    --------
    >>> tray_end()
    """
    try:
        icon_class
    except NameError:
        pass
    else:
        if isinstance(icon, icon_class):
            try:  # this shouldn't be possible to call, other than through pytest
                icon.visible = False
            except AttributeError:
                pass

            try:
                icon.stop()
            except AttributeError:
                pass
            except Exception as e:
                log.error(f'Exception when stopping system tray icon: {e}')
            else:
                global icon_running
                icon_running = False


def tray_quit():
    """
    Shutdown RetroArcher.

    Set the 'pyra.SIGNAL' variable to 'shutdown'.

    Examples
    --------
    >>> tray_quit()
    """
    pyra.SIGNAL = 'shutdown'


def tray_restart():
    """
    Restart RetroArcher.

    Set the 'pyra.SIGNAL' variable to 'restart'.

    Examples
    --------
    >>> tray_restart()
    """
    pyra.SIGNAL = 'restart'


def tray_run():
    """
    Start the tray icon.

    Run the system tray icon in detached mode.

    Examples
    --------
    >>> tray_run()
    """
    try:
        icon_class
    except NameError:
        pass
    else:
        global icon_running

        if isinstance(icon, icon_class):
            try:
                icon.run_detached()
            except AttributeError:
                pass
            except NotImplementedError as e:
                log.error(f'Error running system tray icon: {e}')
            else:
                icon_running = True


def open_webapp() -> bool:
    """
    Open the webapp.

    Open RetroArcher in the default web browser.

    Returns
    -------
    bool
        True if opening page was successful, otherwise False.

    Examples
    --------
    >>> open_webapp()
    True
    """
    url = f"http://127.0.0.1:{config.CONFIG['Network']['HTTP_PORT']}"
    return helpers.open_url_in_browser(url=url)


def github_releases():
    """
    Open GitHub Releases.

    Open GitHub Releases in the default web browser.

    Returns
    -------
    bool
        True if opening page was successful, otherwise False.

    Examples
    --------
    >>> github_releases()
    True
    """
    url = 'https://github.com/RetroArcher/RetroArcher/releases/latest'
    return helpers.open_url_in_browser(url=url)


def donate_github():
    """
    Open GitHub Sponsors.

    Open GitHub Sponsors in the default web browser.

    Returns
    -------
    bool
        True if opening page was successful, otherwise False.

    Examples
    --------
    >>> donate_github()
    True
    """
    url = 'https://github.com/sponsors/ReenigneArcher'
    return helpers.open_url_in_browser(url=url)


def donate_mee6():
    """
    Open MEE6.

    Open MEE6 in the default web browser.

    Returns
    -------
    bool
        True if opening page was successful, otherwise False.

    Examples
    --------
    >>> donate_mee6()
    True
    """
    url = 'https://mee6.xyz/m/804382334370578482'
    return helpers.open_url_in_browser(url=url)


def donate_patreon():
    """
    Open Patreon.

    Open Patreon in the default web browser.

    Returns
    -------
    bool
        True if opening page was successful, otherwise False.

    Examples
    --------
    >>> donate_patreon()
    True
    """
    url = 'https://www.patreon.com/RetroArcher'
    return helpers.open_url_in_browser(url=url)


def donate_paypal():
    """
    Open PayPal.

    Open PayPal in the default web browser.

    Returns
    -------
    bool
        True if opening page was successful, otherwise False.

    Examples
    --------
    >>> donate_paypal()
    True
    """
    url = 'https://www.paypal.com/paypalme/ReenigneArcher'
    return helpers.open_url_in_browser(url=url)
