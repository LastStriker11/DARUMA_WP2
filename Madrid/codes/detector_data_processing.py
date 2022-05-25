# -*- coding: utf-8 -*-
"""
This one is for the real-time data processing.

@author: LQL
"""
import pandas as pd
import numpy as np
import os
import datetime
#%%
t_interval = 15 # in minutes
data_folder = '../Madrid_data/detector_data/' # the path of data
list_data = [f for f in os.listdir(data_folder) if f.endswith('.csv')]  # please have a look at the order of the files
#%%
# concatenate multiple data files
data1 = pd.DataFrame()
for file in list_data:
    year = int(file.split('_')[1][:4])
    month = int(file.split('_')[1][4:6])
    day = int(file.split('_')[1][6:8])
    hour = int(file.split('_')[1][9:11])
    minute = int(file.split('_')[1][11:13])
    second = int(file.split('_')[1][13:15])
    
    df = pd.read_csv(data_folder+file, encoding='latin-1') # latin-1 for decoding Spanish
    cols = ['idelem', 'intensidad', 'ocupacion', 'carga', 'velocidad']
    cols_new = ['loop_detector_ID', 'volume', 'occupancy', 'load_para', 'speed']
    df = df[cols]
    df.columns = cols_new
    
    df['time'] = datetime.datetime(year, month, day, hour, minute, second)
    data1 = pd.concat([data1, df], axis=0)
data1 = data1.reset_index(drop=True)
data1['day'] = (data1['time'] - data1.loc[0,'time']).dt.days
#%%
flag = 1 # for the purpose of only exporting the detector IDs for the speed tensor once.
for var in ['speed', 'volume', 'occupancy', 'load_para']: # iterate variables
    data_collect = []
    for d in data1['day'].unique():
        
        data_day = data1.loc[data1['day']==d, :]
        # for the speed data of inter-city motorways (because only these detectors have speed data)
        if var == 'speed':
            data_day = data_day.dropna(subset=['speed'])
        # average the volume (the original value is already in hour), occupancy and speed
        data = data_day.groupby([data_day.time.dt.floor(str(t_interval)+'T'),'loop_detector_ID'])[var].mean()
        data = data.reset_index(drop=False)
        data['interval'] = (data['time'] - data.loc[0,'time']).dt.total_seconds()/(t_interval*60) # identify interval IDs
        data['interval'] = data['interval'].astype('int')
        data = data.drop('time', axis=1)
        data = data[data['interval']!=int(60*24/t_interval)] # exclude the data from the next day
        
        # store the detector ID of inter-city motorways which have speed data
        if (var == 'speed') & flag:
            data = data.reset_index()
            data['loop_detector_ID'].to_csv('results/intercity_detector_order.csv')
            flag = 0
        
        # convert long form data to wide form
        data = data.pivot_table(index=['loop_detector_ID'], columns='interval', values=var)
        data_collect.append(np.array(data))
    
    data_tensor = np.array(data_collect) # to a 3D array (a tensor): (day x detector x time interval)
    np.save('results/detector_data_'+var+'_tensor', data_tensor) # save data with .npy format
    
# save the detector IDs
data = data.reset_index()
data['loop_detector_ID'].to_csv('results/detector_order.csv')
