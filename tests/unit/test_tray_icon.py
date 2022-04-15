"""
..
   test_tray_icon.py

Unit tests for pyra.tray_icon.
"""
# lib imports
import pytest

# local imports
import pyra
from pyra import tray_icon


@pytest.fixture(scope='module')
def test_tray_icon():
    """Initialize and run a test tray icon"""
    test_tray_icon = tray_icon.tray_initialize()

    tray_icon.tray_run()

    yield test_tray_icon


def test_tray_initialize(test_tray_icon):
    """Test tray initialization"""
    if test_tray_icon is not False:  # may be False for linux
        assert isinstance(test_tray_icon, tray_icon.icon_class)

        # these test whether the OS supports the feature, not if the menu has the feature
        # assert test_tray_icon.HAS_MENU  # on linux this may be False in some cases
        # assert test_tray_icon.HAS_DEFAULT_ACTION  # does not work on macOS
        # assert test_tray_icon.HAS_MENU_RADIO  # does not work on macOS
        # assert test_tray_icon.HAS_NOTIFICATION  # does not work on macOS or xorg


def test_tray_run(test_tray_icon):
    """Test tray_run function"""
    try:
        tray_icon.icon_class
    except AttributeError:
        pass
    else:
        if isinstance(test_tray_icon, tray_icon.icon_class):  # may be False for linux
            assert test_tray_icon


def test_tray_browser(test_config_object):
    """Test tray_browser function"""
    original_value = test_config_object['General']['LAUNCH_BROWSER']

    tray_icon.tray_browser()
    new_value = test_config_object['General']['LAUNCH_BROWSER']

    assert new_value is not original_value


def test_tray_disable(test_config_object):
    """Test tray_disable function"""
    tray_icon.tray_disable()
    new_value = test_config_object['General']['SYSTEM_TRAY']

    assert new_value is False


def test_tray_end(test_config_object):
    """Test tray_end function"""
    tray_icon.tray_end()
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


def test_tray_open_browser_functions():
    """Test all tray functions that open a page in a browser"""
    assert tray_icon.open_webapp()
    assert tray_icon.github_releases()
    assert tray_icon.donate_github()
    assert tray_icon.donate_mee6()
    assert tray_icon.donate_patreon()
    assert tray_icon.donate_paypal()
