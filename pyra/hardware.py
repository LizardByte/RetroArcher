"""
..
   hardware.py

Functions related to the dashboard viewer.
"""
# standard imports
import json

# lib imports
import GPUtil
import plotly
import psutil

# local imports
from pyra import definitions
from pyra import helpers
from pyra import locales
from pyra import logger

_ = locales.get_text()
chart_translations = dict(
    cpu=dict(
        bare=_('cpu'),
        usage=_('cpu usage')
    ),
    gpu=dict(
        bare=_('gpu'),
        usage=_('gpu usage')
    ),
    memory=dict(
        bare=_('memory'),
        usage=_('memory usage')
    ),
    network=dict(
        bare=_('network'),
        usage=_('network usage')
    ),
    general=dict(
        received=_('received'),
        sent=_('sent'),
        system=_('system')
    )
)

log = logger.get_logger(__name__)

initialized = False
network_recv_last = 0
network_sent_last = 0
proc = psutil.Process()  # the main retroarcher process
proc_id = proc.pid
processes = [proc]

nvidia_gpus = GPUtil.getGPUs()

try:
    import pyamdgpuinfo
except ModuleNotFoundError:
    amd_gpus = 0
else:
    amd_gpus = pyamdgpuinfo.detect_gpus()  # this will be an integer representing the count of amd gpus

dash_stats = dict(
    timestamp=[],
    relative_time=[],
    cpu_system=[],
    memory_system=[],
    network_sent=[],
    network_received=[]
)

history_length = 120


def update_cpu() -> float:
    """
    Update dashboard stats for system CPU usage.

    This will append a new value to the ``dash_stats['cpu_system']`` list.

    Returns
    -------
    float
        The current system cpu percentage utilized.

    Examples
    --------
    >>> update_cpu()
    """
    cpu_percent = psutil.cpu_percent(interval=None, percpu=False)

    if initialized:
        dash_stats['cpu_system'].append(cpu_percent)

    return cpu_percent


def update_gpu():
    """
    Update dashboard stats for system GPU usage.

    This will create new keys for the ``dash_stats`` dictionary if required, and then append a new value to the
    appropriate list.

    Nvidia GPUs are fully supported. AMD GPUs are currently only supported on Linux.

    Examples
    --------
    >>> update_gpu()
    """
    global nvidia_gpus
    nvidia_gpus = GPUtil.getGPUs()  # need to get the GPUs again otherwise the load does not update

    for gpu in nvidia_gpus:
        name = f'{gpu.name}-{gpu.id}'

        if initialized:
            try:
                dash_stats[f'gpu_{name}']
            except KeyError:
                dash_stats[f'gpu_{name}'] = []
            finally:
                gpu_load = 100 if gpu.load > 1 else gpu.load * 100  # convert decimal to percentage, max of 100
                dash_stats[f'gpu_{name}'].append(gpu_load)

    # this is untested
    amd_counter = 0
    while amd_counter < amd_gpus:
        gpu = pyamdgpuinfo.get_gpu(amd_counter)

        name = f'{gpu.name}-{gpu.gpu_id}'

        if initialized:
            try:
                dash_stats[f'gpu_{name}']
            except KeyError:
                dash_stats[f'gpu_{name}'] = []
            finally:
                gpu_load = 100 if gpu.query_load() > 100 else gpu.query_load()  # max of 100
                dash_stats[f'gpu_{name}'].append(gpu_load)

        amd_counter += 1


def update_memory():
    """
    Update dashboard stats for system memory usage.

    This will append a new value to the ``dash_stats['memory_system']`` list.

    Returns
    -------
    float
        The current system memory percentage utilized.

    Examples
    --------
    >>> update_memory()
    """
    memory_percent = psutil.virtual_memory().percent

    if initialized:
        dash_stats['memory_system'].append(memory_percent)

    return memory_percent


def update_network():
    """
    Update dashboard stats for system network usage.

    This will append a new values to the ``dash_stats['network_received']`` and ``dash_stats['network_sent']``
    lists.

    Returns
    -------
    tuple
        A tuple of the received and sent values as a difference since the last update.

    Examples
    --------
    >>> update_network()
    """
    global initialized
    global network_recv_last
    global network_sent_last

    net_recv_current = psutil.net_io_counters().bytes_recv / 1000000  # convert bytes to mb
    net_sent_current = psutil.net_io_counters().bytes_sent / 1000000  # convert bytes to mb

    net_recv_diff = net_recv_current - network_recv_last
    net_sent_diff = net_sent_current - network_sent_last

    network_recv_last = net_recv_current
    network_sent_last = net_sent_current

    if initialized:
        dash_stats['network_received'].append(net_recv_diff)
        dash_stats['network_sent'].append(net_sent_diff)

    return net_recv_diff, net_sent_diff


