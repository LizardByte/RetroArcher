"""test_tray_icon.py

unit tests for pyra.tray_icon
"""
# lib imports
import pystray

# local imports
import pyra
from pyra import tray_icon


def test_tray_initialize():
    """Test tray initialization"""
    tray = tray_icon.tray_initialize()
    assert isinstance(tray, pystray.Icon)

    assert tray.HAS_DEFAULT_ACTION
    assert tray.HAS_MENU


def test_tray_browser(test_config_object):
    """Test tray_browser function"""
    original_value = test_config_object['General']['LAUNCH_BROWSER']

    tray_icon.tray_browser()
    new_value = test_config_object['General']['LAUNCH_BROWSER']

    assert new_value is not original_value


def test_tray_disable(test_config_object, test_tray_icon):
    """Test tray_disable function"""
    tray_icon.tray_disable()
    new_value = test_config_object['General']['SYSTEM_TRAY']

    assert new_value is False


def test_tray_end(test_config_object, test_tray_icon):
    """Test tray_end function"""
    tray_icon.tray_disable()
    new_value = test_config_object['General']['SYSTEM_TRAY']

    assert new_value is False


def test_tray_quit():
    """Test tray_quit function"""
    tray_icon.tray_quit()

    signal = pyra.SIGNAL

    assert signal == 'shutdown'


def test_tray_restart():
    """Test tray_restart function"""
    tray_icon.tray_restart()

    signal = pyra.SIGNAL

    assert signal == 'restart'


def test_tray_run(test_tray_icon):
    """Test tray_run function"""
    assert test_tray_icon


def test_tray_open_browser_functions():
    """Test all tray functions that open a page in a browser"""
    assert tray_icon.open_webapp()
    assert tray_icon.github_releases()
    assert tray_icon.donate_github()
    assert tray_icon.donate_mee6()
    assert tray_icon.donate_patreon()
    assert tray_icon.donate_paypal()
