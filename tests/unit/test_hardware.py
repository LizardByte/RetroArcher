"""
..
   test_hardware.py

Unit tests for common.hardware.py.
"""
# lib imports
import pytest

# local imports
from common import hardware


def test_update():
    """
    Test the update function.

    Ensures the initialized variable is updated.
    """
    assert not hardware.initialized  # make sure initialized is False

    count = 0
    while count < 2:
        hardware.update()  # first run just initializes

        assert hardware.initialized  # make sure initialized is True

        for stat_type, data in hardware.dash_stats.items():
            for key in data:
                assert len(data[key]) == count  # make sure no length of each list is the same as number of updates

        count += 1


def test_update_cpu():
    """
    Test the update_cpu function.

    Tests that the function returns a value between 0 and 100.

    Additionally tests that there are values added to the dash_stats dictionary.
    """
    test_cpu_percent = hardware.update_cpu()
    assert test_cpu_percent <= 100  # test if value is number with a max value of 100
    assert test_cpu_percent >= 0  # test if value is number with a min value of 0

    assert hardware.dash_stats['cpu']['system']
    assert test_cpu_percent == hardware.dash_stats['cpu']['system'][-1]


def test_update_gpu():
    """
    Test the update_gpu function.

    This test is conditional depending on if gpus are available.

    This function doesn't return anything, so this will test the dash_stats dictionary.
    """
    if not hardware.nvidia_gpus and not hardware.amd_gpus:
        pytest.skip("gpu not supported")

    hardware.update_gpu()

    assert hardware.dash_stats['gpu']


def test_update_memory():
    """
    Test the update_memory function.

    Tests that the function returns a value between 0 and 100.

    Additionally tests that there are values added to the dash_stats dictionary.
    """
    test_memory_percent = hardware.update_memory()
    assert test_memory_percent <= 100  # test if value is number with a max value of 100
    assert test_memory_percent >= 0  # test if value is number with a min value of 0

    assert hardware.dash_stats['memory']['system']
    assert test_memory_percent == hardware.dash_stats['memory']['system'][-1]


def test_update_network():
    """
    Test the update_network function.

    Tests that the function returns a value greater than 0.

    Additionally tests that there are values added to the dash_stats dictionary.
    """
    test_network_usage = hardware.update_network()
    assert isinstance(test_network_usage, tuple)  # test if value is tuple
    for value in test_network_usage:
        assert value >= 0  # test if value is number with a min value of 0

    assert hardware.dash_stats['network']['received']
    assert test_network_usage[0] == hardware.dash_stats['network']['received'][-1]

    assert hardware.dash_stats['network']['sent']
    assert test_network_usage[1] == hardware.dash_stats['network']['sent'][-1]


def test_chart_data():
    """
    Test the chart_data function.

    Validates that the returned dictionary is properly formed.
    """
    chart_data = hardware.chart_data()
    assert isinstance(chart_data, dict)  # test if value is dict
    assert isinstance(chart_data['graphs'], list)  # test if value is list

    for x in chart_data['graphs']:
        assert isinstance(x, dict)  # test if each item is a dictionary
        assert x['data']
        assert x['layout']
        assert x['config']


def test_chart_types():
    """
    Test the chart_types function.

    Validate that chart types returns a list of the correct values.
    """
    chart_types = hardware.chart_types()
    assert isinstance(chart_types, list)  # test if value is list
    assert 'cpu' in chart_types
    assert 'memory' in chart_types
    assert 'network' in chart_types

    if hardware.nvidia_gpus or hardware.amd_gpus:
        assert 'gpu' in chart_types
