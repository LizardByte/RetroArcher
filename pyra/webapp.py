"""
..
   webapp.py

Responsible for serving the webapp.
"""
# standard imports
import os
from typing import Optional

# lib imports
from flask import Flask, Response
from flask import jsonify, render_template, request, send_from_directory
from flask_babel import Babel

# local imports
import pyra
from pyra import config
from pyra import hardware
from pyra.definitions import Paths
from pyra import locales
from pyra import logger

# localization
_ = locales.get_text()

# setup flask app
app = Flask(
    import_name=__name__,
    root_path=os.path.join(Paths.ROOT_DIR, 'web'),
    static_folder=os.path.join(Paths.ROOT_DIR, 'web'),
    template_folder=os.path.join(Paths.ROOT_DIR, 'web', 'templates')
    )

# remove extra lines rendered jinja templates
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# add python builtins to jinja templates
jinja_functions = dict(
    int=int,
    str=str,
)
app.jinja_env.globals.update(jinja_functions)

# localization
babel = Babel(
    app=app,
    default_locale=locales.default_locale,
    default_timezone=locales.default_timezone,
    default_translation_directories=Paths.LOCALE_DIR,
    default_domain=locales.default_domain,
    configure_jinja=True,
    locale_selector=locales.get_locale
)

# setup logging for flask
log_handlers = logger.get_logger(name=__name__).handlers

for handler in log_handlers:
    app.logger.addHandler(handler)


@app.route('/')
@app.route('/home')
def home() -> render_template:
    """
    Serve the webapp home page.

    .. todo:: This documentation needs to be improved.

    Returns
    -------
    render_template
        The rendered page.

    Notes
    -----
    The following routes trigger this function.

        `/`
        `/home`

    Examples
    --------
    >>> home()
    """
    chart_types = hardware.chart_types()
    chart_translations = hardware.chart_translations

    return render_template('home.html', title=_('Home'), chart_types=chart_types, translations=chart_translations)


@app.route('/callback/dashboard', methods=['GET'])
def callback_dashboard() -> Response:
    """
    Get dashboard data.

    This should be used in a callback in order to update charts in the web app.

    Returns
    -------
    Response
        A response formatted as ``flask.jsonify``.

    See Also
    --------
    pyra.hardware.chart_data : This function sets up the data in the proper format.

    Examples
    --------
    >>> callback_dashboard()
    <Response ... bytes [200 OK]>
    """
    graphs = hardware.chart_data()

    data = jsonify(graphs)

    return data


@app.route('/settings/', defaults={'configuration_spec': None})
@app.route('/settings/<path:configuration_spec>')
def settings(configuration_spec: Optional[str]) -> render_template:
    """
    Serve the configuration page page.

    .. todo:: This documentation needs to be improved.

    Parameters
    ----------
    configuration_spec : Optional[str]
        The spec to return. In the future this will be used to return config specs of plugins; however that is not
        currently implemented.

    Returns
    -------
    render_template
        The rendered page.

    Notes
    -----
    The following routes trigger this function.

        `/settings`

    Examples
    --------
    >>> settings()
    """
    config_settings = pyra.CONFIG

    if not configuration_spec:
        config_spec = config._CONFIG_SPEC_DICT
    else:
        # todo - handle plugin configs
        config_spec = None

    return render_template('config.html', title=_('Settings'), config_settings=config_settings, config_spec=config_spec)


@app.route('/docs/', defaults={'filename': 'index.html'})
@app.route('/docs/<path:filename>')
def docs(filename) -> send_from_directory:
    """
    Serve the Sphinx html documentation.

    .. todo:: This documentation needs to be improved.

    Parameters
    ----------
    filename : str
        The html filename to return.

    Returns
    -------
    flask.send_from_directory
        The requested documentation page.

    Notes
    -----
    The following routes trigger this function.

        `/docs/`
        `/docs/<page.html>`

    Examples
    --------
    >>> docs(filename='index.html')
    """

    return send_from_directory(directory=os.path.join(Paths.DOCS_DIR), path=filename)


@app.route('/favicon.ico')
def favicon() -> send_from_directory:
    """
    Serve the favicon.ico file.

    .. todo:: This documentation needs to be improved.

    Returns
    -------
    flask.send_from_directory
        The ico file.

    Notes
    -----
    The following routes trigger this function.

        `/favicon.ico`

    Examples
    --------
    >>> favicon()
    """
    return send_from_directory(directory=os.path.join(app.static_folder, 'images'),
                               path='retroarcher.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/status')
