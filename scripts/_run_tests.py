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

    proc.terminate()  # ask nicely
    time.sleep(5)  # wait
    proc.kill()  # don't ask


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

        packages = [
            'libappindicator3-1',
            'ubuntu-desktop',
            'xserver-xorg-video-dummy'
        ]

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


def run_commands():
    """Run commands

    This will run after pre_commands.
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
        proc = subprocess.Popen(args=cmd)
    except NameError:
        pass

    # run pytest
    cmd = [sys.executable, '-m', 'pytest', '-v']
    cmd_popen_print(cmd=cmd)

    try:
        outs, errs = proc.communicate(timeout=5)
    except NameError:
        return
    except subprocess.TimeoutExpired:
        proc.kill()
        outs, errs = proc.communicate()
    finally:
        # proc.terminate()  # ask nicely
        # time.sleep(5)  # wait
        # proc.kill()  # don't ask
        print(f'proc stdout: {outs}')
        print(f'proc stderr: {errs}')


def main():
    """main function"""
    pre_commands()

    run_commands()

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
