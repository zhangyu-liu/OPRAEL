import os
import sys
import numpy as np
import pandas as pd

def collect_data(run):
    with open(run, 'r') as f:
        try:
            lines = f.read().split("\n")
        except UnicodeDecodeError:
            print('Read err%s' % run)
        f.close()
    try:
        start_time = int(lines[5].split(' ')[-1])
        end_time = int(lines[7].split(' ')[-1])
        RAW_runtime = end_time - start_time
        col_data = {"id":{}}
        start_line = r"#<module>"
        s_flag = False
        POSIX_RAW_OPENS =  0

        for line in lines:
            if start_line in line:
                s_flag = True
                continue
            if s_flag==True:
                if 'POSIX_BYTES_READ' in line:
                    sp_line = line.split('\t')
                    shared_flag = sp_line[1]
                    rank_id = sp_line[2]
                    POSIX_BYTES_READ = int(sp_line[4])
                    col_data["id"][rank_id]["read_bytes"] = POSIX_BYTES_READ
                elif 'POSIX_BYTES_WRITTEN' in line:
                    sp_line = line.split('\t')
                    shared_flag = sp_line[1]
                    rank_id = sp_line[2]
                    POSIX_BYTES_WRITTEN = int(sp_line[4])
                    col_data["id"][rank_id]["write_bytes"] = POSIX_BYTES_WRITTEN
                elif 'POSIX_READS' in line:
                    sp_line = line.split('\t')
                    rank_id = sp_line[2]
                    POSIX_READS = int(sp_line[4])
                    if rank_id in col_data["id"]:
                        col_data["id"][rank_id] ["POSIX_READS"] = POSIX_READS
                    else:
                        col_data["id"][rank_id]  = {"POSIX_READS": POSIX_READS}
                elif 'POSIX_WRITES' in line:
                    sp_line = line.split('\t')
                    rank_id = sp_line[2]
                    POSIX_WRITES = int(sp_line[4])
                    if rank_id in col_data["id"]:
                        col_data["id"][rank_id] ["POSIX_WRITES"] = POSIX_WRITES
                    else:
                        col_data["id"][rank_id]  = {"POSIX_WRITES": POSIX_WRITES}
                elif 'POSIX_SEQ_WRITES' in line:
                    sp_line = line.split('\t')
                    rank_id = sp_line[2]
                    POSIX_SEQ_WRITES = int(sp_line[4])
                    if rank_id in col_data["id"]:
                        col_data["id"][rank_id] ["POSIX_SEQ_WRITES"] = POSIX_SEQ_WRITES
                    else:
                        col_data["id"][rank_id]  = {"POSIX_SEQ_WRITES": POSIX_SEQ_WRITES}
                elif 'POSIX_SEQ_READS' in line:
                    sp_line = line.split('\t')
                    rank_id = sp_line[2]
                    POSIX_SEQ_READS = int(sp_line[4])
                    if rank_id in col_data["id"]:
                        col_data["id"][rank_id] ["POSIX_SEQ_READS"] = POSIX_SEQ_READS
                    else:
                        col_data["id"][rank_id]  = {"POSIX_SEQ_READS": POSIX_SEQ_READS}
                elif 'POSIX_CONSEC_READS' in line:
                    sp_line = line.split('\t')
                    rank_id = sp_line[2]
                    POSIX_CONSEC_READS = int(sp_line[4])
                    if rank_id in col_data["id"]:
                        col_data["id"][rank_id] ["POSIX_CONSEC_READS"] = POSIX_CONSEC_READS
                    else:
                        col_data["id"][rank_id]  = {"POSIX_CONSEC_READS": POSIX_CONSEC_READS}
                elif 'POSIX_CONSEC_WRITES' in line:
                    sp_line = line.split('\t')
                    rank_id = sp_line[2]
                    POSIX_CONSEC_WRITES = int(sp_line[4])
                    if rank_id in col_data["id"]:
                        col_data["id"][rank_id] ["POSIX_CONSEC_WRITES"] = POSIX_CONSEC_WRITES
                    else:
                        col_data["id"][rank_id]  = {"POSIX_CONSEC_WRITES": POSIX_CONSEC_WRITES}
                elif 'POSIX_SIZE_READ_0_100' in line:
                    sp_line = line.split('\t')
                    rank_id = sp_line[2]
                    POSIX_SIZE_READ_0_100 = int(sp_line[4])
                    if rank_id in col_data["id"]:
                        col_data["id"][rank_id] ["POSIX_SIZE_READ_0_100"] = POSIX_SIZE_READ_0_100
                    else:
                        col_data["id"][rank_id]  = {"POSIX_SIZE_READ_0_100":POSIX_SIZE_READ_0_100}
                elif 'POSIX_SIZE_READ_100_1K' in line:
                    POSIX_SIZE_READ_100_1K = int(sp_line[4])
                    sp_line = line.split('\t')
                    rank_id = sp_line[2]
                    if rank_id in col_data["id"]:
                        col_data["id"][rank_id] ["POSIX_SIZE_READ_100_1K"] = POSIX_SIZE_READ_100_1K
                    else:
                        col_data["id"][rank_id]  = {"POSIX_SIZE_READ_100_1K": POSIX_SIZE_READ_100_1K}
                elif 'POSIX_SIZE_READ_1K_10K' in line:
                    sp_line = line.split('\t')
                    rank_id = sp_line[2]
                    POSIX_SIZE_READ_1K_10K = int(sp_line[4])
                    if rank_id in col_data["id"]:
                        col_data["id"][rank_id] ["POSIX_SIZE_READ_1K_10K"] = POSIX_SIZE_READ_1K_10K
                    else:
                        col_data["id"][rank_id]  = {"POSIX_SIZE_READ_1K_10K": POSIX_SIZE_READ_1K_10K}
                elif 'POSIX_SIZE_READ_10K_100K' in line:
                    sp_line = line.split('\t')
                    rank_id = sp_line[2]
                    POSIX_SIZE_READ_10K_100K = int(sp_line[4])
                    if rank_id in col_data["id"]:
                        col_data["id"][rank_id] ["POSIX_SIZE_READ_10K_100K"] = POSIX_SIZE_READ_10K_100K
                    else:
                        col_data["id"][rank_id]  = {"POSIX_SIZE_READ_10K_100K": POSIX_SIZE_READ_10K_100K}
                elif 'POSIX_SIZE_READ_100K_1M' in line:
                    sp_line = line.split('\t')
                    rank_id = sp_line[2]
                    POSIX_SIZE_READ_100K_1M = int(sp_line[4])
                    if rank_id in col_data["id"]:
                        col_data["id"][rank_id] ["POSIX_SIZE_READ_100K_1M"] = POSIX_SIZE_READ_100K_1M
                    else:
                        col_data["id"][rank_id]  = {"POSIX_SIZE_READ_100K_1M": POSIX_SIZE_READ_100K_1M}
                elif 'POSIX_SIZE_READ_1M_4M' in line:
                    sp_line = line.split('\t')
                    rank_id = sp_line[2]
                    POSIX_SIZE_READ_1M_4M = int(sp_line[4])
                    if rank_id in col_data["id"]:
                        col_data["id"][rank_id] ["POSIX_SIZE_READ_1M_4M"] = POSIX_SIZE_READ_1M_4M
                    else:
                        col_data["id"][rank_id]  = {"POSIX_SIZE_READ_1M_4M": POSIX_SIZE_READ_1M_4M}
                elif 'POSIX_SIZE_READ_4M_10M' in line:
                    sp_line = line.split('\t')
                    rank_id = sp_line[2]
                    POSIX_SIZE_READ_4M_10M = int(sp_line[4])
                    if rank_id in col_data["id"]:
                        col_data["id"][rank_id] ["POSIX_SIZE_READ_4M_10M"] = POSIX_SIZE_READ_4M_10M
                    else:
                        col_data["id"][rank_id]  = {"POSIX_SIZE_READ_4M_10M": POSIX_SIZE_READ_4M_10M}
                elif 'POSIX_SIZE_READ_10M_100M' in line:
                    sp_line = line.split('\t')
                    rank_id = sp_line[2]
                    POSIX_SIZE_READ_10M_100M = int(sp_line[4])
                    if rank_id in col_data["id"]:
                        col_data["id"][rank_id] ["POSIX_SIZE_READ_10M_100M"] = POSIX_SIZE_READ_10M_100M
                    else:
                        col_data["id"][rank_id]  = {"POSIX_SIZE_READ_10M_100M": POSIX_SIZE_READ_10M_100M}
                elif 'POSIX_SIZE_READ_100M_1G' in line:
                    sp_line = line.split('\t')
                    rank_id = sp_line[2]
                    POSIX_SIZE_READ_100M_1G = int(sp_line[4])
                    if rank_id in col_data["id"]:
                        col_data["id"][rank_id] ["POSIX_SIZE_READ_100M_1G"] = POSIX_SIZE_READ_100M_1G
                    else:
                        col_data["id"][rank_id]  = {"POSIX_SIZE_READ_100M_1G": POSIX_SIZE_READ_100M_1G}
                elif 'POSIX_SIZE_READ_1G_PLUS' in line:
                    sp_line = line.split('\t')
                    rank_id = sp_line[2]
                    POSIX_SIZE_READ_1G_PLUS = int(sp_line[4])
                    if rank_id in col_data["id"]:
                        col_data["id"][rank_id] ["POSIX_SIZE_READ_1G_PLUS"] = POSIX_SIZE_READ_1G_PLUS
                    else:
                        col_data["id"][rank_id]  = {"POSIX_SIZE_READ_1G_PLUS": POSIX_SIZE_READ_1G_PLUS}
                elif 'POSIX_SIZE_WRITE_0_100' in line:
                    sp_line = line.split('\t')
                    rank_id = sp_line[2]
                    POSIX_SIZE_WRITE_0_100 = int(sp_line[4])
                    if rank_id in col_data["id"]:
                        col_data["id"][rank_id] ["POSIX_SIZE_WRITE_0_100"] = POSIX_SIZE_WRITE_0_100
                    else:
                        col_data["id"][rank_id]  = {"POSIX_SIZE_WRITE_0_100": POSIX_SIZE_WRITE_0_100}
                elif 'POSIX_SIZE_WRITE_100_1K' in line:
                    sp_line = line.split('\t')
                    rank_id = sp_line[2]
                    POSIX_SIZE_WRITE_100_1K = int(sp_line[4])
                    if rank_id in col_data["id"]:
                        col_data["id"][rank_id] ["POSIX_SIZE_WRITE_100_1K"] = POSIX_SIZE_WRITE_100_1K
                    else:
                        col_data["id"][rank_id]  = {"POSIX_SIZE_WRITE_100_1K": POSIX_SIZE_WRITE_100_1K}
                elif 'POSIX_SIZE_WRITE_1K_10K' in line:
                    sp_line = line.split('\t')
                    rank_id = sp_line[2]
                    POSIX_SIZE_WRITE_1K_10K = int(sp_line[4])
                    if rank_id in col_data["id"]:
                        col_data["id"][rank_id] ["POSIX_SIZE_WRITE_1K_10K"] = POSIX_SIZE_WRITE_1K_10K
                    else:
                        col_data["id"][rank_id]  = {"POSIX_SIZE_WRITE_1K_10K": POSIX_SIZE_WRITE_1K_10K}
                elif 'POSIX_SIZE_WRITE_10K_100K' in line:
                    sp_line = line.split('\t')
                    rank_id = sp_line[2]
                    POSIX_SIZE_WRITE_10K_100K = int(sp_line[4])
                    if rank_id in col_data["id"]:
                        col_data["id"][rank_id] ["POSIX_SIZE_WRITE_10K_100K"] = POSIX_SIZE_WRITE_10K_100K
                    else:
                        col_data["id"][rank_id]  = {"POSIX_SIZE_WRITE_10K_100K": POSIX_SIZE_WRITE_10K_100K}
                elif 'POSIX_SIZE_WRITE_100K_1M' in line:
                    sp_line = line.split('\t')
                    rank_id = sp_line[2]
                    POSIX_SIZE_WRITE_100K_1M = int(sp_line[4])
                    if rank_id in col_data["id"]:
                        col_data["id"][rank_id] ["POSIX_SIZE_WRITE_100K_1M"] = POSIX_SIZE_WRITE_100K_1M
                    else:
                        col_data["id"][rank_id]  = {"POSIX_SIZE_WRITE_100K_1M": POSIX_SIZE_WRITE_100K_1M}
                elif 'POSIX_SIZE_WRITE_1M_4M' in line:
                    sp_line = line.split('\t')
                    rank_id = sp_line[2]
                    POSIX_SIZE_WRITE_1M_4M = int(sp_line[4])
                    if rank_id in col_data["id"]:
                        col_data["id"][rank_id] ["POSIX_SIZE_WRITE_1M_4M"] = POSIX_SIZE_WRITE_1M_4M
                    else:
                        col_data["id"][rank_id]  = {"POSIX_SIZE_WRITE_1M_4M": POSIX_SIZE_WRITE_1M_4M}
                elif 'POSIX_SIZE_WRITE_4M_10M' in line:
                    sp_line = line.split('\t')
                    rank_id = sp_line[2]
                    POSIX_SIZE_WRITE_4M_10M = int(sp_line[4])
                    if rank_id in col_data["id"]:
                        col_data["id"][rank_id] ["POSIX_SIZE_WRITE_4M_10M"] = POSIX_SIZE_WRITE_4M_10M
                    else:
                        col_data["id"][rank_id]  = {"POSIX_SIZE_WRITE_4M_10M": POSIX_SIZE_WRITE_4M_10M}
                elif 'POSIX_SIZE_WRITE_10M_100M' in line:
                    sp_line = line.split('\t')
                    rank_id = sp_line[2]
                    POSIX_SIZE_WRITE_10M_100M = int(sp_line[4])
                    if rank_id in col_data["id"]:
                        col_data["id"][rank_id] ["POSIX_SIZE_WRITE_10M_100M"] = POSIX_SIZE_WRITE_10M_100M
                    else:
                        col_data["id"][rank_id]  = {"POSIX_SIZE_WRITE_10M_100M": POSIX_SIZE_WRITE_10M_100M}
                elif 'POSIX_SIZE_WRITE_100M_1G' in line:
                    sp_line = line.split('\t')
                    rank_id = sp_line[2]
                    POSIX_SIZE_WRITE_100M_1G = int(sp_line[4])

                    if rank_id in col_data["id"]:
                        col_data["id"][rank_id] ["POSIX_SIZE_WRITE_100M_1G"] = POSIX_SIZE_WRITE_100M_1G
                    else:
                        col_data["id"][rank_id]  = {"POSIX_SIZE_WRITE_100M_1G": POSIX_SIZE_WRITE_100M_1G}
                elif 'POSIX_SIZE_WRITE_1G_PLUS' in line:
                    sp_line = line.split('\t')
                    rank_id = sp_line[2]
                    POSIX_SIZE_WRITE_1G_PLUS = int(sp_line[4])
                    if rank_id in col_data["id"]:
                        col_data["id"][rank_id] ["POSIX_SIZE_WRITE_1G_PLUS"] = POSIX_SIZE_WRITE_1G_PLUS
                    else:
                        col_data["id"][rank_id]  = {"POSIX_SIZE_WRITE_1G_PLUS": POSIX_SIZE_WRITE_1G_PLUS}
                elif 'total_bytes' in line:
                    POSIX_total_bytes = int(line.split(' ')[-1])
                elif 'agg_perf_by_slowest:' in line:
                    POSIX_agg_perf_by_slowest = float(line.split(' ')[-1])
                    s_flag = False
                    break
        exe = lines[2]
        uid = lines[3][7:]
    except Exception as e:
        print("error")
        return None
    exe = exe.split("/")

    if (len(exe) > 1):
        exe = exe[-1]
    else:
        exe = exe[-1][7:]

    d = {}
    try:
        POSIX_BYTES_READ=POSIX_BYTES_WRITTEN = 0
        POSIX_READS=POSIX_WRITES=POSIX_SEQ_WRITES=POSIX_SEQ_READS=POSIX_CONSEC_READS=POSIX_CONSEC_WRITES = 0
        POSIX_SIZE_READ_0_100=POSIX_SIZE_READ_100_1K=POSIX_SIZE_READ_1K_10K=POSIX_SIZE_READ_10K_100K=POSIX_SIZE_READ_100K_1M=POSIX_SIZE_READ_1M_4M=POSIX_SIZE_READ_4M_10M= 0
        POSIX_SIZE_READ_10M_100M=POSIX_SIZE_READ_100M_1G=POSIX_SIZE_READ_1G_PLUS=POSIX_SIZE_WRITE_0_100=POSIX_SIZE_WRITE_100_1K=POSIX_SIZE_WRITE_1K_10K=POSIX_SIZE_WRITE_10K_100K=POSIX_SIZE_WRITE_100K_1M = 0
        POSIX_SIZE_WRITE_1M_4M=POSIX_SIZE_WRITE_4M_10M=POSIX_SIZE_WRITE_10M_100M=POSIX_SIZE_WRITE_100M_1G=POSIX_SIZE_WRITE_1G_PLUS = 0


        for rank_ in  col_data["id"].keys():
            POSIX_BYTES_READ += col_data["id"][rank_]["read_bytes"]
            POSIX_BYTES_WRITTEN += col_data["id"][rank_]["write_bytes"]

            POSIX_READS += col_data["id"][rank_]["POSIX_READS"]
            POSIX_WRITES += col_data["id"][rank_]["POSIX_WRITES"]
            POSIX_SEQ_WRITES += col_data["id"][rank_]["POSIX_SEQ_WRITES"]
            POSIX_SEQ_READS += col_data["id"][rank_]["POSIX_SEQ_READS"]
            POSIX_CONSEC_READS += col_data["id"][rank_]["POSIX_CONSEC_READS"]
            POSIX_CONSEC_WRITES += col_data["id"][rank_]["POSIX_CONSEC_WRITES"]

            POSIX_SIZE_READ_0_100 += col_data["id"][rank_]["POSIX_SIZE_READ_0_100"]
            POSIX_SIZE_READ_100_1K += col_data["id"][rank_]["POSIX_SIZE_READ_100_1K"]
            POSIX_SIZE_READ_1K_10K += col_data["id"][rank_]["POSIX_SIZE_READ_1K_10K"]
            POSIX_SIZE_READ_10K_100K += col_data["id"][rank_]["POSIX_SIZE_READ_10K_100K"]
            POSIX_SIZE_READ_100K_1M += col_data["id"][rank_]["POSIX_SIZE_READ_100K_1M"]
            POSIX_SIZE_READ_1M_4M += col_data["id"][rank_]["POSIX_SIZE_READ_1M_4M"]
            POSIX_SIZE_READ_4M_10M += col_data["id"][rank_]["POSIX_SIZE_READ_4M_10M"]
            POSIX_SIZE_READ_10M_100M += col_data["id"][rank_]["POSIX_SIZE_READ_10M_100M"]
            POSIX_SIZE_READ_100M_1G += col_data["id"][rank_]["POSIX_SIZE_READ_100M_1G"]
            POSIX_SIZE_READ_1G_PLUS += col_data["id"][rank_]["POSIX_SIZE_READ_1G_PLUS"]

            POSIX_SIZE_WRITE_0_100 += col_data["id"][rank_]["POSIX_SIZE_WRITE_0_100"]
            POSIX_SIZE_WRITE_100_1K += col_data["id"][rank_]["POSIX_SIZE_WRITE_100_1K"]
            POSIX_SIZE_WRITE_1K_10K += col_data["id"][rank_]["POSIX_SIZE_WRITE_1K_10K"]
            POSIX_SIZE_WRITE_10K_100K += col_data["id"][rank_]["POSIX_SIZE_WRITE_10K_100K"]
            POSIX_SIZE_WRITE_100K_1M += col_data["id"][rank_]["POSIX_SIZE_WRITE_100K_1M"]
            POSIX_SIZE_WRITE_1M_4M += col_data["id"][rank_]["POSIX_SIZE_WRITE_1M_4M"]
            POSIX_SIZE_WRITE_4M_10M += col_data["id"][rank_]["POSIX_SIZE_WRITE_4M_10M"]
            POSIX_SIZE_WRITE_10M_100M += col_data["id"][rank_]["POSIX_SIZE_WRITE_10M_100M"]
            POSIX_SIZE_WRITE_100M_1G += col_data["id"][rank_]["POSIX_SIZE_WRITE_100M_1G"]
            POSIX_SIZE_WRITE_1G_PLUS += col_data["id"][rank_]["POSIX_SIZE_WRITE_1G_PLUS"]

    except ZeroDivisionError:
        return None
    exe = exe.split(" ")
    exe = exe[0]
    exe = exe.strip()
    application = '%s_%s' % (exe, uid)

    d = {'POSIX_agg_perf_by_slowest': POSIX_agg_perf_by_slowest, 'POSIX_total_bytes': POSIX_total_bytes,
         'runtime': RAW_runtime,
         'apps': application,
         'POSIX_BYTES_READ': POSIX_BYTES_READ, 'POSIX_BYTES_WRITTEN': POSIX_BYTES_WRITTEN,
         'POSIX_READS': POSIX_READS, 'POSIX_WRITES': POSIX_WRITES,
         'POSIX_SEQ_WRITES': POSIX_SEQ_WRITES,
         'POSIX_SEQ_READS': POSIX_SEQ_READS, 'POSIX_CONSEC_READS': POSIX_CONSEC_READS, 'POSIX_CONSEC_WRITES': POSIX_CONSEC_WRITES,
         'POSIX_SIZE_READ_0_100': POSIX_SIZE_READ_0_100, 'POSIX_SIZE_READ_100_1K': POSIX_SIZE_READ_100_1K, 'POSIX_SIZE_READ_1K_10K': POSIX_SIZE_READ_1K_10K,
         'POSIX_SIZE_READ_10K_100K': POSIX_SIZE_READ_10K_100K, 'POSIX_SIZE_READ_100K_1M': POSIX_SIZE_READ_100K_1M, 'POSIX_SIZE_READ_1M_4M': POSIX_SIZE_READ_1M_4M, 'POSIX_SIZE_READ_4M_10M': POSIX_SIZE_READ_4M_10M,
         'POSIX_SIZE_READ_10M_100M': POSIX_SIZE_READ_10M_100M, 'POSIX_SIZE_READ_100M_1G': POSIX_SIZE_READ_100M_1G, 'POSIX_SIZE_READ_1G_PLUS': POSIX_SIZE_READ_1G_PLUS, 'POSIX_SIZE_WRITE_0_100': POSIX_SIZE_WRITE_0_100,
         'POSIX_SIZE_WRITE_100_1K': POSIX_SIZE_WRITE_100_1K, 'POSIX_SIZE_WRITE_1K_10K': POSIX_SIZE_WRITE_1K_10K, 'POSIX_SIZE_WRITE_10K_100K': POSIX_SIZE_WRITE_10K_100K, 'POSIX_SIZE_WRITE_100K_1M': POSIX_SIZE_WRITE_100K_1M,
         'POSIX_SIZE_WRITE_1M_4M': POSIX_SIZE_WRITE_1M_4M, 'POSIX_SIZE_WRITE_4M_10M': POSIX_SIZE_WRITE_4M_10M, 'POSIX_SIZE_WRITE_10M_100M': POSIX_SIZE_WRITE_10M_100M, 'POSIX_SIZE_WRITE_100M_1G': POSIX_SIZE_WRITE_100M_1G,
         'POSIX_SIZE_WRITE_1G_PLUS': POSIX_SIZE_WRITE_1G_PLUS}
    return d
