import os
import numpy as np
import pandas as pd
import json


def Generate_hints(spn,spf_M,cbr,cbw,dsr,dsw):
    path = os.getcwd()

    mapping = ["automatic","disable","enable"]

    contents = "IOR_HINT__MPI__striping_factor=" + str(spn) + "\n" \
    + "IOR_HINT__MPI__striping_unit=" + str(spf_M) + "\n" \
    + "IOR_HINT__MPI__romio_cb_read=" + mapping[cbr] + "\n" \
    + "IOR_HINT__MPI__romio_cb_write="+ mapping[cbw] + "\n" \
    + "IOR_HINT__MPI__romio_ds_read=" + mapping[dsr] +"\n" \
    + "IOR_HINT__MPI__romio_ds_write=" + mapping[dsw] +"\n"

    with open(os.path.join(path,"hintsF"),"w") as f:
        f.write(contents)

def GetJsonContent(jsonPath,target):
    with open(jsonPath, encoding='utf-8') as f:
        content = json.load(f)
        result_s = content["tests"][0]["Results"]
        read_list = []
        write_list = []
        for _ in result_s:
            if _["access"] == "read":
                read_list.append(_[target])
            else:
                write_list.append(_[target])
    return read_list, write_list