def update():
    """
    Update all dashboard stats.

    This function updates the cpu and memory usage of this python process as well as subprocesses. Following that the
    system functions are called to update system cpu, gpu, memory, and network usage. Finally the keys in the
    ``dash_stats`` dictionary are cleaned up to only hold 120 values. This function is called once per second, so
    therefore there are 2 minutes worth of values in the dictionary.

    Examples
    --------
    >>> update()
    """
    global initialized

    current_timestamp = helpers.timestamp()

    if initialized:
        dash_stats['timestamp'].append(helpers.timestamp())

        dash_stats['relative_time'] = []
        for x in dash_stats['timestamp']:
            seconds_ago = current_timestamp - x
            dash_stats['relative_time'].append(seconds_ago)

        child_processes = proc.children(recursive=False)  # list all children processes

        for child in child_processes:
            if child not in processes:
                processes.append(child)

    for p in processes:
        # set the name
        proc_name = definitions.Names().name if p.pid == proc_id else p.name()

        # cpu stats per process
        proc_cpu_percent = None
        try:
            proc_cpu_percent = p.cpu_percent()  # get current value
        except psutil.NoSuchProcess:
            pass
        finally:
            if initialized:
                try:
                    dash_stats[f'cpu_{proc_name}']
                except KeyError:
                    dash_stats[f'cpu_{proc_name}'] = []
                finally:
                    dash_stats[f'cpu_{proc_name}'].append(proc_cpu_percent)  # append the current value to the list

        # memory stats per process
        proc_memory_percent = None
        try:
            proc_memory_percent = p.memory_percent(memtype='rss')  # get current value
        except psutil.NoSuchProcess:
            pass
        finally:
            if initialized:
                try:
                    dash_stats[f'memory_{proc_name}']
                except KeyError:
                    dash_stats[f'memory_{proc_name}'] = []
                finally:
                    dash_stats[f'memory_{proc_name}'].append(proc_memory_percent)  # append the current value to the list

    update_cpu()  # todo, need to investigate why this is sometimes lower than the individual process
    update_gpu()  # todo... AMD GPUs on non Linux... integrated GPUs... GPU stats for processes
    update_memory()
    update_network()  # todo... network stats for processes

    for key in dash_stats:
        dash_stats[key] = dash_stats[key][-history_length:]  # keep the first 2 minutes

    if not initialized:
        initialized = True


def chart_data() -> str:
    """
    Get chart data.

    Get the data from the ``dash_stats`` dictionary, formatted for use with ``plotly``.

    Returns
    -------
    str
        A list, formatted as a string, containing dictionaries.
        Each dictionary is a chart ready to use with ``plotly``.

    See Also
    --------
    pyra.webapp.callback_dashboard : A callback called by javascript to get this data.

    Examples
    --------
    >>> chart_data()
    '[{"data": [...], "layout": ..., "config": ..., {"data": ...]'
    """
    x = dash_stats['relative_time']

    graphs = []

    accepted_chart_types = chart_types()

    for chart in accepted_chart_types:

        data = []
        for key, value in dash_stats.items():
            if key.startswith(chart):
                y = value
                split_name = key.split(f'{chart}_', 1)[-1]

                try:  # try to get the name from the translation dictionary
                    name = chart_translations['general'][split_name]
                except KeyError:
                    name = split_name

                data.append(
                    dict(  # https://plotly.com/javascript/reference/scatter/
                        cliponaxis=False,
                        hoverinfo='y',
                        line=dict(
                            shape='spline',
                            smoothing=0.5,  # 0.75 is nice, but sometimes drops below the axis line
                            width=3.5,
                        ),
                        mode='lines+markers',
                        name=name,
                        textfont=dict(
                            family='Open Sans',
                        ),
                        type='scatter',
                        x=x,
                        y=y,
                    )
                )

        if data:
            graphs.append(
                dict(
                    data=data,
                    layout=dict(  # https://plotly.com/javascript/reference/layout/
                        autosize=True,  # makes chart responsive, works better than the responsive config option
                        font=dict(
                            color='FFF',
                            family='Open Sans',
                        ),
                        legend=dict(
                            orientation='h',
                        ),
                        margin=dict(
                            b=40,  # bottom
                            l=60,  # left
                            r=20,  # right
                            t=40,  # top
                        ),
                        meta=dict(
                            id=f'chart-{chart}',  # this must match the div id in the html template
                        ),
                        paper_bgcolor='#303030',
                        plot_bgcolor='#303030',
                        showlegend=True,
                        title=chart_translations[chart]['usage'],
                        uirevision=True,
                        xaxis=dict(
                            autorange='reversed',  # smaller number, right side
                            layer='below traces'
                        ),
                        yaxis=dict(
                            title=dict(
                                standoff=10,  # separation between title and axis lables
                                text=_('mb') if chart == 'network' else _('%'),
                            ),
                            rangemode='tozero',  # axis does not drop below zero
                            layer='below traces'
                        ),
                    ),
                    config=dict(
                        displayModeBar=False,
                        responsive=False,  # keep False, does not work properly when True with ajax calls
                    )
                )
            )

    graphs_json = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return graphs_json


def chart_types():
    """
    Get chart types.

    Get the type of charts supported by the system.

    Returns
    -------
    list
        A list containing the types of charts supported.

    Examples
    --------
    >>> chart_types()
    ['cpu', 'memory', 'network']

    >>> chart_types()
    ['cpu', 'gpu', 'memory', 'network']
    """
    chart_type_list = [
        'cpu',
        'memory',
        'network'
    ]

    if nvidia_gpus or amd_gpus:
        chart_type_list.insert(1, 'gpu')

    return chart_type_list
