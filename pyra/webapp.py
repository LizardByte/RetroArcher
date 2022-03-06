"""webapp.py

Responsible for serving the webapp.
"""
# standard imports
import os

# lib imports
from flask import Flask
from flask import render_template, send_from_directory

# local imports
from pyra.definitions import Paths
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

# setup logging for flask
log_handlers = logger.get_logger(name=__name__).handlers

for handler in log_handlers:
    app.logger.addHandler(handler)


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
                               path='retroarcher.ico', filename='favicon.ico', mimetype='image/vnd.microsoft.icon')


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
