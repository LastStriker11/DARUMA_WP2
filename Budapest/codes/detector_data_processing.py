# -*- coding: utf-8 -*-
"""
This program is used to process the detector data from Budapest.
The user need to provide the data path and specify the time interval.
The outputs are saved in 'results/', including the speed tensor, occupancy tensor and traffic counts tensor.
The information of detectors is saved in a separate csv file: 'results/detector_order.csv'.

@author: LQL
"""
import pandas as pd
import numpy as np
import os
#%%
t_interval = 15 # in minutes
data_folder = '../Budapest_data/LoopData/Detektor_measurements_1/'
#%%
list_data = [f for f in os.listdir(data_folder) if f.endswith('.csv')]  # please have a look at the order of the files
cols = ['Time', 'Long Name', 'processed_all_vol', 'processed_all_occ', 'processed_all_spd']
cols_new = ['time', 'loop_detector_ID', 'counts', 'occupancy', 'speed']

for file in list_data: # iterate data files
    period = file.split('_')[-1][:6] # when the data were collected
    data1 = pd.read_csv(data_folder+file, sep=';')
    data1 = data1[cols]
    data1.columns = cols_new
    data1['time'] = pd.to_datetime(data1['time'], dayfirst=True) # notice the format of the time -> dayfirst=True
    data1['day'] = (data1['time'] - data1.loc[0,'time']).dt.days # create a column to indicate days
    
    for var in ['counts', 'occupancy', 'speed']: # iterate variables
        data_collect = []
        for d in data1['day'].unique(): # iterate days
            
            data_day = data1.loc[data1['day']==d, :] # data of the day
            # aggregate the data based on t_interval
            if var == 'counts':
                # sum up the counts
                data = data_day.groupby([data_day.time.dt.floor(str(t_interval)+'T'),'loop_detector_ID'])[var].sum()
            else:
                # average the occupancy and speed
                data = data_day.groupby([data_day.time.dt.floor(str(t_interval)+'T'),'loop_detector_ID'])[var].mean()
            
            data = data.reset_index(drop=False)
            data['interval'] = (data['time'] - data.loc[0,'time']).dt.total_seconds()/(t_interval*60) # create a column to indicate intervals
            data['interval'] = data['interval'].astype('int')
            data = data.drop('time', axis=1)
            data = data[data['interval']!=int(60*24/t_interval)] # exclude the data from the next day
            
            # convert long form data to wide form
            data = data.pivot_table(index=['loop_detector_ID'], columns='interval', values=var)
            data_collect.append(np.array(data))
        
        data_tensor = np.array(data_collect) # to a 3D array (a tensor): (day x detector x time interval)
        np.save('results/detector_data_'+var+'_tensor_'+period, data_tensor) # save data with .npy format
        
# save the detector labels
data = data.reset_index()
data['loop_detector_ID'].to_csv('results/detector_order.csv')