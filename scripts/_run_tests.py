"""_run_tests.py

This is not intended to be run by the end user, but only to supplement the `python_tests.yml` github action.
"""
# standard imports
import os
import subprocess
import sys
import time

platform = sys.platform.lower()

exit_code = 0


def cmd_daemon(cmd: list) -> subprocess.Popen:
    """Popen cmd in subprocess and continue

    :param cmd list - list of arguments for the command
    """
    proc = subprocess.Popen(args=cmd)
    return proc


def cmd_popen_print(cmd: list):
    """Popen cmd in subprocess and print the output, line by line.

    :param cmd list - list of arguments for the command
    :raises subprocess.CalledProcessError
    """
    proc = subprocess.Popen(args=cmd, stdout=sys.stdout, stderr=sys.stderr, text=True)

    proc.communicate()

    if proc.returncode != 0:
        global exit_code
        exit_code = proc.returncode

        raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)

    proc.kill()


def cmd_check(cmd: list):
    """Check_call cmd in subprocess and continue

    :param cmd list - list of arguments for the command
    """
    subprocess.check_call(args=cmd, stdout=sys.stdout, stderr=sys.stderr)


def main():
    """main function"""
    pre_commands()

    proc = daemon_commands()

    pytest_command()

    try:
        proc.kill()  # kill the running process
    except Exception:
        pass

    sys.exit(exit_code)


def pre_commands():
    """Run pre commands

    Use this to install dependencies, compile translations, etc.
    """
    if platform == 'darwin':
        pass

    elif platform == 'linux':
        update_cmd = ['sudo', 'apt-get', 'update']
        cmd_popen_print(cmd=update_cmd)
        # cmd_check(cmd=update_cmd)

        cmd = ['sudo', 'apt-get', 'install', '-y']

        packages = [
            'ubuntu-desktop',
            'xserver-xorg-video-dummy'
        ]

        for package in packages:
            cmd.append(package)

    elif platform == 'win32':
        pass

    try:
        cmd_popen_print(cmd=cmd)
        # cmd_check(cmd=cmd)
    except NameError:
        pass

    compile_cmd = [sys.executable, './scripts/_locale.py', '--compile']
    cmd_check(cmd=compile_cmd)


def daemon_commands():
    """Run daemon commands

    This will run after pre_commands and is intended to run anything that will continue running during pytest.
    """
    if platform == 'darwin':
        pass

    elif platform == 'linux':
        dummy_conf = """Section "Monitor"
  Identifier "Monitor0"
  HorizSync 28.0-80.0
  VertRefresh 48.0-75.0
  # https://arachnoid.com/modelines/
  # 1920x1080 @ 60.00 Hz (GTF) hsync: 67.08 kHz; pclk: 172.80 MHz
  Modeline "1920x1080_60.00" 172.80 1920 2040 2248 2576 1080 1081 1084 1118 -HSync +Vsync
EndSection

Section "Device"
  Identifier "Card0"
  Driver "dummy"
  VideoRam 256000
EndSection

Section "Screen"
  DefaultDepth 24
  Identifier "Screen0"
  Device "Card0"
  Monitor "Monitor0"
  SubSection "Display"
    Depth 24
    Modes "1920x1080_60.00"
  EndSubSection
EndSection
        """

        with open(file='dummy-1920x1080.conf', mode='w') as f:
            f.write(dummy_conf)

        cmd = ['sudo', 'X', '-config', 'dummy-1920x1080.conf']

        os.environ['DISPLAY'] = ':0'  # set the DISPLAY environment variable

    elif platform == 'win32':
        pass

    time.sleep(5)  # wait 5 seconds

    try:
        return cmd_daemon(cmd=cmd)
    except NameError:
        return False


def pytest_command():
    """Run the pytest command"""
    cmd = [sys.executable, '-m', 'pytest', '-v']
    cmd_popen_print(cmd=cmd)
    # cmd_check(cmd=cmd)


if __name__ == '__main__':
    main()
