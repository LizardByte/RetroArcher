import sys
import PyInstaller.__main__


def build():
    pyinstaller_args = [
        'retroarcher.py',
        '--onefile',
        '--noconfirm',
        '--paths=./',
        '--add-data=web:web',
        '--icon=./web/images/retroarcher.ico',
        '--splash=./web/images/logo-circle.png'
    ]

    if sys.platform.lower() == 'win32':  # windows
        pyinstaller_args.append('--console')

        # fix args for windows
        arg_count = 0
        for arg in pyinstaller_args:
            pyinstaller_args[arg_count] = arg.replace(':', ';')
            arg_count += 1
    elif sys.platform.lower() == 'darwin':  # macOS
        pyinstaller_args.append('--console')
        pyinstaller_args.append('--osx-bundle-identifier=com.github.retroarcher.retroarcher')

    elif sys.platform.lower() == 'linux':  # linux
        # todo
        pass

    PyInstaller.__main__.run(pyinstaller_args)


if __name__ == '__main__':
    build()
