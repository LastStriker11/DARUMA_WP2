# -*- coding: utf-8 -*-
"""
This program is used to convert the docomo data to tensors (# time intervals * # OD pairs * # variables).

@author: LQL
"""

import pandas as pd
import numpy as np
#%%
data_folder = '../Kyoto_data/docomo/OD/'
# samples needed to transform
list_data = ['01_total','02_residence(district)','03_residence(prefecture)'] # the "stay" data can be processed in a similar way
#%%
# construct a reference df to ensure all dfs (one per time interval) have the same dimension
df_area = pd.read_csv(data_folder+'selected_area.csv')
zone_id = df_area['mesh_code'].tolist()
zone_id.append(88888888)
od_pair = []
# list all possible OD pairs
for i in zone_id:
    for j in zone_id:
        od_pair.append([i,j])
df_ref = pd.DataFrame(od_pair)
df_ref.columns = ['area_origin','area_destination']
df_ref['residence'] = -1
df_ref['trip'] = 0
#%%
for file in list_data:
    data = pd.read_csv(data_folder+file+'.csv')
    cols = ['date','time','area_origin','area_destination','residence','trip']
    data = data[cols]
    # data['time'] = data['date'].astype(str) + ',' + data['time']
    # data = data.drop(['date'], axis=1)
    df_tensor = []
    for i in data['date'].unique():
        df_date = pd.DataFrame()
        for j in data['time'].unique():
            df_ref['date'] = i
            df_ref['time'] = j
            df0 = data[(data['date']==i)&(data['time']==j)]
            # merge two dfs and remove the redundancies
            df_time = df_ref.merge(df0, on=['date','time','area_origin','area_destination','residence','trip'], how='outer')
            df_time = df_time.drop_duplicates(subset=['area_origin','area_destination'], keep='last')
            df_time = df_time.sort_values(by=['area_origin','area_destination'])
            df_time = df_time.set_index(['area_origin','area_destination'])
            df_date = pd.concat([df_date, df_time['trip']], axis=1)
        df_tensor.append(np.array(df_date))
    
    df_tensor = np.array(df_tensor) # dimension: (# time intervals * # OD pairs * # variables)
    np.save('results/'+file+'_tensor', df_tensor) # save data with .npy format
