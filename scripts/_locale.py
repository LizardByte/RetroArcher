"""
..
   _locale.py

Functions related to building, initializing, updating, and compiling localization translations.
"""
# standard imports
import argparse
import os
import subprocess

project_name = 'RetroArcher'

script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(script_dir)
locale_dir = os.path.join(root_dir, 'locale')

# retroarcher target locales
target_locales = [
    'de',  # Deutsch
    'en',  # English
    'en_GB',  # English (United Kingdom)
    'en_US',  # English (United States)
    'es',  # español
    'fr',  # français
    'it',  # italiano
    'ru',  # русский
]


def babel_extract():
    """Executes `pybabel extract` in subprocess."""
    commands = [
        'pybabel',
        'extract',
        '-F', os.path.join(script_dir, 'babel.cfg'),
        '-o', os.path.join(locale_dir, f'{project_name.lower()}.po'),
        '--sort-by-file',
        f'--msgid-bugs-address=github.com/{project_name.lower()}',
        f'--copyright-holder={project_name}',
        f'--project={project_name}',
        '--version=v0',
        '--add-comments=NOTE',
        './retroarcher.py',
        './pyra',
        './web'
    ]

    print(commands)
    subprocess.check_output(args=commands, cwd=root_dir)


def babel_init(locale_code: str):
    """Executes `pybabel init` in subprocess.

    :param locale_code: str - locale code
    """
    commands = [
        'pybabel',
        'init',
        '-i', os.path.join(locale_dir, f'{project_name.lower()}.po'),
        '-d', locale_dir,
        '-D', project_name.lower(),
        '-l', locale_code
    ]

    print(commands)
    subprocess.check_output(args=commands, cwd=root_dir)


def babel_update():
    """Executes `pybabel update` in subprocess."""
    commands = [
        'pybabel',
        'update',
        '-i', os.path.join(locale_dir, f'{project_name.lower()}.po'),
        '-d', locale_dir,
        '-D', project_name.lower(),
        '--update-header-comment'
    ]

    print(commands)
    subprocess.check_output(args=commands, cwd=root_dir)


def babel_compile():
    """Executes `pybabel compile` in subprocess."""
    commands = [
        'pybabel',
        'compile',
        '-d', locale_dir,
        '-D', project_name.lower()
    ]

    print(commands)
    subprocess.check_output(args=commands, cwd=root_dir)


if __name__ == '__main__':
    # Set up and gather command line arguments
    parser = argparse.ArgumentParser(
        description='Script helps update locale translations. Translations must be done manually.')

    parser.add_argument('--extract', action='store_true', help='Extract messages from python files and templates.')
    parser.add_argument('--init', action='store_true', help='Initialize any new locales specified in target locales.')
    parser.add_argument('--update', action='store_true', help='Update existing locales.')
    parser.add_argument('--compile', action='store_true', help='Compile translated locales.')

    args = parser.parse_args()

    if args.extract:
        babel_extract()

    if args.init:
        for locale_id in target_locales:
            if not os.path.isdir(os.path.join(locale_dir, locale_id)):
                babel_init(locale_code=locale_id)

    if args.update:
        babel_update()

    if args.compile:
        babel_compile()
