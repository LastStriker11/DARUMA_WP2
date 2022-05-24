# -*- coding: utf-8 -*-
"""
@author: lasts
"""
import pandas as pd
import numpy as np
import os
#%%
t_interval = 10 # in minutes
data_folder = '../Kyoto_data/jartic/'
#%%
# For Kyoto
list_data = [f for f in os.listdir(data_folder) if f.endswith('.csv')]  # please have a look at the order of the files
data_collect = []
for file in list_data:
    data1 = pd.read_csv(data_folder+file, encoding='cp932')

    data1['time'] = pd.to_datetime(data1['time']) # change to the datetime type

    # sum up the traffic for every t_interval minutes
    data = data1.groupby([data1.time.dt.floor(str(t_interval)+'T'),'loop_detector_ID'])['traffic'].sum()
    data = data.reset_index(drop=False)
    data['interval'] = (data['time'] - data.loc[0,'time']).dt.total_seconds()/(t_interval*60) # identify interval IDs
    data['interval'] = data['interval'].astype('int')
    data = data.drop('time', axis=1)
    
    # convert long form data to wide form
    
    data = data.pivot_table(index=['loop_detector_ID'], columns='interval', values='traffic')
    data_collect.append(np.array(data))

data_tensor = np.array(data_collect) # to a 3D array (a tensor): (day x detector x time interval)

np.save('results/detector_data_tensor', data_tensor) # save data with .npy format

# save the detector labels
data = data.reset_index()
data['loop_detector_ID'].to_csv('results/detector_order.csv')
#%%
# For Budapest
