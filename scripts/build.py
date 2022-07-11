"""
..
   build.py

Creates spec and builds binaries for RetroArcher.
"""
# standard imports
import sys

# lib imports
import PyInstaller.__main__


def build():
    """Sets arguments for pyinstaller, creates spec, and builds binaries."""
    pyinstaller_args = [
        'retroarcher.py',
        '--onefile',
        '--noconfirm',
        '--paths=./',
        '--add-data=docs:docs',
        '--add-data=web:web',
        '--add-data=locale:locale',
        '--icon=./web/images/retroarcher.ico'
    ]

    if sys.platform.lower() == 'win32':  # windows
        pyinstaller_args.append('--console')
        pyinstaller_args.append('--splash=./web/images/logo-circle.png')

        # fix args for windows
        arg_count = 0
        for arg in pyinstaller_args:
            pyinstaller_args[arg_count] = arg.replace(':', ';')
            arg_count += 1
    elif sys.platform.lower() == 'darwin':  # macOS
        pyinstaller_args.append('--console')
        pyinstaller_args.append('--osx-bundle-identifier=com.github.retroarcher.retroarcher')

    elif sys.platform.lower() == 'linux':  # linux
        pyinstaller_args.append('--splash=./web/images/logo-circle.png')

    PyInstaller.__main__.run(pyinstaller_args)


if __name__ == '__main__':
    build()
