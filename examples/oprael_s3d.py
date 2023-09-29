# License: MIT
import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from oprael import Optimizer, space as sp, OPRAELOptimizer
import argparse
import os
import subprocess
import sys


argparser = argparse.ArgumentParser()

argparser.add_argument('--access',default="w",help="r replace only read,w replace only write,rw replace read and write")
argparser.add_argument("--MPIN",type=str,default="8",help="The MPI Node to run the benchmark.")
argparser.add_argument("--process",type=str,default="64",help="The number of process to run the benchmark.")
args = argparser.parse_args()

# Define Search Space
space = sp.Space()
strp_fac = sp.Int("Strip_Count", 1, 64, default_value=1)
strp_unt = sp.Int("Strip_Size", 1, 1024, default_value=1)
rm_cb_read = sp.Int("Romio_CB_Read", 0, 2, default_value=0)
rm_cb_write = sp.Int("Romio_CB_Write", 0, 2, default_value=0)
rm_ds_read = sp.Int("Romio_DS_Read", 0, 2, default_value=0)
rm_ds_write = sp.Int("Romio_DS_Write", 0, 2, default_value=0)
cb_nodes = sp.Int("Cb_nodes", 1, 64, default_value=1)
config_list = sp.Int("Cb_config", 1, 8, default_value=1)

space.add_variables([strp_fac, strp_unt, rm_cb_read, rm_cb_write, rm_ds_read, rm_ds_write,cb_nodes,config_list])

Mbytes = 1024 * 1024
states_mapping = ["automatic","disable","enable"]


def getIO(path):
    with open(path, "r") as f:
        contents = f.readlines()
    performance = -10000

    for _ in contents:
        if "write bandwidth" in _:
            performance = float(_.split(":")[1].replace("MiB/s", "").strip())
    return performance

# Define Objective Function
def eval_func(config):
    this_strp_fac = config["Strip_Count"]
    this_strp_uni = config["Strip_Size"] * Mbytes
    this_rm_cb_read = config["Romio_CB_Read"]
    this_rm_cb_write = config["Romio_CB_Write"]
    this_ds_read = config["Romio_DS_Read"]
    this_ds_write = config["Romio_DS_Write"]
    this_cb_nodes = config["Cb_nodes"]
    this_config_list = config["Cb_config"]
    node_list = "*:%s" % (this_config_list)

    path = os.getcwd()
    hint = os.path.join(path, "hint.txt")
    with open(hint, 'w') as f:    
        f.write(str(this_strp_fac))
        f.write('\n')
        f.write(str(this_strp_uni))
        f.write('\n')
        f.write(str(this_rm_cb_read))
        f.write('\n')
        f.write(str(this_rm_cb_write))
        f.write('\n')
        f.write(str(this_ds_read))
        f.write('\n')
        f.write(str(this_ds_write))
        f.write('\n')
        f.write(str(this_cb_nodes))
        f.write('\n')
        f.write(str(this_config_list))
    f.close()
    print("Evaluate Parameters config (%d, %d, %d, %d, %d, %d, %d, %d):" % (
    this_strp_fac, this_strp_uni, this_rm_cb_read, this_rm_cb_write, this_ds_read, this_ds_write,this_cb_nodes,this_config_list))
    tmp_json_name = "%d_%d_%d_%d,_%d_%d_%d_%d.json" % (
    this_strp_fac, this_strp_uni, this_rm_cb_read, this_rm_cb_write, this_ds_read, this_ds_write, this_cb_nodes, this_config_list)
    tmp_time_result = os.path.join(path, tmp_json_name)
    try:
        if os.path.exists(tmp_time_result):
            performance = getIO(tmp_time_result)
            return {'objectives': [-performance]}

        #cmd = r"yhrun -p thcp1 -N %s -n %s /path/s3d_io.x 200 200 200 4 4 4 1 T . %s %s %s %s %s %s %s %s >> %s" % (
        #args.MPIN, args.process, str(this_strp_fac), str(this_strp_uni),
        #states_mapping[this_rm_cb_read], states_mapping[this_rm_cb_write], states_mapping[this_ds_read], states_mapping[this_ds_write],
        #str(this_cb_nodes), node_list, tmp_time_result)
        cmd = r"yhrun -p thcp1 -N %s -n %s /path/s3d_io.x 200 200 200 4 4 4 1 T . >> %s" % (
        args.MPIN, args.process, tmp_time_result)
        print(cmd)
        subprocess.run(cmd, shell=True)
        performance = getIO(tmp_time_result)
        return {'objectives': [-performance]}
    except Exception as e:
        print("error",e)
        return {'objectives': [10000]}


# Run
if __name__ == "__main__":
    common_feature = {"Data": "S3D-I/O","nprocs": 64,
                      "I/O_amount": 6141803233.28, "MPI_Node": 8, "Process_PerNode": 8, "Mode": 1}

    opt = OPRAELOptimizer( 
        eval_func,
        space,
        max_runs=3,
        runtime_limit=31500,
        advisor_type='custom',
        # surrogate_type='custom',
        time_limit_per_trial=1800,
        task_id='OPRAEL_S3D-I/O',
        #train_csv=r"s3d_200_200.csv",
        access=args.access,
        common_feature=common_feature,
        darshan_path=r"200_200.darshan-txt",
        custom_advisor_list=["tpe","ga", "bo"] 
    )
    history = opt.run()

    f = open('OPRAEL_S3D-IO.log', 'w')
    sys.stdout = f

    print(history)

    sys.stdout = sys.__stdout__
    f.close()
