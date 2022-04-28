"""
..
   webapp.py

Responsible for serving the webapp.
"""
# standard imports
import os

# lib imports
import flask
from flask import Flask
from flask import render_template, send_from_directory
from flask_babel import Babel

# local imports
import pyra
from pyra import config
from pyra import hardware
from pyra.definitions import Paths
from pyra import locales
from pyra import logger

# setup flask app
app = Flask(
    import_name=__name__,
    root_path=os.path.join(Paths().ROOT_DIR, 'web'),
    static_folder=os.path.join(Paths().ROOT_DIR, 'web'),
    template_folder=os.path.join(Paths().ROOT_DIR, 'web', 'templates')
    )


# remove extra lines rendered jinja templates
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# localization
babel = Babel(
    app=app,
    default_locale=locales.default_locale,
    default_timezone=locales.default_timezone,
    default_domain=locales.default_domain,
    configure_jinja=True,
)
# app.translation_directories(Paths().LOCALE_DIR)
app.config['BABEL_TRANSLATION_DIRECTORIES'] = Paths().LOCALE_DIR

# setup logging for flask
log_handlers = logger.get_logger(name=__name__).handlers

for handler in log_handlers:
    app.logger.addHandler(handler)


@babel.localeselector
def get_locale() -> str:
    """
    Get the locale from the config.

    Get the locale specified in the config. This does not need to be called as it is done so automatically by `babel`.

    Returns
    -------
    str
        The locale.

    See Also
    --------
    pyra.locales.get_locale : Use this function instead.

    Examples
    --------
    >>> get_locale()
    en
    """
    locale = locales.get_locale()
    return locale


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

    return render_template('home.html', title='Home', chart_types=chart_types, translations=chart_translations)


@app.route('/callback/dashboard', methods=['GET'])
def callback_dashboard() -> str:
    """
    Get dashboard data.

    This should be used in a callback in order to update charts in the web app.

    Returns
    -------
    str
        A list, formatted as a string, containing dictionaries.
        Each dictionary is a chart ready to use with ``plotly``.

    See Also
    --------
    pyra.hardware.chart_data : Returns the same data as this function.

    Examples
    --------
    >>> callback_dashboard()
    '[{"data": [...], "layout": ..., "config": ..., {"data": ...]'
    """
    data = hardware.chart_data()

    return data


@app.route('/docs/', defaults={'filename': 'index.html'})
@app.route('/docs/<path:filename>')
def docs(filename) -> flask.send_from_directory:
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

    return send_from_directory(directory=os.path.join(Paths().DOCS_DIR), path=filename)


@app.route('/favicon.ico')
def favicon() -> flask.send_from_directory:
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
    app.logger.warn('testing from app.logger')
    app.logger.error('testing from app.logger')
    app.logger.critical('testing from app.logger')
    app.logger.debug('testing from app.logger')
    return f'Testing complete, check "logs/{__name__}.log" for output.'


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

    >>> from pyra import threads
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
