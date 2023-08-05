import uuid
import pexpect 
import os


def test_end2end(

    tmp_chdir, 
    copy_to_tmp, 
    uid, 
    s3_parquet_file, 
    cluster_name, 
    region, 
    s3_stage_dir, 
    script_dir,
    pexpect2, 
    
):
    """End-to-end project build test. 

    Args:
      stdin:
      pyemr:
      cluster_name: specify a real emr cluster
      region: specify a emr region
      s3_stage_dir:
      s3_parquet_file:
      script_dir:

    """
    
    # get param
    name = f'unittest_{uid}'
    cluster_name_ = cluster_name or f'cluster_{uid}'
    s3_stage_dir_ = s3_stage_dir or f's3://_{uid}'
    region = region or 'eu-west-1'
    
    # check files don't exist 
    assert not os.path.isfile("./pyproject.toml")
    assert not os.path.isfile(f"./dist/{name}_dev_0_1_0.tar.gz")
        
    # init project     
    os.system(f"pyemr init {name} {cluster_name_} {s3_stage_dir_} dev {region}")
    assert os.path.isfile("./pyproject.toml")
    os.system('poetry add cowsay==4.0')
    os.system('pyemr add fire==0.4.0')
    assert 'cowsay' in open("./pyproject.toml").read()
    copy_to_tmp('count_rows.py')
    
    # if real stage specified that build 
    if s3_stage_dir :
        os.system('pyemr build')
        assert os.path.isfile(f"./dist/{name}_dev_0_1_0.tar.gz")
        
        # check the s3 path 
        ls_s3_path = f'aws s3 ls {s3_stage_dir_}/{name}/stage=dev/version=0.1.0/code/latest/{name}_dev_0_1_0.tar.gz'
        with pexpect2(ls_s3_path) as ifthen:
            assert ifthen(f' {name}_dev_0_1_0.tar.gz')
        
        # test 
        if s3_parquet_file:
            
            with pexpect2(f"pyemr test count_rows.py {uid} {s3_parquet_file}", 120) as ifthen:
                assert ifthen('Download part?', '\n')
                assert ifthen(f'Finished:{uid}')
            
            # run on cluster 
            if cluster_name and region:
                os.system(f"pyemr submit count_rows.py {uid} {s3_parquet_file}")
                os.system(f"pyemr logs count_rows.py {uid} {s3_parquet_file}")
                os.system(f"pyemr export count_rows.py {uid} {s3_parquet_file}")


