"""install_test_dependencies.py

This is not intended to be run by the end user, but only to supplement the `python_tests.yml` github action.
"""

# standard imports
import subprocess
import sys

platform = sys.platform.lower()


def main():
    """main function"""
    if platform == 'darwin':
        pass

    elif platform == 'linux':
        packages = ['libappindicator1']

        subprocess.run(['apt-get', 'install', '-y'] + packages, stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                       text=True)

    elif platform == 'win32':
        pass


if __name__ == '__main__':
    main()
