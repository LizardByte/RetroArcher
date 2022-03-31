"""test_tray_icon.py

unit tests for pyra.tray_icon
"""
# lib imports
import pytest

# local imports
import pyra


@pytest.fixture(scope='module')
def tray_icon():  # this is a hack to allow tray_icon to import properly
    from pyra import config  # tray_icon won't import properly without this
    config.CONFIG = config.create_config('test_config.ini')
    from pyra import tray_icon  # import tray_icon after setting config.CONFIG

    yield tray_icon


@pytest.fixture(scope='module')
def test_tray_icon(tray_icon):
    """Initialize and run a test tray icon"""
    test_tray_icon = tray_icon.tray_initialize()

    tray_icon.tray_run()

    yield test_tray_icon


def test_tray_initialize(tray_icon, test_tray_icon):
    """Test tray initialization"""
    if test_tray_icon is not None:  # may be None for linux
        assert isinstance(test_tray_icon, tray_icon.icon_class)

        # these test whether the OS supports the feature, not if the menu has the feature
        assert test_tray_icon.HAS_MENU
        # assert test_tray_icon.HAS_DEFAULT_ACTION  # does not work on macOS
        # assert test_tray_icon.HAS_MENU_RADIO  # does not work on macOS
        # assert test_tray_icon.HAS_NOTIFICATION  # does not work on macOS or xorg


def test_tray_run(test_tray_icon):
    """Test tray_run function"""
    if test_tray_icon is not None:  # may be None for linux
        assert test_tray_icon


def test_tray_browser(test_config_object, tray_icon):
    """Test tray_browser function"""
    original_value = test_config_object['General']['LAUNCH_BROWSER']

    tray_icon.tray_browser()
    new_value = test_config_object['General']['LAUNCH_BROWSER']

    assert new_value is not original_value


def test_tray_disable(test_config_object, tray_icon):
    """Test tray_disable function"""
    tray_icon.tray_disable()
    new_value = test_config_object['General']['SYSTEM_TRAY']

    assert new_value is False


def test_tray_end(test_config_object, tray_icon):
    """Test tray_end function"""
    tray_icon.tray_end()
    new_value = test_config_object['General']['SYSTEM_TRAY']

    assert new_value is False


def test_tray_quit(tray_icon):
    """Test tray_quit function"""
    tray_icon.tray_quit()

    signal = pyra.SIGNAL

    assert signal == 'shutdown'


def test_tray_restart(tray_icon):
    """Test tray_restart function"""
    tray_icon.tray_restart()

    signal = pyra.SIGNAL

    assert signal == 'restart'


def test_tray_open_browser_functions(tray_icon):
    """Test all tray functions that open a page in a browser"""
    assert tray_icon.open_webapp()
    assert tray_icon.github_releases()
    assert tray_icon.donate_github()
    assert tray_icon.donate_mee6()
    assert tray_icon.donate_patreon()
    assert tray_icon.donate_paypal()
