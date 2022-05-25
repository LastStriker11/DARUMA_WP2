# -*- coding: utf-8 -*-
"""
@author: LQL
"""
import pandas as pd
import numpy as np
import os
#%%
t_interval = 10 # in minutes
data_folder = '../Madrid_data/detector_data/'
list_data = [f for f in os.listdir(data_folder) if f.endswith('.csv')]  # please have a look at the order of the files
data_collect = []
file = list_data[0]
year = int(file.split('_')[1][:4])
month = int(file.split('_')[1][4:6])
day = int(file.split('_')[1][6:8])


data1 = pd.read_csv(data_folder+file, encoding = 'latin-1')
cols = ['idelem', 'intensidad', 'ocupacion', 'carga']
cols_new = ['id', 'volume', 'occupancy', 'load_para']
data1 = data1[cols]
data1.columns = cols_new
#%%
volume_collect = []
occupancy_collect = []
load_para_collect = []
for var in ['volume', 'occupancy', 'load_para']:
    volum