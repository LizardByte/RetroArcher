"""webapp.py

Responsible for serving the webapp.
"""
# standard imports
import os

# lib imports
from flask import Flask
from flask import render_template, send_from_directory
from flask_babel import Babel

# local imports
from pyra import config
from pyra.definitions import Paths
from pyra import logger

default_locale = 'en'
default_timezone = 'UTC'

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
    default_locale=default_locale,
    default_timezone=default_timezone,
    default_domain='retroarcher',
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
    """Verifies the locale from the config against supported locales and returns appropriate locale.

    :return: str
    """
    supported_locales = ['en', 'es']
    try:
        config_locale = config.CONFIG['General']['LOCALE']
    except TypeError:
        config_locale = None

    if config_locale in supported_locales:
        return config_locale
    else:
        return default_locale


@app.route('/')
@app.route('/home')
def home() -> render_template:
    """Serves the webapp home page

    :route '/'
    :route '/home'
    :return render_template
    """
    return render_template('home.html', title='Home')


@app.route('/favicon.ico')
def favicon() -> send_from_directory:
    """Serves the webapp favicon.ico file.

    :route '/favicon.ico'
    :return send_from_directory
    """
    return send_from_directory(directory=os.path.join(app.static_folder, 'images'),
                               path='retroarcher.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/test_logger')
def test_logger() -> str:
    """Test logging functions.

    Check `./logs/pyra.webapp.log` for output.

    :return str
    """
    app.logger.info('testing from app.logger')
    app.logger.warn('testing from app.logger')
    app.logger.error('testing from app.logger')
    app.logger.critical('testing from app.logger')
    app.logger.debug('testing from app.logger')
    return f'Testing complete, check "logs/{__name__}.log" for output.'
