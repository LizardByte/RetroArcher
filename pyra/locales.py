# lib imports
import babel

# local imports
from pyra import logger

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
    locale_ids = babel.localedata.locale_identifiers()

    locales = {}

    for locale_id in locale_ids:
        locale = babel.Locale.parse(identifier=locale_id)
        locales[locale_id] = locale.get_display_name()

    return locales


if __name__ == '__main__':
    all_locales = get_all_locales()
    print(all_locales)
