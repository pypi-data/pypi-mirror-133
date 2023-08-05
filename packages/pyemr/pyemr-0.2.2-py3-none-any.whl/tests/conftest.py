import os
import shutil
import time
import uuid
from io import StringIO

import fire
import pexpect
import pytest

from pyemr.cli import Cli
import sys
from contextlib import contextmanager


cwd = os.getcwd()


def pytest_addoption(parser):
    """

    Args:
      parser:

    Returns:

    """
    parser.addoption("--cluster_name", action="store", default=None)
    parser.addoption("--s3_parquet_file", action="store", default=None)
    parser.addoption("--s3_stage_dir", action="store", default=None)
    parser.addoption("--region", action="store", default="eu-west-1")


@pytest.fixture()
def cluster_name(pytestconfig):
    """

    Args:
      pytestconfig:

    Returns:

    """
    return pytestconfig.getoption("cluster_name")


@pytest.fixture()
def s3_parquet_file(pytestconfig):
    """

    Args:
      pytestconfig:

    Returns:

    """
    return pytestconfig.getoption("s3_parquet_file")


@pytest.fixture()
def region(pytestconfig):
    """

    Args:
      pytestconfig:

    Returns:

    """
    return pytestconfig.getoption("region")


@pytest.fixture()
def s3_stage_dir(pytestconfig):
    """

    Args:
      pytestconfig:

    Returns:

    """
    return pytestconfig.getoption("s3_stage_dir")




@pytest.fixture()
def copy_to_tmp(tmp_path):
    """

    Args:
      tmp_path:

    Returns:

    """

    def runner(file_name):
        """

        Args:
          file_name:

        Returns:

        """
        print(f"tmp_path : {tmp_path}")
        os.chdir(tmp_path)
        in_path = f"{cwd}/tests/scripts/{file_name}"
        shutil.copyfile(in_path, f"{tmp_path}/{file_name}")

    return runner


@pytest.fixture()
def script_dir():
    """ """
    return f"{cwd}/tests/scripts"


@pytest.fixture()
def uid():
    """ """
    uid = str(uuid.uuid4())[:8]
    return uid



def _terminate(p):
    """

    Args:
      p:

    Returns:

    """
    time.sleep(1)
    for i in range(5):
        if p.isalive():
            p.sendeof()

    time.sleep(1)
    if p.isalive():
        p.terminate()

    return True


def _expect(p, pattern):
    
    while True:
        line = p.readline().decode()
        if line.endswith("\n"):
            line = line[:-1]
        
        print(line)
        if pattern in line:
            break
    
    



@pytest.fixture()
def tmp_chdir(tmp_path):
    print(f"tmp_path:{tmp_path}")
    os.chdir(tmp_path)
    return tmp_path


def expect_send(p):
    
    def ifthen_(if_pattern, then_cmd=None):
        try:
            p.expect([if_pattern] )
            print(p.before.decode('utf-8', 'ignore'))
                  
            if then_cmd and type(then_cmd) == str:
                p.sendline(then_cmd)
            
            if then_cmd and type(then_cmd) == list:
                for line in then_cmd:
                    p.sendline(line)
            
            return True
        except:
            _terminate(p)
            raise
    
    return ifthen_


@pytest.fixture
def pexpect2():
    
    @contextmanager
    def spawn2(cmd, timeout=40):
        print(f'spawning:{cmd}')
        try:
            p = pexpect.spawn(cmd,timeout=timeout)
            yield expect_send(p)
        except:
            _terminate(p)
            raise
        finally:
            _terminate(p)
    
    return spawn2



@pytest.fixture()
def readscript(script_dir):
    
    def readscript_(script_name):
        with open(f"{script_dir}/{script_name}") as f:
            return f.read()
    
    return readscript_




