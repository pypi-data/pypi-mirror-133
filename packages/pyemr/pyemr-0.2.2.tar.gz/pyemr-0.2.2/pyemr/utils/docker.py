"""A collection of aws tools"""
import os
import subprocess
from pathlib import Path

from pyemr.utils.sys import is_port_in_use, pipe_cmd

from .config import cprint, get_config_attr, get_package_dir, SH_DIR



AMAZON_LINUX_DOCKER_TAG = "pyemr/amazonlinux:latest"
AMAZON_LINUX_DOCKER_FILE = "files/docker/amazonlinux.spark{spark_version}.Dockerfile"


def launch_docker_shell():
    """Launch the docker shell."""
    docker_build(AMAZON_LINUX_DOCKER_FILE, AMAZON_LINUX_DOCKER_TAG)

    cwd = os.getcwd()
    docker_run_sh(cwd, "", it=True)


def launch_docker_bash():
    """Launches the docker bash."""
    docker_build(AMAZON_LINUX_DOCKER_FILE, AMAZON_LINUX_DOCKER_TAG)

    docker_run_sh(os.getcwd(), "", it=True, entry_point="bash")


def local_spark_submit(script):
    """Run the spark submit from inside docker.

    Args:
      script:

    Returns:

    """
    docker_build(AMAZON_LINUX_DOCKER_FILE, AMAZON_LINUX_DOCKER_TAG)
    docker_run_sh(
        os.getcwd(),
        f"/pyemr/{SH_DIR}/spark_submit.sh {script}",
        it=True,
        p="8889:8889",
    )


def is_docker_build(tag_name):
    """Checks if the docker image is built.

    Args:
      tag_name:

    Returns:
      bool: Returns true if docker is built.

    """
    try:
        subprocess.check_output(["docker", "inspect", "--type=image", tag_name])
        return True
    except subprocess.CalledProcessError as e:
        return False


def docker_build(
    dockerfile: str = AMAZON_LINUX_DOCKER_FILE,
    tag_name=AMAZON_LINUX_DOCKER_TAG,
):
    """Build the docker file.

    Args:
      dockerfile: str:  (Default value = AMAZON_LINUX_DOCKER_FILE)
      tag_name:  (Default value = AMAZON_LINUX_DOCKER_TAG)

    Returns:

    """
    project_dir = get_package_dir()
    print("project_dir", project_dir)

    if "{spark_version}" in dockerfile:
        spark_version = get_config_attr("spark_version")
        dockerfile = dockerfile.format(spark_version=spark_version)

    if not os.path.isfile(f"{project_dir}/{dockerfile}"):
        raise ValueError(
            f"No docker image found for spark {spark_version}. Create a new docker file called '{project_dir}/{dockerfile}'.",
        )

    print(f"Building emr docker image '{dockerfile}'...")

    if is_docker_build(tag_name) == False:
        cprint(
            f"WARNING:This is the first time you using pyemr or '{dockerfile}'. It might take ~5 minutes.",
        )

    cmd = ["docker", "build", "-t", tag_name, "--file", dockerfile, "."]
    pipe_cmd(cmd, cwd=project_dir)


def docker_build_run(cmd):
    """

    Args:
      cmd:

    Returns:

    """
    docker_build(AMAZON_LINUX_DOCKER_FILE, AMAZON_LINUX_DOCKER_TAG)
    docker_run_sh(
        os.getcwd(),
        cmd,
        it=True,
    )


def docker_run_sh(
    mount_dir,
    sh_cmd="",
    it=False,
    p="8889:8889",
    entry_point="sh",
    tag_name=AMAZON_LINUX_DOCKER_TAG,
):
    """Runs sh from the docker file.

    Args:
      tag_name: (Default value = AMAZON_LINUX_DOCKER_TAG)
      mount_dir:
      sh_cmd: (Default value = '')
      it: (Default value = False)
      p: (Default value = None)
      entry_point: (Default value = 'sh')

    Returns:

    """
    if p:
        out_port = int(p.split(":")[-1])
        if is_port_in_use(out_port):
            raise ValueError(
                f"Port {out_port} is already in use. Do you have pyemr container already running? Try 'docker container list', then 'docker stop'.",
            )

    home = str(Path.home())
    pwd_mount = f'src="{mount_dir}",target=/app,type=bind'
    aws_mount = f"src={home}/.aws/credentials,target=/root/.aws/credentials,type=bind"
    cmd = ["docker", "run", "--mount", pwd_mount, "--mount", aws_mount]
    if it:
        cmd.append("-it")

    if p is not None:
        cmd += ["-p", p]

    cmd += [tag_name, entry_point, sh_cmd]
    pipe_cmd(cmd)
