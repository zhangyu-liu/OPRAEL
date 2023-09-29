"""
data preprocessing
"""

import re
import numpy as np
import pandas as pd
import logging
from sklearn.preprocessing import StandardScaler

def get_number_columns(df):
    """
    Returns the columns that contain values, excluding columns contain string metadata.
    """
    return df.columns[np.logical_or(df.dtypes == np.float64, df.dtypes == np.int64)]


def normalization(df):
    df = df.copy()

    if np.any(np.isnan(df[get_number_columns(df)])):
        logging.error("Found NaN values before normalizing data.")

    total_accesses = df.POSIX_WRITES + df.POSIX_READS
    total_bytes = df.POSIX_total_bytes

    df['POSIX_total_accesses'] = total_accesses

    try:
        df['POSIX_BYTES_READ_PERC'] = df.POSIX_BYTES_READ / total_bytes
        df['POSIX_BYTES_WRITTEN_PERC'] = df.POSIX_BYTES_WRITTEN / total_bytes
    except:
        logging.error(
            "Failed to normalize one of the features in [POSIX_BYTES_READ, POSIX_BYTES_WRITTEN]")

    try:
        df['POSIX_READS_PERC'] = df.POSIX_READS / total_accesses
        df['POSIX_WRITES_PERC'] = df.POSIX_WRITES / total_accesses
        df['POSIX_SEQ_READS_PERC'] = df.POSIX_SEQ_READS / total_accesses
        df['POSIX_SEQ_WRITES_PERC'] = df.POSIX_SEQ_WRITES / total_accesses
        df['POSIX_CONSEC_READS_PERC'] = df.POSIX_CONSEC_READS / total_accesses
        df['POSIX_CONSEC_WRITES_PERC'] = df.POSIX_CONSEC_WRITES / total_accesses
    except:
        logging.error(
            "Failed to normalize one of the features in [POSIX_READS, POSIX_WRITES, POSIX_SEQ_WRITES, POSIX_SEQ_READS, POSIX_CONSEC_READS, POSIX_CONSEC_WRITES]")

    try:

        df['POSIX_SIZE_READ_0_100_PERC'] = df.POSIX_SIZE_READ_0_100 / total_accesses
        df['POSIX_SIZE_READ_100_1K_PERC'] = df.POSIX_SIZE_READ_100_1K / total_accesses
        df['POSIX_SIZE_READ_1K_10K_PERC'] = df.POSIX_SIZE_READ_1K_10K / total_accesses
        df['POSIX_SIZE_READ_10K_100K_PERC'] = df.POSIX_SIZE_READ_10K_100K / total_accesses
        df['POSIX_SIZE_READ_100K_1M_PERC'] = df.POSIX_SIZE_READ_100K_1M / total_accesses
        df['POSIX_SIZE_READ_1M_4M_PERC'] = df.POSIX_SIZE_READ_1M_4M / total_accesses
        df['POSIX_SIZE_READ_4M_10M_PERC'] = df.POSIX_SIZE_READ_4M_10M / total_accesses
        df['POSIX_SIZE_READ_10M_100M_PERC'] = df.POSIX_SIZE_READ_10M_100M / total_accesses
        df['POSIX_SIZE_READ_100M_1G_PERC'] = df.POSIX_SIZE_READ_100M_1G / total_accesses
        df['POSIX_SIZE_READ_1G_PLUS_PERC'] = df.POSIX_SIZE_READ_1G_PLUS / total_accesses

        df['POSIX_SIZE_WRITE_0_100_PERC'] = df.POSIX_SIZE_WRITE_0_100 / total_accesses
        df['POSIX_SIZE_WRITE_100_1K_PERC'] = df.POSIX_SIZE_WRITE_100_1K / total_accesses
        df['POSIX_SIZE_WRITE_1K_10K_PERC'] = df.POSIX_SIZE_WRITE_1K_10K / total_accesses
        df['POSIX_SIZE_WRITE_10K_100K_PERC'] = df.POSIX_SIZE_WRITE_10K_100K / total_accesses
        df['POSIX_SIZE_WRITE_100K_1M_PERC'] = df.POSIX_SIZE_WRITE_100K_1M / total_accesses
        df['POSIX_SIZE_WRITE_1M_4M_PERC'] = df.POSIX_SIZE_WRITE_1M_4M / total_accesses
        df['POSIX_SIZE_WRITE_4M_10M_PERC'] = df.POSIX_SIZE_WRITE_4M_10M / total_accesses
        df['POSIX_SIZE_WRITE_10M_100M_PERC'] = df.POSIX_SIZE_WRITE_10M_100M / total_accesses
        df['POSIX_SIZE_WRITE_100M_1G_PERC'] = df.POSIX_SIZE_WRITE_100M_1G / total_accesses
        df['POSIX_SIZE_WRITE_1G_PLUS_PERC'] = df.POSIX_SIZE_WRITE_1G_PLUS / total_accesses

    except:
        logging.warning("Failed to normalize POSIX_SIZE_*")


    # In case of division by zero, we'll get NaN. We convert those to zeros.
    df = df.fillna(0)

    return df


def log_scale_dataset(df, add_small_value=1, set_NaNs_to=-10):
    """
    Takes a base 10 logarithmic transformation.
    """
    number_columns = get_number_columns(df)
    columns = [x for x in number_columns if "perc" not in x.lower()]
    logging.info("Applying log10() to the columns {}".format(columns))

    for c in columns:
        if c == 'MPI_Node' or c == 'nprocs' or c=='Strip_Count' or c=='Strip_Size' or c=='I/O_amount' or c=='Cb_nodes' or c=='Cb_config' or c=='Process_PerNode' \
                or c=='Block_Size' or c=='Segment_Count' or c=='proc_perNode':
            df["LOG10_" + c] = np.log10(df[c] + add_small_value).fillna(value=set_NaNs_to)
            df.rename(columns={c: "RAW_" + c}, inplace=True)
        else:
            df[c.replace("POSIX", "POSIX_LOG10")] = np.log10(df[c] + add_small_value).fillna(value=set_NaNs_to)
            df.rename(columns={c: c.replace("POSIX", "POSIX_RAW")}, inplace=True)

    return df

