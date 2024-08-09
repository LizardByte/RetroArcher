"""
..
   test_tray_icon.py

Unit tests for common.tray_icon.
"""
# standard imports
import time

# lib imports
import pytest

# local imports
import common
from common import tray_icon


@pytest.fixture(scope='function')
def initial_tray():
    """Test tray initialization"""
    tray_icon_instance = tray_icon.tray_initialize()

    if tray_icon_instance is not False:  # may be False for linux
        assert isinstance(tray_icon_instance, tray_icon.icon_class)

        # these test whether the OS supports the feature, not if the menu has the feature
        # assert test_tray_icon.HAS_MENU  # on linux this may be False in some cases
        # assert test_tray_icon.HAS_DEFAULT_ACTION  # does not work on macOS
        # assert test_tray_icon.HAS_MENU_RADIO  # does not work on macOS
        # assert test_tray_icon.HAS_NOTIFICATION  # does not work on macOS or xorg

        assert tray_icon_instance.visible is False

    yield tray_icon_instance


@pytest.fixture(scope='function')
def tray_supported(initial_tray):
    """Test tray_run function"""
    try:
        tray_icon.icon_class
    except AttributeError:
        yield
    else:
        if isinstance(initial_tray, tray_icon.icon_class):  # may be False for linux
            assert initial_tray

            yield True
        else:
            yield False


@pytest.fixture(scope='function')
def running_tray(initial_tray, tray_supported):
    """Test tray_run and tray_disable functions"""
    if not tray_supported:
        pytest.skip("tray icon not supported")

    tray_threaded_return_value = tray_icon.tray_run_threaded()

    time.sleep(1)  # give a little time for everything to be setup

    assert isinstance(tray_threaded_return_value, bool)
    assert tray_threaded_return_value is True
    assert tray_icon.icon_running is True

    yield tray_threaded_return_value

    if tray_threaded_return_value:
        tray_icon.tray_end()
        assert tray_icon.icon_running is False


def test_tray_disable(initial_tray, running_tray, test_config_object):
    """Test tray_disable function"""
    test_config_object['General']['SYSTEM_TRAY'] = True
    tray_icon.tray_disable()
    new_value = test_config_object['General']['SYSTEM_TRAY']

    assert new_value is False
    assert tray_icon.icon_running is False


def test_tray_end(initial_tray, tray_supported, running_tray):
    """Test tray_end function"""
    if not tray_supported:
        pytest.skip("tray icon not supported")

    tray_icon.tray_end()

    assert tray_icon.icon_running is False
    assert initial_tray.visible is False


def test_tray_toggle(initial_tray, tray_supported, running_tray):
    """Test tray_toggle function"""
    if not tray_supported:
        pytest.skip("tray icon not supported")

    for _ in range(5):
        original_value = tray_icon.icon_running
        tray_icon.tray_toggle()
        time.sleep(1)
        assert tray_icon.icon_running is not original_value


def test_tray_browser(test_config_object):
    """Test tray_browser function"""
    original_value = test_config_object['General']['LAUNCH_BROWSER']

    tray_icon.tray_browser()
    new_value = test_config_object['General']['LAUNCH_BROWSER']

    assert new_value is not original_value


def test_tray_quit():
    """Test tray_quit function"""
    tray_icon.tray_quit()

    signal = common.SIGNAL

    assert signal == 'shutdown'


def test_tray_restart():
    """Test tray_restart function"""
    tray_icon.tray_restart()

    signal = common.SIGNAL

    assert signal == 'restart'


def test_tray_open_browser_functions():
    """Test all tray functions that open a page in a browser"""
    open_browser_functions = [
        tray_icon.open_webapp,
        tray_icon.github_releases,
        tray_icon.donate_github,
        tray_icon.donate_mee6,
        tray_icon.donate_patreon,
        tray_icon.donate_paypal
    ]

    for function in open_browser_functions:
        assert function.__call__()
