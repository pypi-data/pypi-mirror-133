import os
import pexpect
import pytest




def test_pyemr_start_python(tmp_chdir,pexpect2):
    """

    Args:
      pexpect_runner:

    Returns:

    """
    with pexpect2("pyemr python") as ifthen:
        assert ifthen("Select spark_version", '\n' )
        assert ifthen(">>>")



def test_pyemr_sucess(tmp_chdir, pexpect2, uid):
    """

    Args:
      pexpect_runner:

    Returns:

    """
    
    code = [
        f"uuid_ = '{uid}'",
        "print(f'Finished:{uuid_}')",
        '\n\n\n'
    ]
    
    with pexpect2("pyemr python") as ifthen:
        assert ifthen("Select spark_version", '\n' )
        assert ifthen(">>>", '\n'.join(code) )
        assert ifthen(f"Finished:{uid}")




def test_pyemr_fail(pexpect2, uid):
    """

    Args:
      pexpect_runner:

    Returns:

    """
    
    with pexpect2("pyemr python") as ifthen:
        assert ifthen("Select spark_version", '\n' )
        assert ifthen(">>>", 'assert False' )
        assert ifthen("AssertionError" )



def test_pyemr_write_dataframe(tmp_chdir, pexpect2, uid, readscript):
    """

    Args:
      pexpect_runner:

    Returns:

    """
    out_path = f"s3://some/s3/bucket/data_{uid}.parquet"
    
    code = f"import sys \n\nsys.argv = [None, '{uid}', '{out_path}'] \n\n"
    code += readscript('write_dataframe.py')
    
    with pexpect2("pyemr python") as ifthen:
        assert ifthen("Select spark_version", '\n' )
        assert ifthen(">>>", code )
        assert ifthen(f"Finished:{uid}")
    
    path = out_path.replace("s3:/", "./data/mock/s3")
    assert len(os.listdir(path)) != 0 or os.path.isdir(path)




def test_read_s3_count_rows(tmp_chdir, pexpect2, uid, readscript, s3_parquet_file):
    """

    Args:
      run_exp:
      copy_to_tmp:
      uid:
      s3_parquet_file:

    Returns:

    """
    
    if s3_parquet_file:
        
        code = f"import sys \nsys.argv = [None, '{uid}', '{s3_parquet_file}'] \n\n"
        code += readscript('count_rows.py') + '\n\n\n'
        
        with pexpect2("pyemr python") as ifthen:
            assert ifthen("Select spark_version", '\n' )
            assert ifthen(">>>", code )
            assert ifthen(f"Finished:{uid}")
        
        path = s3_parquet_file.replace("s3:/", "./data/mock/s3")
        assert len(os.listdir(path)) != 0 or os.path.isdir(path)
    else:
        pytest.skip(
            "Test skipped, 's3_parquet_file' is not specified. Try 'pytest --s3_parquet_file s3://some/parquet'",
        )



def test_import_package_script_interactive(tmp_chdir, pexpect2, readscript, uid):
    """

    Args:
      run_exp:
      copy_to_tmp:
      uid:

    Returns:

    """
    
    # init package and install dependency
    cmd = "pyemr init example cluster_name s3://some/s3/directory dev eu-west-1"
    
    with pexpect2(cmd, 60) as ifthen:
        assert ifthen("spark_version =")
    
    with pexpect2('poetry add cowsay==4.0', 60) as ifthen:
        assert ifthen(pexpect.EOF)
    
    # run import script
    code = f"import sys \nsys.argv = [None, '{uid}'] \n\n"
    code = code + '\n' + readscript('import_package.py') + '\n\n\n'
    with pexpect2('pyemr python', 300) as ifthen:
        assert ifthen('>>>', code)
        assert ifthen( f"Finished:{uid}" )


