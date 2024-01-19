"""
..
   hardware.py

Functions related to the dashboard viewer.
"""
# standard imports

# lib imports
import GPUtil
from numexpr import cpuinfo
import psutil

# local imports
from pyra import definitions
from pyra import helpers
from pyra import locales
from pyra import logger

try:
    cpu_name = cpuinfo.cpu.info[0]['ProcessorNameString'].strip()
except KeyError:
    cpu_name = None

_ = locales.get_text()
chart_translations = dict(
    cpu=dict(
        bare=_('cpu'),
        usage=_('cpu usage'),
        name=cpu_name
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
    import pyamdgpuinfo  # linux only
except ModuleNotFoundError:
    pyamdgpu = False
    try:
        from pyadl import ADLManager, ADLError
    except Exception:  # cannot import `ADLError` from `pyadl.pyadl`
        amd_gpus = range(0)  # no amd gpus found
    else:
        amd_gpus = ADLManager.getInstance().getDevices()  # list of AMD gpus
else:
    pyamdgpu = True
    amd_gpus = range(pyamdgpuinfo.detect_gpus())  # integer representing amd gpus count

dash_stats = dict(
    time=dict(
        timestamp=[],
        relative_time=[]
    ),
    cpu=dict(
        system=[]
    ),
    gpu=dict(),
    memory=dict(
        system=[]
    ),
    network=dict(
        sent=[],
        received=[]
    )
)

history_length = 120


def update_cpu() -> float:
    """
    Update dashboard stats for system CPU usage.

    This will append a new value to the ``dash_stats['cpu'][system']`` list.

    Returns
    -------
    float
        The current system cpu percentage utilized.

    Examples
    --------
    >>> update_cpu()
    """
    cpu_percent = min(float(100), psutil.cpu_percent(interval=None, percpu=False))  # max of 100

    if initialized:
        dash_stats['cpu']['system'].append(cpu_percent)

    return cpu_percent


def update_gpu():
    """
    Update dashboard stats for system GPU usage.

    This will create new keys for the ``dash_stats`` dictionary if required, and then append a new value to the
    appropriate list.

    AMD data is provided by `pyamdgpuinfo <https://github.com/mark9064/pyamdgpuinfo>`_ on Linux, and by
    `pyadl <https://github.com/nicolargo/pyadl>`_ on non Linux systems.
    Nvidia data is provided by `GPUtil <https://github.com/anderskm/gputil>`_.

    Examples
    --------
    >>> update_gpu()
    """
    global nvidia_gpus
    nvidia_gpus = GPUtil.getGPUs()  # need to get the GPUs again otherwise the load does not update

    gpu_types = [nvidia_gpus, amd_gpus]

    for gpu_type in gpu_types:  # loop through gpu types
        for gpu in gpu_type:  # loop through found gpus
            name = None
            gpu_load = None
            if gpu_type == nvidia_gpus:
                name = f'{gpu.name}-{gpu.id}'
                gpu_load = min(100, gpu.load * 100)  # convert decimal to percentage, max of 100
            elif gpu_type == amd_gpus:
                if pyamdgpu:
                    amd_gpu = pyamdgpuinfo.get_gpu(gpu)
                    name = f'{amd_gpu.name}-{amd_gpu.gpu_id}'
                    gpu_load = min(100, gpu.query_load())  # max of 100
                else:
                    name = f'{gpu.adapterName.decode("utf-8")}-{gpu.adapterIndex}'  # adapterName is bytes so decode it
                    try:
                        gpu_load = min(100, gpu.getCurrentUsage())  # max of 100
                    except ADLError:
                        gpu_load = None

            if initialized and name:
                try:
                    dash_stats['gpu'][name]
                except KeyError:
                    dash_stats['gpu'][name] = []
                finally:
                    dash_stats['gpu'][name].append(gpu_load)


def update_memory():
    """
    Update dashboard stats for system memory usage.

    This will append a new value to the ``dash_stats['memory']['system']`` list.

    Returns
    -------
    float
        The current system memory percentage utilized.

    Examples
    --------
    >>> update_memory()
    """
    memory_percent = min(100, psutil.virtual_memory().percent)  # max of 100

    if initialized:
        dash_stats['memory']['system'].append(memory_percent)

    return memory_percent


def update_network():
    """
    Update dashboard stats for system network usage.

    This will append a new values to the ``dash_stats['network']['received']`` and ``dash_stats['network']['sent']``
    lists.

    Returns
    -------
    tuple
        A tuple of the received and sent values as a difference since the last update.

    Examples
    --------
    >>> update_network()
    """
    global network_recv_last
    global network_sent_last

    network_stats = psutil.net_io_counters()

    # get the current values in mb
    network_received_current = network_stats.bytes_recv / 1e6  # convert bytes to mb
    network_sent_current = network_stats.bytes_sent / 1e6  # convert bytes to mb

    # compare the current values to the last values, as current values increase incrementally
    network_received_diff = network_received_current - network_recv_last
    network_sent_diff = network_sent_current - network_sent_last

    # rewrite the last value
    network_recv_last = network_received_current
    network_sent_last = network_sent_current

    if initialized:
        dash_stats['network']['received'].append(network_received_diff)
        dash_stats['network']['sent'].append(network_sent_diff)

    return network_received_diff, network_sent_diff


def update():
    """
    Update all dashboard stats.

    This function updates the cpu and memory usage of this python process as well as subprocesses. Following that the
    system functions are called to update system cpu, gpu, memory, and network usage. Finally, the keys in the
    ``dash_stats`` dictionary are cleaned up to only hold 120 values. This function is called once per second,
    therefore there are 2 minutes worth of values in the dictionary.

    Examples
    --------
    >>> update()
    """
    global initialized

    current_timestamp = helpers.timestamp()

    if initialized:
        dash_stats['time']['timestamp'].append(helpers.timestamp())

        dash_stats['time']['relative_time'] = []
        for x in dash_stats['time']['timestamp']:
            seconds_ago = current_timestamp - x
            dash_stats['time']['relative_time'].append(seconds_ago)

        child_processes = proc.children(recursive=False)  # list all children processes

        for child in child_processes:
            if child not in processes:
                processes.append(child)

    # find the indexes to remove from the lists
    time_index = 0
    last_tstamp = None
    for tstamp in dash_stats['time']['relative_time']:
        if tstamp <= history_length:
            if last_tstamp is not None:
                # ensures upper X axis label does not fall
                if tstamp < history_length < last_tstamp and time_index > 0:
                    time_index += -1
            break
        else:
            last_tstamp = tstamp
            time_index += 1

    # remove oldest list entries
    for stat_type, data in dash_stats.items():
        for key in data:
            data[key] = data[key][time_index:]  # keep the first 2 minutes

    for p in processes:
        # set the name
        proc_name = definitions.Names.name if p.pid == proc_id else p.name()

        # cpu stats per process
        proc_cpu_percent = None
        try:
            proc_cpu_percent = min(float(100), p.cpu_percent())  # get current value, max of 100
        except psutil.NoSuchProcess:
            pass
        finally:
            if initialized:
                try:
                    dash_stats['cpu'][proc_name]
                except KeyError:
                    dash_stats['cpu'][proc_name] = []
                finally:  # append the current value to the list
                    dash_stats['cpu'][proc_name].append(proc_cpu_percent)

        # memory stats per process
        proc_memory_percent = None
        try:
            proc_memory_percent = min(float(100), p.memory_percent(memtype='rss'))  # get current value, max of 100
        except psutil.NoSuchProcess:
            pass
        finally:
            if initialized:
                try:
                    dash_stats['memory'][proc_name]
                except KeyError:
                    dash_stats['memory'][proc_name] = []
                finally:  # append the current value to the list
                    dash_stats['memory'][proc_name].append(proc_memory_percent)

    update_cpu()  # todo, need to investigate why this is sometimes lower than the individual process
    update_gpu()  # todo... AMD GPUs on non Linux... integrated GPUs... GPU stats for processes
    update_memory()
    update_network()  # todo... network stats for processes

    if not initialized:
        initialized = True


def chart_data() -> dict:
    """
    Get chart data.

    Get the data from the ``dash_stats`` dictionary, formatted for use with ``plotly``.

    Returns
    -------
    dict
        A single key named 'graphs' contains a list of graphs. Each graph is formatted as a dictionary and ready to use
        with ``plotly``.

    See Also
    --------
    pyra.webapp.callback_dashboard : A callback called by javascript to get this data.

    Examples
    --------
    >>> chart_data()
    {'graphs': [{"data": [...], "layout": ..., "config": ..., {"data": ...]}
    """
    x = dash_stats['time']['relative_time']

    graphs = dict(graphs=[])

    accepted_chart_types = chart_types()

    # todo
    # currently disabled: https://github.com/plotly/plotly.js/issues/6012
    # x_ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]

    for chart in accepted_chart_types:

        if chart == 'network':
            # NOTE: Mbps = megabytes per second
            hover_template = _('%(numeric_value)s Mbps') % {'numeric_value': '%{y:.3f}'}
        else:
            # NOTE: the double percent symbols is rendered as one in this case
            hover_template = _('%(numeric_value)s %%') % {'numeric_value': '%{y:.2f}'}

        data = []
        for key, value in dash_stats[chart].items():
            y = value

            try:  # try to get the name from the translation dictionary
                name = chart_translations['general'][key]
            except KeyError:
                name = key

            data.append(
                dict(  # https://plotly.com/javascript/reference/scatter/
                    cliponaxis=False,
                    hovertemplate=hover_template,
                    line=dict(
                        shape='spline',
                        smoothing=0.8,  # 0.75 is nice, but sometimes drops below the axis line
                        width=3.5,
                    ),
                    mode='lines+markers' if len(x) < 30 else 'lines',
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
            graphs['graphs'].append(
                dict(
                    data=data,  # this is a list
                    layout=dict(  # https://plotly.com/javascript/reference/layout/
                        autosize=True,  # makes chart responsive, works better than the responsive config option
                        font=dict(
                            color='FFF',
                            family='Open Sans',
                        ),
                        hoverlabel=dict(
                            bgcolor='252525',
                        ),
                        hovermode='x unified',  # show all Y values on hover
                        legend=dict(
                            entrywidth=0,
                            entrywidthmode='pixels',
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
                            fixedrange=True,  # disable zoom of axis
                            layer='below traces',
                            showspikes=False,
                            # todo
                            # currently disabled: https://github.com/plotly/plotly.js/issues/6012
                            # does not display how I would like
                            # would like to show "x s ago" (localizable) on the hover label, but not in the axis
                            # tickmode='array',
                            # # NOTE: this exact moment in time
                            # ticktext=[_('NOW') if value == 0 else
                            #           # NOTE: s = seconds, i.e. "5 s"... do not change "%(numeric_value)s"
                            #           _('%(numeric_value)s s') % {'numeric_value': value} for value in x_ticks],
                            # tickvals=x_ticks
                        ),
                        yaxis=dict(
                            fixedrange=True,  # disable zoom of axis
                            layer='below traces',
                            # rangemode='tozero',  # axis does not drop below 0; however the line gets cut below 0
                            title=dict(
                                standoff=10,  # separation between title and axis labels
                                text=_('Mbps') if chart == 'network' else _('%'),
                            ),
                        ),
                    ),
                    config=dict(
                        displayModeBar=False,  # disable the modebar
                        editable=False,  # explicitly disable editing
                        responsive=False,  # keep False, does not work properly when True with ajax calls
                        scrollZoom=False  # explicitly disable mouse scroll zoom
                    )
                )
            )

    return graphs


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
