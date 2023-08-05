import os
import uuid
from pexpect import EOF
import pexpect

test_id = str(uuid.uuid4())


def test_init_param(tmp_chdir, pexpect2, uid):
    """

    Args:
      stdin:
      pyemr:

    Returns:

    """
    toml_path = "./pyproject.toml"
    assert not os.path.isfile(toml_path)
    
    with pexpect2(f"pyemr init {uid} {uid} {uid} {uid} {uid}") as ifthen:
        ifthen('spark_version', None)
    
    toml = open(toml_path).read()
    assert os.path.isfile(toml_path)
    assert f'name = "{uid}"' in toml
    assert f's3-staging-dir = "{uid}"' in toml



def test_pyemr_add(tmp_chdir, pexpect2, uid):
    """

    Args:
      tmp_path:
      monkeypatch:
      stdin:
      pyemr:
      cluster_name:

    Returns:

    """
    toml_path = "./pyproject.toml"
    assert not os.path.isfile(toml_path)

    with pexpect2(f"pyemr init") as ifthen:
        ifthen('Project Name', uid)
        ifthen('cluster-name', uid)
        ifthen('s3-staging-dir', f's3://{uid}')
        ifthen('stage', 'dev')
        ifthen('region', 'eu-west-1')
        assert ifthen('spark_version = "2.4.5"' )
        assert ifthen( EOF )
    
    with pexpect2(f"pyemr add cowsay==4.0") as ifthen:
        assert ifthen(EOF)
    
    assert os.path.isfile(toml_path)
    toml = open(toml_path).read()
    assert f'name = "{uid}"' in toml
    assert 'cowsay = "4.0"' in toml
    assert f's3-staging-dir = "s3://{uid}"' in toml


