"""install_test_dependencies.py

This is not intended to be run by the end user, but only to supplement the `python_tests.yml` github action.
"""
# standard imports
import subprocess
import sys

platform = sys.platform.lower()


def run_cmd(cmd: list):
    """Execute cmd in subprocess and print the output, line by line.

    :raises subprocess.CalledProcessError
    """
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True) as proc:
        for line in proc.stdout:
            print(line, end='')  # process line here

    if proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode, proc.args)


def main():
    """main function"""
    if platform == 'darwin':
        pass

    elif platform == 'linux':
        cmd = ['sudo', 'apt-get', 'install', '-y']

        packages = ['libappindicator1']

        for package in packages:
            cmd.append(package)

    elif platform == 'win32':
        pass

    try:
        run_cmd(cmd)
    except NameError:
        pass


if __name__ == '__main__':
    main()
