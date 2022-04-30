"""
..
   test_hardware.py

Unit tests for pyra.hardware.py.
"""
# local imports
from pyra import hardware


def test_update_cpu():
    """Tests if update_cpu returns a float value"""
    test_cpu_percent = hardware.update_cpu()
    assert test_cpu_percent <= 100  # test if value is number with a max value of 100
    assert test_cpu_percent >= 0  # test if value is number with a min value of 0


def test_update_gpu():
    """
    # todo... this test needs to be defined
    """
    pass


def test_update_memory():
    """Tests if update_memory returns a float value"""
    test_memory_percent = hardware.update_memory()
    assert test_memory_percent <= 100  # test if value is number with a max value of 100
    assert test_memory_percent >= 0  # test if value is number with a min value of 0


def test_update_network():
    """Tests if update_network returns a tuple containing two float values"""
    test_network_usage = hardware.update_network()
    assert isinstance(test_network_usage, tuple)  # test if value is tuple
    for value in test_network_usage:
        assert value >= 0  # test if value is number with a min value of 0


def test_update():
    """
    Tests the update function.

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


def test_chart_data():
    """Tests the chart_data function."""
    chart_data = hardware.chart_data()
    assert isinstance(chart_data, list)  # test if value is string

    for x in chart_data:
        assert isinstance(x, dict)  # test if each item is a dictionary
        assert x['data']
        assert x['layout']
        assert x['config']


def test_chart_types():
    """Tests the chart_types function."""
    chart_types = hardware.chart_types()
    assert isinstance(chart_types, list)  # test if value is list
    assert 'cpu' in chart_types
    assert 'memory' in chart_types
    assert 'network' in chart_types
