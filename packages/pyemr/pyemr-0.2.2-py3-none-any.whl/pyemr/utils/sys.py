""" """
import os
import shutil
import socket
import sys
import time

import pexpect


def get_site_package_paths():
    """Returns the paths of the site packages.

    Example:

    Args:

    Returns:

    >>> site_package = get_site_package_paths()
        >>> assert len(site_package) > 0
        >>> assert min([path.endswith("site-packages") for path in site_package])
    """

    spks = []
    for path in sys.path:
        if path.endswith("site-packages"):
            if path not in spks:
                spks.append(path)

    return ",".join(spks)


def copy_and_overwrite(from_path, to_path):
    """

    Args:
      from_path:
      to_path:

    Returns:

    """
    if os.path.exists(to_path):
        shutil.rmtree(to_path)

    # os.makedirs(to_path, exist_ok=True)
    shutil.copytree(from_path, to_path)


def os_cmd(*args, **kwargs):
    """

    Args:
      *args:
      **kwargs:

    Returns:

    """

    args = " ".join(args)
    kwargs = " ".join(["-{k} {v}" for k, v in kwargs.items()])
    cmd = []
    if args:
        cmd.append(args)
    if kwargs:
        cmd.append(kwargs)

    cmd = " ".join(cmd)
    os.system(cmd)


def pexpect_terminate(p):
    """

    Args:
      p:

    Returns:

    """
    for i in range(5):
        if p.isalive():
            p.sendeof()

    time.sleep(1)
    if p.isalive():
        p.terminate()

    return True


def pipe_cmd(cmd, cwd=None):
    """

    Args:
      cmd:
      cwd:  (Default value = None)

    Returns:

    """

    if type(cmd) == list:
        cmd = " ".join(cmd)

    print(f"Running '{cmd}'")

    if cwd:
        p = pexpect.spawn(cmd, cwd=cwd)
    else:
        p = pexpect.spawn(cmd)
    p.interact()
    # print(' '.join(cmd))
    # run(' '.join(cmd))

    pexpect_terminate(p)


def is_port_in_use(port: int):
    """

    Args:
      port: int:

    Returns:

    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0
