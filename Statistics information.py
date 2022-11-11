#!/user/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import datetime
import numpy as np
import pandas as pd

starttime = datetime.datetime.now()	# Running time statistics
y=0
all_info=pd.DataFrame(pd.read_csv('E:/SHIOMI_data/wetransfer_paired-trajectories_2022-02-23_0850/result/all_info_sensi_T - delete6.5.csv'))
id_sensi=all_info['id']     # Modify the id of the table
times = [0]*len(id_sensi)       # Add new time column

if __name__ == '__main__':
    filenames_in = 'E:/SHIOMI_data/wetransfer_paired-trajectories_2022-02-23_0850/result/new_id'  # 输入文件的文件地址
    pathDir = os.listdir(filenames_in)
    for allDir in pathDir:
        child = re.findall(r"(.+?).csv", allDir)  # Regular way to read file name, remove extension
        if len(child) >= 0:  # Remove useless system files
            newfile = ''
            needdate = child  #### This is the desired file name
        domain1 = os.path.abspath(filenames_in)  # Pending file location
        info = os.path.join(domain1, allDir)  # Splice out the name of the file to be processed

        # ------------Data processing process---------------
        print(info, "start processing")
        print(needdate)
        df = pd.DataFrame(pd.read_csv(info))   # read file data
        x = df['id']
        id_number=x[1]    # id
        id_length=len(x)        # time
        for i in range(len(times)):
            if id_sensi[i] == id_number:
                times[i]=id_length


        print(info, "done")

all_info['times']=times
all_info.to_csv(r"E:/SHIOMI_data/wetransfer_paired-trajectories_2022-02-23_0850/result/all_info_sensi_T - 副本-new.csv",mode = 'a',index =False)
endtime = datetime.datetime.now()
print(endtime - starttime)
print(y)