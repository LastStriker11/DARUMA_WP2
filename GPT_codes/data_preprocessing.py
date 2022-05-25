# -*- coding: utf-8 -*-
"""
@author: LQL
"""

import pandas as pd
import numpy as np
import ast
import os
import pickle
import datetime
#%%
DATA_FOLDER = '../output/' # path to the raw GPT data
#%%
def data_info_stat():
    """
    Summarize the information of downloaded data.
    
    Parameters
    -------
    None.

    Returns
    -------
    info_file : DataFrame
        A DataFrame contains the information of all data files.

    """
    list_file = [f for f in os.listdir(DATA_FOLDER)] # all file names
    week_file = [] # store week info
    day_file = [] # store day info
    inter_file = [] # stor interval info
    w_pre = 0 # to store the previous week number
    for f in list_file:
        t = str.split(f, sep='_')[1]
        t, interval = str.split(t, sep='-')
        interval = interval[:2]
        w = datetime.datetime.strptime(t, '%Y%m%d').strftime('%U') # %Y: year, %m: month, %d: day, %U: week number of the year.
        if w == '00': # to avoid the uncompleteness of the last week of 2021 and the first week of 2022
            w = w_pre
        d = datetime.datetime.strptime(t, '%Y%m%d').strftime('%u') # %Y: year, %m: month, %d: day, %u: day of week, 1->Monday, 7->Sunday.
        w_pre = w
        week_file.append(w)
        day_file.append(d)
        inter_file.append(interval)
    info_file = pd.DataFrame(data={'file_name':list_file, 'week_year':week_file, 'day_week':day_file, 'interval': inter_file})
    return info_file
#%%
def gpt_list2df(info_file):
    """
    Convert raw popularity data (dictionary-based) to dataframe.

    Parameters
    ----------
    info_file : DataFrame
        Information of data files.

    Returns
    -------
    data : DataFrame
        Flat GPT data.

    """
    
    data = pd.DataFrame()
    for w in info_file['week_year'].unique():
        week_tmp = info_file.loc[info_file['week_year']==w, 'file_name']
        print('======GPT List to DataFrame')
        print('Week: %s' %(w))
        for f in week_tmp:
            print('Processing: %s'%f)
            data_poi = pd.read_csv(DATA_FOLDER+f)
            data_poi = data_poi[data_poi['popular_times']!='None']
            cols = ['lat','lon','node_type','popular_times','rating','rating_n','current_popularity']
            data_tmp = data_poi[cols]
            
            gpt_flat = []
            
            for index, p in data_tmp.iterrows():
                p_times = pd.DataFrame(ast.literal_eval(p.popular_times)) # decode dictionary
                p_times = p_times['data'].explode().tolist() # explode(): transform each element of a list-like to a row.
                gpt_flat.append(p_times)
            gpt_flat = pd.DataFrame(gpt_flat)
            
            gpt_flat = pd.concat([gpt_flat, data_tmp[['lat','lon']]], axis=1)
            gpt_flat['week_year'] = w
            gpt_flat = gpt_flat.dropna() # Cleaning 1: delete nan data
            data = pd.concat([data, gpt_flat], axis=0)
            data.drop_duplicates(inplace=True)
    
    data.set_index(['lat','lon'], inplace=True)
    return data
#%%
def gpt_clean(info_file, data):
    """
    Cleaning function for GPT data.

    Parameters
    ----------
    info_file : DataFrame
        Information of data files.
    data : DataFrame
        GPT data.

    Returns
    -------
    data_all : List
        List of cleaned GPT data, with each item a DataFrame for a week.
    index_common: MultiIndex
        POIs that have data in all weeks.

    """
    data_all = []
    data_sum = data.index.value_counts()
    pois_tmp = data_sum[data_sum>=N_W] # only POIs that update the historical popularity once a week are preserved.
    print('======Data Cleaning')
    for w in info_file['week_year'].unique(): # week_year is string
        print('==Processing week-%s.'%w)
        data_day = data.loc[data['week_year']==w, :]
        data_day = data_day.drop(labels='week_year', axis=1)
    
        data_day.reset_index(drop=False, inplace=True)
        data_day.drop_duplicates(inplace=True) # Cleaning 2: delete duplicates
        data_day.set_index(['lat','lon'], inplace=True)
        data_day = data_day[(data_day.T != 0).any()] # Cleaning 3: delete records with all 0
        data_day = data_day[data_day.index.isin(pois_tmp.index)] # Cleaning 4: delete pois without updating historical data at lease once a week
        
        records = []
        k = 0 # for iteration
        for j in data_day.index.unique():
            if k%100 == 0:
                print('--Processing pois %s-%s.'%(k,k+100))
            data_j = data_day.loc[data_day.index==j, :]
            
            # Cleaning 5: delete outliers (interquartile range) !!! you can commented it if you don't need it
            c = data_j.describe()
            q25, q75 = c.loc['25%', :], c.loc['75%', :]
            iqr = q75 - q25
            cut_off = iqr * 1.5
            lower, upper = q25 - cut_off, q75 + cut_off
            trust_values = []
            for i in range(24*7):
                inliers = [x for x in data_j[i] if x >= lower[i] and x <= upper[i]]
                # consider the data missing problem by examing the number of zeros (should be less than half)
                if len(data_j[data_j[i]==0])>(len(data_j)/2):
                    inliers = [x for x in data_j[i] if x >= lower[i] and x <= upper[i]]
                    trust_values.append(sum(inliers)/len(inliers))
                else:
                    inliers = [x for x in data_j[i] if x >= lower[i] and x <= upper[i] and x!=0]
                    trust_values.append(sum(inliers)/len(inliers)) # Cleaning 6: average values for those updating GPT more than once a week
            records.append(trust_values)
            k += 1
        data_day_avg = pd.DataFrame(records)
        data_day_avg.index = data_day.index.unique()
        data_all.append(data_day_avg)
    
    return data_all
