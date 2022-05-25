# -*- coding: utf-8 -*-
"""
This is for the archived historical detector data.

Notice: the speed tensor includes all detectors. 
However, only part of them (i.e., inter-city motorways) have speeds.
But we did not filter them out as we we did in the program for streaming data.

@author: LQL
"""

import pandas as pd
import numpy as np
import os
#%%
t_interval = 15 # can not be changed in this script!!!
data_folder = '../Madrid_data/detector_historical_data/'
#%%
list_data = [f for f in os.listdir(data_folder) if f.endswith('.csv')]  # please have a look at the order of the files
cols = ['id', 'fecha', 'intensidad', 'ocupacion', 'carga', 'vmed']
cols_new = ['loop_detector_ID', 'time', 'volume', 'occupancy', 'load_para', 'speed']

for file in list_data: # iterate month
    # read data
    data1 = pd.read_csv(data_folder+file, sep=';')
    data1 = data1[cols]
    data1.columns = cols_new
    data1['time'] = pd.to_datetime(data1['time']) # notice the format of the time
    data1['day'] = (data1['time'] - data1.loc[0,'time']).dt.days # create a column to indicate days
    
    for var in ['speed', 'volume', 'occupancy', 'load_para']: # iterate variables
        data_collect = []
        index_collect = [] # not all detectors have data in all days 
        for d in data1['day'].unique(): # iterate days
            
            data = data1.loc[data1['day']==d, :]
            
            data = data.reset_index(drop=True)
            data['interval'] = (data['time'] - data.loc[0,'time']).dt.total_seconds()/(t_interval*60) # a column indicating intervals
            data['interval'] = data['interval'].astype('int')
            data = data.drop('time', axis=1)
            data = data[data['interval']!=int(60*24/t_interval)] # exclude the data from the next day
            
            # convert long form data to wide form
            data = data.pivot_table(index=['loop_detector_ID'], columns='interval', values=var)
            index_collect.append(data.index)
            data_collect.append(data)
        
        # find the common index
        index_common = index_collect[0]
        for d in range(len(index_collect)-1):
            index_common = index_common.intersection(index_collect[d+1])
        for d in range(len(data_collect)):
            data_collect[d] = np.array(data_collect[d].loc[index_common,:])
            
        data_tensor = np.array(data_collect) # to a 3D array (a tensor): (day x detector x time interval)
        np.save('results/detector_historical_data_'+var+'_'+file[:7]+'_tensor', data_tensor) # save data with .npy format
    
    # save the detector labels
    data = data.reset_index()
    data['loop_detector_ID'].to_csv('results/detector_order_historical_'+file[:7]+'.csv')