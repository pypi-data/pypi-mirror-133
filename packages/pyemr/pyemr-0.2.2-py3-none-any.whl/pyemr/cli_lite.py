# pylint: disable=R0201
"""Command Line Interface"""

import argparse
import sys


def inherit_site_packages(*args, **kwargs):
    """append additional site packages, using pure python

    Args:
      *args:
      **kwargs:

    Returns:

    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--additional_site_package_paths",
        type=str,
        help="Site packages to pass to pass to the enviroment.",
        default="",
    )
    args, unknown = parser.parse_known_args()
    site_packages = args.additional_site_package_paths.strip().split(",")
    for path in site_packages:
        if path not in sys.path:
            sys.path.append(path)


class Cli:
    """Command line interface for the package."""

    def notebook(self, env="venv"):
        """Runs docker notebooks with s3 patch.

        Args:
          env: str:  (Default value = 'docker')

        Returns:

        """

        from pyemr.utils.notebook import (
            run_notebook_in_poetry, run_notebook_on_sys,
        )

        if env in ["os", "local", "sys"]:
            run_notebook_on_sys()

        if env in ["poetry", "venv"]:
            run_notebook_in_poetry()

    def python(self, env="venv", *args, **kwargs):
        """Runs interactive docker python session with s3 patch.

        Args:
          env: str:  (Default value = 'docker')
          *args:
          **kwargs:

        Returns:

        """
        from pyemr.utils.python import (
            launch_mock_python_sys, launch_mock_python_venv,
        )

        if env in ["os", "local", "sys"]:
            launch_mock_python_sys()

        if env in ["poetry", "venv"]:
            launch_mock_python_venv()

    def test(self, script, env="venv", *args, **kwargs):
        """Run a script locally with s3 patch.

        Args:
          script:
          *args:
          **kwargs:
          env: (Default value = 'venv')

        Returns:

        """
        from pyemr.utils.testing import (
            test_script_with_s3_mock_sys, test_script_with_s3_mock_venv,
        )

        if "site_package_paths" in kwargs:
            kwargs.pop("additional_site_package_paths")

        if env in ["os", "local", "sys"]:
            test_script_with_s3_mock_sys(script, *args, **kwargs)

        if env in ["poetry", "venv"]:
            test_script_with_s3_mock_venv(script, *args, **kwargs)


def main():
    """ """
    inherit_site_packages()
    import fire

    fire.Fire(Cli)


if __name__ == "__main__":
    main()
