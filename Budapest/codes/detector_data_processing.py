# -*- coding: utf-8 -*-
"""
@author: Qing-Long Lu
"""
import pandas as pd
import numpy as np
import os
#%%
t_interval = 10 # in minutes
data_folder = '../Budapest_data/LoopData/Detektor_measurements_1/'
#%%
list_data = [f for f in os.listdir(data_folder) if f.endswith('.csv')]  # please have a look at the order of the files
cols = ['Time', 'Long Name', 'processed_all_vol', 'processed_all_occ', 'processed_all_spd']
cols_new = ['Time', 'Long Name', 'volume', 'occupancy', 'speed']

for file in list_data:
    period = file.split('_')[-1][:6] # the time that the data were collected
    data1 = pd.read_csv(data_folder+file, sep=';')
    data1 = data1[cols]
    data1.columns = cols_new
    data1['Time'] = pd.to_datetime(data1['Time'], dayfirst=True) # notice the format of the time
    data1['day'] = (data1['Time'] - data1.loc[0,'Time']).dt.days
    
    for var in ['volume', 'occupancy', 'speed']:
        data_collect = []
        for d in data1['day'].unique():
            
            data_day = data1.loc[data1['day']==d, :]
            # sum up the traffic for every t_interval minutes
            data = data_day.groupby([data_day.Time.dt.floor(str(t_interval)+'T'),'Long Name'])[var].sum()
            data = data.reset_index(drop=False)
            data['interval'] = (data['Time'] - data.loc[0,'Time']).dt.total_seconds()/(t_interval*60) # identify interval IDs
            data['interval'] = data['interval'].astype('int')
            data = data.drop('Time', axis=1)
            data = data[data['interval']!=144] # exclude the data from the next day
            
            # convert long form data to wide form
            data = data.pivot_table(index=['Long Name'], columns='interval', values=var)
            data_collect.append(np.array(data))
        
        data_tensor = np.array(data_collect) # to a 3D array (a tensor): (day x detector x time interval)
        np.save('results/'+var+'_data_tensor'+period, data_tensor) # save data with .npy format
        
# save the detector labels
data = data.reset_index()
data['Long Name'].to_csv('results/detector_order.csv')