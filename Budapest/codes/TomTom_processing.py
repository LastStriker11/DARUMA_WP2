# -*- coding: utf-8 -*-
"""
This pragram is used to process the TomTom link-based data (.json) from Budapest.
The user need to provide the path of data folder.
The outputs are saved in 'results/TomTom/', including the average speed,
average travel time and the number of probe vehicles.
The information of links is saved in a separate csv file: 'results/TomTom_link_info.csv'

@author: LOL
"""
import pandas as pd
import numpy as np
import os
import json
#%%
data_folder = '../Budapest_data/TomTom_FCD/district11_20220103_20220109/'
list_data = [f for f in os.listdir(data_folder) if f.endswith('.json')]  # please have a look at the order of the files
#%%
for file in list_data:
    with open(data_folder+file) as json_data:
        data = json.load(json_data) # load the json data
        
    df = pd.DataFrame(data['network']['segmentResults']) # convert the data into the dataframe format
    df = df.drop(['segmentId','streetName','shape','frc'], axis=1) # remove useless columns

    # averageSpeed, sampleSize, averageTravelTime
    for var in ['averageSpeed','sampleSize','averageTravelTime']:
        df_flat = []
        for index, p in df.iterrows():
            data_inter = pd.DataFrame(p.segmentTimeResults) # uncode the dictionary
            data_inter = data_inter['averageSpeed'].explode().tolist() # explode(): transform each element of a list-like to a row.
            df_flat.append(data_inter)
            
        df_flat = pd.DataFrame(df_flat)
        df_flat.columns = [i for i in range(2,26)] # change the column name
        df_flat.to_csv('results/TomTom/'+data['jobName'][-11:-1]+'_'+var+'.csv', index=None)
#%%
# export the link information
export_link_info = True
if export_link_info:
    df[['newSegmentId','speedLimit','distance']].to_csv('results/TomTom_link_info.csv', index=None)