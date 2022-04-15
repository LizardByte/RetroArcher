"""
..
   locales.py

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
    """
    Get a dictionary of all possible locales for use with babel.

    Dictionary keys will be `locale_id` and value with be `locale_display_name`.
    This is a shortened example of the returned value.

    .. code-block:: python

        {
          'de': 'Deutsch',
          'en': 'English',
          'en_GB': 'English (United Kingdom)',
          'en_US': 'English (United States)',
          'es': 'español',
          'fr': 'français',
          'it': 'italiano',
          'ru': 'русский'
        }

    Returns
    -------
    dict
        Dictionary of all possible locales.

    Examples
    --------
    >>> get_all_locales()
    {... 'en': 'English', ... 'en_GB': 'English (United Kingdom)', ... 'es': 'español', ... 'fr': 'français', ...}
    """
    log.debug(msg='Getting locale dictionary.')
    locale_ids = localedata.locale_identifiers()

    locales = {}

    for locale_id in locale_ids:
        locale = babel.Locale.parse(identifier=locale_id)
        locales[locale_id] = locale.get_display_name()

    return locales


def get_locale() -> str:
    """
    Verify the locale.

    Verify the locale from the config against supported locales and returns appropriate locale.

    Returns
    -------
    str
        The locale set in the config if it is valid, otherwise the default locale (en).

    Examples
    --------
    >>> get_locale()
    'en'
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
    """
    Install the language defined in the conifg.

    This function installs the language defined in the config and allows translations in python code.

    Returns
    -------
    gettext.gettext
        The `gettext.gettext` method.

    Examples
    --------
    >>> get_text()
    <bound method GNUTranslations.gettext of <gettext.GNUTranslations object at 0x...>>
    """
    language = gettext.translation(
        domain=default_domain,
        localedir=Paths().LOCALE_DIR,
        languages=[get_locale()]
    )

    language.install()

    return language.gettext
