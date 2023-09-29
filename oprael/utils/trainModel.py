import os
import numpy as np
import xgboost as xgb
import pandas as pd
import sklearn
from oprael.utils.getFeature import collect_data
from oprael.utils.dataset import normalization, log_scale_dataset
import time
import pickle
# from sklearn.inspection import permutation_importance
# import shap

# BT-IO and S3D-I/O
common_input_ = ["LOG10_MPI_Node", "LOG10_nprocs", "LOG10_Strip_Count", "LOG10_Strip_Size", "Romio_CB_Read", "Romio_CB_Write", \
                      "Romio_DS_Read", "Romio_DS_Write","LOG10_I/O_amount","LOG10_Cb_nodes","LOG10_Cb_config","Mode","LOG10_Process_PerNode"]

#IOR
#common_input_ = ["LOG10_MPI_Node", "LOG10_nprocs", "LOG10_Strip_Count", "LOG10_Strip_Size", "LOG10_Block_Size",
#                     "LOG10_Segment_Count", "Romio_CB_Read", "Romio_CB_Write", \
#                     "Romio_DS_Read", "Romio_DS_Write","FPerP", "LOG10_proc_perNode"]

read_input_new_ = ["POSIX_BYTES_READ_PERC","POSIX_CONSEC_READS_PERC","POSIX_SEQ_READS_PERC","POSIX_SIZE_READ_0_100_PERC", \
                       "POSIX_SIZE_READ_100K_1M_PERC","POSIX_SIZE_READ_100M_1G_PERC","POSIX_SIZE_READ_100_1K_PERC","POSIX_SIZE_READ_10K_100K_PERC", \
                       "POSIX_SIZE_READ_10M_100M_PERC","POSIX_SIZE_READ_1G_PLUS_PERC","POSIX_SIZE_READ_1K_10K_PERC","POSIX_SIZE_READ_1M_4M_PERC","POSIX_SIZE_READ_4M_10M_PERC","POSIX_READS_PERC"]

write_input_new_ = ["POSIX_BYTES_WRITTEN_PERC","POSIX_CONSEC_WRITES_PERC","POSIX_SEQ_WRITES_PERC", \
        "POSIX_SIZE_WRITE_0_100_PERC","POSIX_SIZE_WRITE_100K_1M_PERC","POSIX_SIZE_WRITE_100M_1G_PERC","POSIX_SIZE_WRITE_100_1K_PERC","POSIX_SIZE_WRITE_10K_100K_PERC", \
                       "POSIX_SIZE_WRITE_10M_100M_PERC","POSIX_SIZE_WRITE_1G_PLUS_PERC","POSIX_SIZE_WRITE_1K_10K_PERC","POSIX_SIZE_WRITE_1M_4M_PERC","POSIX_SIZE_WRITE_4M_10M_PERC", \
                       "POSIX_WRITES_PERC"]

Mode = ["Mode"]

def huber_approx_obj(y_pred, y_test):

    """
    Huber loss, adapted from https://stackoverflow.com/questions/45006341/xgboost-how-to-use-mae-as-objective-function
    """
    d = y_pred - y_test
    h = 5  # h is delta in the graphic
    scale = 1 + (d / h) ** 2
    scale_sqrt = np.sqrt(scale)
    grad = d / scale_sqrt
    hess = 1 / scale / scale_sqrt
    return grad, hess


def getColumns(mode):
    if mode=="read":
        return set(common_input_ + read_input_new_)
    elif mode=="write":
        return set(common_input_ + write_input_new_)
    else:
        return set(common_input_ + Mode)  #read:0  write:1


def split_data(data,input_colums,pre_column):
    X = data[input_colums]
    Y = data[pre_column]  #

    X_train, X_test, Y_train, Y_test = sklearn.model_selection.train_test_split(X, Y, test_size=0.3)
    return X_train,X_test,Y_train,Y_test

def train_XGB(train_data, mode):
    '''
    global read_input_columns, write_input_columns
    
    data = pd.read_csv(train_data)
    if mode == "read":
        input_columns = getColumns("read")
        X_train, X_test, Y_train, Y_test = split_data(data, input_columns, "LOG10_r_bw")
    elif mode == "write":
        input_columns = getColumns("write")
        X_train, X_test, Y_train, Y_test = split_data(data, input_columns, "LOG10_w_bw")
    
    xgb_model = xgb.XGBRegressor(obj=huber_approx_obj)
    
    xgb_model.fit(X_train, Y_train, eval_metric=huber_approx_obj)
    
    with open('./xgb.pkl', 'wb') as f:
        pickle.dump(xgb_model, f)
    '''
    # IOR
    #with open('./xgb_ior.pkl', 'rb') as f:
    #    xgb_model = pickle.load(f)
    #f.close()
    
    # S3D-I/O
    with open('./xgb_s3d-io.pkl', 'rb') as f:
        xgb_model = pickle.load(f)
    f.close()

    return xgb_model

def log_scale_feature(df, add_small_value=1, set_NaNs_to=-10):
    # IOR
    #number_list = ["MPI_Node","nprocs","Strip_Count","Strip_Size","Block_Size","Segment_Count","proc_perNode"]
    # S3D-I/O and BT-I/O
    number_list = ["MPI_Node","nprocs","Strip_Count","Strip_Size","I/O_amount","Cb_nodes","Cb_config","Process_PerNode"]


    df[number_list] = df[number_list].astype(float)
    for c in number_list:
        df["LOG10_" + c] = np.log10(df[c] + add_small_value).fillna(value=set_NaNs_to)
        df.rename(columns={c: "RAW_" + c}, inplace=True)
    return df


def get_darshanFeature(darshanPath):
    d_ = collect_data(darshanPath)
    darshan_feature = pd.DataFrame()

    #darshan_feature = darshan_feature.append(d_, ignore_index=True)
    darshan_feature = pd.concat([darshan_feature, pd.DataFrame([d_])], ignore_index=True)

    darshan_feature = normalization(darshan_feature)
    darshan_feature = log_scale_dataset(darshan_feature)
    return darshan_feature