def status() -> dict:
    """
    Check the status of RetroArcher.

    This is useful for a healthcheck from Docker, and may have many other uses in the future for third party
    applications.

    Returns
    -------
    dict
        A dictionary of the status.

    Examples
    --------
    >>> status()
    """
    web_status = {'result': 'success', 'message': 'Ok'}
    return web_status


@app.route('/test_logger')
def test_logger() -> str:
    """
    Test logging functions.

    Check `./logs/pyra.webapp.log` for output.

    Returns
    -------
    str
        A message telling the user to check the logs.

    Notes
    -----
    The following routes trigger this function.

        `/test_logger`

    Examples
    --------
    >>> test_logger()
    """
    app.logger.info('testing from app.logger')
    app.logger.warning('testing from app.logger')
    app.logger.error('testing from app.logger')
    app.logger.critical('testing from app.logger')
    app.logger.debug('testing from app.logger')
    return f'Testing complete, check "logs/{__name__}.log" for output.'


@app.route('/api/settings', methods=['GET', 'POST'], defaults={'configuration_spec': None})
@app.route('/api/settings/<path:configuration_spec>')
def api_settings(configuration_spec: Optional[str]) -> Response:
    """
    Get current settings or save changes to settings from web ui.

    This endpoint accepts a `GET` or `POST` request. A `GET` request will return the current settings.
    A `POST` request will process the data passed in and return the results of processing.

    Parameters
    ----------
    configuration_spec : Optional[str]
        The spec to return. In the future this will be used to return config specs of plugins; however that is not
        currently implemented.

    Returns
    -------
    Response
        A response formatted as ``flask.jsonify``.

    Examples
    --------
    >>> callback_dashboard()
    <Response ... bytes [200 OK]>
    """
    if not configuration_spec:
        config_spec = config._CONFIG_SPEC_DICT
    else:
        # todo - handle plugin configs
        config_spec = None

    if request.method == 'GET':
        return config.CONFIG
    if request.method == 'POST':
        # setup return data
        message = ''  # this will be populated as we progress
        result_status = 'OK'

        boolean_dict = {
            'true': True,
            'false': False,
        }

        data = request.form
        for option, value in data.items():
            split_option = option.split('|', 1)
            key = split_option[0]
            setting = split_option[1]

            setting_type = config_spec[key][setting]['type']

            # get the original value
            try:
                og_value = config.CONFIG[key][setting]
            except KeyError:
                og_value = ''
            finally:
                if setting_type == 'boolean':
                    value = boolean_dict[value.lower()]  # using eval could allow code injection, so use dictionary
                if setting_type == 'float':
                    value = float(value)
                if setting_type == 'integer':
                    value = int(value)

            if og_value != value:
                # setting changed, get the on change command
                try:
                    setting_change_method = config_spec[key][setting]['on_change']
                except KeyError:
                    pass
                else:
                    setting_change_method()

            config.CONFIG[key][setting] = value

        valid = config.validate_config(config=config.CONFIG)

        if valid:
            message += 'Selected settings are valid.'
            config.save_config(config=config.CONFIG)

        else:
            message += 'Selected settings are not valid.'

        return jsonify({'status': f'{result_status}', 'message': f'{message}'})


def start_webapp():
    """
    Start the webapp.

    Start the flask webapp. This is placed in it's own function to allow the ability to start the webapp within a
    thread in a simple way.

    Examples
    --------
    >>> start_webapp()
     * Serving Flask app 'pyra.webapp' (lazy loading)
    ...
     * Running on http://.../ (Press CTRL+C to quit)

    >>> from pyra import webapp, threads
    >>> threads.run_in_thread(target=webapp.start_webapp, name='Flask', daemon=True).start()
     * Serving Flask app 'pyra.webapp' (lazy loading)
    ...
     * Running on http://.../ (Press CTRL+C to quit)
    """
    app.run(
        host=config.CONFIG['Network']['HTTP_HOST'],
        port=config.CONFIG['Network']['HTTP_PORT'],
        debug=pyra.DEV,
        use_reloader=False  # reloader doesn't work when running in a separate thread
    )
