"""
..
   locales.py

Functions related to localization.

Localization (also referred to as l10n) is the process of adapting a product or service to a specific locale.
Translation is only one of several elements in the localization process. In addition to translation, the localization
process may also include:
- Adapting design and layout to properly display translated text in the language of the locale
- Adapting sorting functions to the alphabetical order of a specific locale
- Changing formats for date and time, addresses, numbers, currencies, etc. for specific target locales
- Adapting graphics to suit the expectations and tastes of a target locale
- Modifying content to suit the tastes and consumption habits of a target locale

The aim of localization is to give a product or service the look and feel of having been created specifically for a
target market, no matter their language, cultural preferences, or location.
"""
# standard imports
import gettext
import os
import subprocess
import sys

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
    translation_fallback = False
    if not os.path.isfile(os.path.join(Paths.LOCALE_DIR, get_locale(), 'LC_MESSAGES', f'{default_domain}.mo')):
        log.warning(msg='No locale mo translation file found.')

        locale_script = os.path.join(Paths.ROOT_DIR, 'scripts', '_locale.py')

        if os.path.isfile(locale_script):
            log.info(msg='Running locale compile script.')
            # run python script in a subprocess
            subprocess.run(
                args=[sys.executable, locale_script, '--compile'],
                cwd=Paths.ROOT_DIR,
            )
        else:
            log.warning(msg='Locale compile script not found. Defaulting to English.')
            translation_fallback = True

    language = gettext.translation(
        domain=default_domain,
        localedir=Paths.LOCALE_DIR,
        languages=[get_locale()],
        fallback=translation_fallback,
    )

    language.install()

    return language.gettext
