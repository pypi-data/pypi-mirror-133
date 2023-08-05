""" """
import importlib.util
import os
import sys

from pyemr.utils.mocking import patch_pyspark
from pyemr.utils.sys import get_site_package_paths, pipe_cmd


@patch_pyspark
def test_script_with_s3_mock_sys(script, *args, **kwargs):
    """

    Args:
      script:
      *args:
      **kwargs:

    Returns:

    """
    tmp_argv_path = sys.argv.copy()

    new_argv = [script]
    if args:
        new_argv += args

    for key, value in kwargs.items():
        new_argv.append(f"--{key}")
        new_argv.append(value)

    sys.argv = new_argv

    spec = importlib.util.spec_from_file_location("__main__", script)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)

    sys.argv = tmp_argv_path


def test_script_with_s3_mock_venv(script, *args, **kwargs):
    """

    Args:
      script:
      *args:
      **kwargs:

    Returns:

    """

    if not os.path.exists("pyproject.toml"):
        test_script_with_s3_mock_sys(script, *args, **kwargs)
        return True
    else:
        from pyemr.utils.poetry import install_pyemr_in_poetry_env

        install_pyemr_in_poetry_env()
        # get the current sessions site packages
        site_pkg_paths = get_site_package_paths()

        pipe_cmd("poetry install")
        cmd = ["poetry", "run", "python", "-m", "pyemr.cli_lite", "test", script]

        args = [f"{a}" for a in args]
        args = " ".join(args)
        kwargs = {f"--{k}={v}" for k, v in kwargs.items()}

        if args:
            cmd += [args]

        if kwargs:
            cmd += [kwargs]

        cmd += ["--env=sys", f"--additional_site_package_paths={site_pkg_paths}"]
        cmd = " ".join(cmd)
        pipe_cmd(cmd)


def test_script_with_s3_mock_docker(script, *args, **kwargs):
    """Test the python script inside the docker container, using s3 mock.

    Args:
      *args:
      **kwargs:
      script:

    Returns:

    """
    from pyemr.utils.docker import SH_DIR, docker_build_run

    # args = " ".join([f'a' for a in args ])
    # kwargs = " ".join([f"--{k} {v}" for k, v in kwargs.items()])
    args = " ".join(sys.argv[2:])
    print(f"Running: f'{SH_DIR}/test_script.sh {args}'")
    docker_build_run(f"{SH_DIR}/test_script.sh {args}")
