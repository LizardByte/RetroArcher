"""tray_icon.py

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


def tray_initialize() -> Union[Icon, bool]:
    """Initializes the system tray icon.

    :return Instance of pystray.Icon if icon is supported, otherwise False
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
    """Toggle the config option 'LAUNCH_BROWSER'."""
    # toggle the value of LAUNCH_BROWSER
    config.CONFIG['General']['LAUNCH_BROWSER'] = not config.CONFIG['General']['LAUNCH_BROWSER']

    config.save_config(config.CONFIG)


def tray_disable():
    """Turn off the config option 'SYSTEM_TRAY'."""
    tray_end()
    config.CONFIG['General']['SYSTEM_TRAY'] = False
    config.save_config(config.CONFIG)


def tray_end():
    """Hide the system tray icon, then stop the system tray icon."""
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
    """Set the 'pyra.SIGNAL' variable to 'shutdown'."""
    pyra.SIGNAL = 'shutdown'


def tray_restart():
    """Set the 'pyra.SIGNAL' variable to 'restart'."""
    pyra.SIGNAL = 'restart'


def tray_run():
    """Run the system tray icon in detached mode."""
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


def open_webapp():
    """Open RetroArcher in the default web browser."""
    url = f"http://127.0.0.1:{config.CONFIG['Network']['HTTP_PORT']}"
    return helpers.open_url_in_browser(url=url)


def github_releases():
    """Open GitHub Releases in the default web browser."""
    url = 'https://github.com/RetroArcher/RetroArcher/releases/latest'
    return helpers.open_url_in_browser(url=url)


def donate_github():
    """Open GitHub Sponsors in the default web browser."""
    url = 'https://github.com/sponsors/ReenigneArcher'
    return helpers.open_url_in_browser(url=url)


def donate_mee6():
    """Open MEE6 in the default web browser."""
    url = 'https://mee6.xyz/m/804382334370578482'
    return helpers.open_url_in_browser(url=url)


def donate_patreon():
    """Open Patreon in the default web browser."""
    url = 'https://www.patreon.com/RetroArcher'
    return helpers.open_url_in_browser(url=url)


def donate_paypal():
    """Open PayPal in the default web browser."""
    url = 'https://www.paypal.com/paypalme/ReenigneArcher'
    return helpers.open_url_in_browser(url=url)


icon: Union[Icon, bool] = tray_initialize()
