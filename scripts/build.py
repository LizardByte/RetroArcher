"""
scripts/build.py

Creates spec and builds binaries for RetroArcher.
"""
# standard imports
import sys

# lib imports
import PyInstaller.__main__


def build():
    """Sets arguments for pyinstaller, creates spec, and builds binaries."""
    pyinstaller_args = [
        './src/retroarcher.py',
        '--onefile',
        '--noconfirm',
        '--paths=./',
        '--add-data=docs:docs',
        '--add-data=web:web',
        '--add-data=locale:locale',
        '--icon=./web/images/favicon.ico'
    ]

    if sys.platform.lower() == 'win32':  # windows
        pyinstaller_args.append('--console')
        pyinstaller_args.append('--splash=./web/images/logo-circle.png')

        # fix args for windows
        for index, arg in enumerate(pyinstaller_args):
            pyinstaller_args[index] = arg.replace(':', ';')
    elif sys.platform.lower() == 'darwin':  # macOS
        pyinstaller_args.append('--console')
        pyinstaller_args.append('--osx-bundle-identifier=dev.lizardbyte.retroarcher')

    elif sys.platform.lower() == 'linux':  # linux
        pyinstaller_args.append('--splash=./web/images/logo-circle.png')

    PyInstaller.__main__.run(pyinstaller_args)


if __name__ == '__main__':
    build()