#%%
def gpt_day_wise(data_all):
    """
    Split the data by day of week.

    Parameters
    ----------
    data_all : List
        List of cleaned GPT data, with each item a DataFrame for a week.

    Returns
    -------
    data_days : List
        List of cleaned GPT data, with each item a list of DataFrames for different week.

    """
    data_days = [] # [Mon, Tue, Wed, Thu, Fri, Sat, Sun]
    for i in range(7):
        data_week = []
        for w in range(N_W):
            data_tmp = data_all[w].iloc[:, 24*i:24*(i+1)]
            data_week.append(data_tmp)
        data_days.append(data_week)
    return data_days
#%%
def gpt_real_time(info_file, index_common):
    """
    Summarizing and preprocessing real-time data.

    Parameters
    ----------
    info_file : DataFrame
        Information of data files.

    Returns
    -------
    data_rt : DataFrame
        Real time GPT data of all time intervals considered.

    """
    data_rt = pd.DataFrame()
    print('======Real-time data')
    for w in info_file['week_year'].unique():
        week_tmp = info_file.loc[info_file['week_year']==w, :]
        print('Week: %s' %(w))
        for i, f in week_tmp.iterrows():
            print('Processing: %s'%f['file_name'])
            data_poi = pd.read_csv(DATA_FOLDER+f['file_name'])
            data_tmp = data_poi[(data_poi['current_popularity']!='None')&(data_poi['node_type']!='station')] # station data are excluded, but you can remove it
            cols = ['lat','lon','current_popularity']
            data_tmp = data_tmp[cols]
            data_tmp.dropna(inplace=True)
            data_tmp.drop_duplicates(inplace=True) # be careful, sometimes there are more than one records for one POI
            data_tmp['current_popularity'] = data_tmp['current_popularity'].astype(int)
            data_tmp = data_tmp[data_tmp['current_popularity']>=0]
            data_tmp.set_index(['lat','lon'], inplace=True)
            data_tmp.columns = [w+'_'+f['day_week']+'_'+f['interval']]
            data_rt = pd.concat([data_rt,data_tmp], axis=1)
    
    data_rt = data_rt[data_rt.index.isin(index_common)] # filter out those are not included in the common dataset
    return data_rt
#%%
if __name__ == '__main__':
    info_file = data_info_stat() # all data files
    N_W = len(info_file['week_year'].unique()) # number of weeks
    
    data = gpt_list2df(info_file) # Convert raw popularity data (dictionary-based) to dataframe.
    data_all = gpt_clean(info_file, data)
    del data
    
    # Cleaning 7: find the pois that have data in all weeks
    index_common = data_all[0].index
    for w in range(N_W-1):
        index_common = index_common.intersection(data_all[w+1].index)
    for w in range(N_W):
        data_all[w] = data_all[w].loc[index_common,:]
    
    # store the information of venues
    df = pd.read_csv(DATA_FOLDER+info_file.loc[0,'file_name'])
    info_venue = df[['lat','lon','node_type','rating','rating_n']]
        
    # split the data by day
    data_days = gpt_day_wise(data_all)
    
    # processing real-time data
    data_rt = gpt_real_time(info_file, index_common)
    
    f = open('results/data_processed.pckl', 'wb')
    pickle.dump([data_all,data_days,data_rt,index_common,info_file,info_venue], f)
    f.close()
    

































