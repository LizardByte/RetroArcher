"""_run_tests.py

This is not intended to be run by the end user, but only to supplement the `python_tests.yml` github action.
"""
# standard imports
import os
import subprocess
import sys
import time

platform = sys.platform.lower()

running_processes = []


def cmd_daemon(cmd: list):
    """Popen cmd in subprocess and continue

    :param cmd list - list of arguments for the command
    """
    proc = subprocess.Popen(args=cmd)

    running_processes.append(proc)


def cmd_popen_print(cmd: list):
    """Popen cmd in subprocess and print the output, line by line.

    :param cmd list - list of arguments for the command
    :raises subprocess.CalledProcessError
    """
    with subprocess.Popen(args=cmd, stdout=subprocess.PIPE, text=True) as proc:
        for line in proc.stdout:
            print(line, end='')  # process line here

    if proc.returncode != 0:
        raise subprocess.CalledProcessError(returncode=proc.returncode, cmd=proc.args)


def cmd_run(cmd: list):
    """Run cmd in subprocess and continue

    :param cmd list - list of arguments for the command
    """
    result = subprocess.run(args=cmd, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)


def main():
    """main function"""
    pre_commands()

    daemon_commands()

    pytest_command()

    for proc in running_processes:  # terminate still running processes
        proc.terminate()


def pre_commands():
    """Run pre commands

    Use this to install dependencies, compile translations, etc.
    """
    if platform == 'darwin':
        pass

    elif platform == 'linux':
        update_cmd = ['sudo', 'apt-get', 'update']
        cmd_popen_print(cmd=update_cmd)

        cmd = ['sudo', 'apt-get', 'install', '-y']

        packages = ['libappindicator1', 'xserver-xorg-video-dummy']

        for package in packages:
            cmd.append(package)

    elif platform == 'win32':
        pass

    try:
        cmd_popen_print(cmd=cmd)
    except NameError:
        pass

    compile_cmd = [sys.executable, './scripts/_locale.py', '--compile']
    cmd_popen_print(cmd=compile_cmd)


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
        os.environ['XAUTHORITY'] = '~/.Xauthority'  # https://unix.stackexchange.com/a/118826/397626

    elif platform == 'win32':
        pass

    try:
        cmd_daemon(cmd=cmd)
    except NameError:
        pass

    time.sleep(5)  # wait 5 seconds


def pytest_command():
    """Run the pytest command"""
    cmd = [sys.executable, '-m', 'pytest', '-v']
    cmd_popen_print(cmd=cmd)


if __name__ == '__main__':
    main()
