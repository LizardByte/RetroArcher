"""locales.py

Functions related to localization.
"""
# standard imports
import gettext

# lib imports
import babel
from babel import localedata

# local imports
from pyra import config
from pyra.definitions import Paths
from pyra import logger

default_domain = 'retroarcher'
default_locale = 'en'
default_timezone = 'UTC'
supported_locales = ['en', 'es']

log = logger.get_logger(__name__)


def get_all_locales() -> dict:
    """Function to get a dictionary of all possible locales for use with babel.

    Dictionary keys will be `locale_id` and value with be `locale_display_name`.
    This example is shortened.
    e.g.: {
              'de': 'Deutsch',
              'en': 'English',
              'en_GB': 'English (United Kingdom)',
              'en_US': 'English (United States)',
              'es': 'español',
              'fr': 'français',
              'it': 'italiano'
              'ru': 'русский'
          }

    :return: dict
    """
    log.debug(msg='Getting locale dictionary.')
    locale_ids = localedata.locale_identifiers()

    locales = {}

    for locale_id in locale_ids:
        locale = babel.Locale.parse(identifier=locale_id)
        locales[locale_id] = locale.get_display_name()

    return locales


def get_locale() -> str:
    """Verifies the locale from the config against supported locales and returns appropriate locale.

    :return: str
    """
    try:
        config_locale = config.CONFIG['General']['LOCALE']
    except TypeError:
        config_locale = None

    if config_locale in supported_locales:
        return config_locale
    else:
        return default_locale


def get_text() -> gettext.gettext:
    """Install the language defined in the conifg.

    :return gettext.gettext
    """
    language = gettext.translation(
        domain=default_domain,
        localedir=Paths().LOCALE_DIR,
        languages=[get_locale()]
    )

    language.install()

    return language.gettext
