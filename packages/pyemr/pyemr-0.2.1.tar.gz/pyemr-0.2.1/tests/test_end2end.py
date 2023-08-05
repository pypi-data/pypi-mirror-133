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
    """

    Args:
      stdin:
      pyemr:
      cluster_name:
      region:
      s3_stage_dir:
      s3_parquet_file:
      script_dir:

    """
    
    # check files don't exist 
    assert not os.path.isfile("./pyproject.toml")
    assert not os.path.isfile("./pyproject.toml")
    
    # get param
    name = f'unittest_{uid}'
    cluster_name_ = cluster_name or f'cluster_{uid}'
    s3_stage_dir_ = s3_stage_dir or f's3://_{uid}'
    region_ = region or 'some-aws-region'
    
    # init project     
    os.system(f"pyemr init {name} {cluster_name_} {s3_stage_dir_} dev {region_}")
    assert os.path.isfile("./pyproject.toml")
    os.system('poetry add cowsay==4.0')
    os.system('pyemr add fire==0.4.0')
    assert 'cowsay' in open("./pyproject.toml").read()
    copy_to_tmp('count_rows.py')
    
    # build 
    if s3_stage_dir :
        os.system('pyemr build')
        assert os.path.isfile(f"./dist/{name}_dev_0_1_0.tar.gz")
        ls_s3_path = f'aws s3 ls {s3_stage_dir_}/{name}/stage=dev/version=0.1.0/code/latest/{name}_dev_0_1_0.tar.gz'
        with pexpect2(ls_s3_path) as ifthen:
            assert ifthen(' {name}_dev_0_1_0.tar.gz')
        
        # check s3 path
        # test 
        if s3_parquet_file:
            
            with pexpect2(f"pyemr test count_rows.py {uid} {s3_parquet_file}") as ifthen:
                assert ifthen('Download part?', '\n')
                assert ifthen(f'Finished:{uid}')
            
            # run on cluster 
            if cluster_name and region:
                os.system(f"pyemr submit count_rows.py {uid} {s3_parquet_file}")
                os.system(f"pyemr logs count_rows.py {uid} {s3_parquet_file}")
                os.system(f"pyemr export count_rows.py {uid} {s3_parquet_file}")



'''
    def _0_init():
        
        init_cmd = f"pyemr init name_{uid} cluster_{uid} s3://ducket/{uid} dev eu-west-1"
        with pexpect2(f"pyemr init name_{uid} cluster_{uid} s3://ducket/{uid} dev eu-west-1", 60) as ifthen:
            assert ifthen("spark_version =")
        
        with pexpect2("poetry add cowsay==4.0", 120) as ifthen:
            assert ifthen(EOF)
        
        with pexpect2("poetry add fire==0.4.0", 120) as ifthen:
            assert ifthen(EOF)
    
    def _1_build():
        with pexpect2("pyemr build", 200) as ifthen:
            assert ifthen(EOF)
        
        assert len(os.listdir(path)) != 0 or os.path.isdir(path)
    
    def _2_export():
        
        copy_to_tmp('count_rows.py')
        with pexpect2(f"pyemr export {script_dir}/count_rows.py {uid} {s3_parquet_file}", 200) as ifthen:
            assert ifthen(EOF)    
        
        assert len(os.listdir(path)) != 0 or os.path.isdir(path)
    
    def _3_test():
        with pexpect2(f"pyemr test {script_dir}/count_rows.py {uid} {s3_parquet_file}", 200) as ifthen:
            assert ifthen(EOF)        
    
    def _4_submit():
        with pexpect2(f"pyemr submit {script_dir}/count_rows.py {uid} {s3_parquet_file}", 200) as ifthen:
            assert ifthen(EOF)        
    
    _0_init()
    if s3_stage_dir:
        _1_build()
        if s3_parquet_file:
            _3_test()
        if cluster_name and region:
            _4_submit()
'''
        

