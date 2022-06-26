# -*- coding: utf-8 -*-
"""
This program is used to combine all twitter files and separate it into a tweet dataset and a user dataset.
These two datasets can be connected based on 'user.id' if needed.

@author: LQL
"""

import pandas as pd
import os
#%%
data_folder = '../Kyoto/Kyoto_data/twitter/with_geo_info/'
result_folder = 'results/'
#%%
list_data = [f for f in os.listdir(data_folder) if f.endswith('.csv')]
data = pd.DataFrame()
df_user = pd.DataFrame()
for file in list_data:
    df0 = pd.read_csv(data_folder+file)
    # information about tweets to save
    cols = ['coordinates.coordinates','created_at_localtime','entities.hashtags',
            'entities.user_mentions','lang','place.full_name',
            'favorite_count','quote_count','reply_count','retweet_count','text','user.id']
    # information about users to save
    cols_user = ['user.contributors_enabled','user.created_at','user.default_profile','user.description',
                 'user.default_profile_image','user.favourites_count','user.followers_count','user.friends_count',
                 'user.id','user.listed_count','user.location','user.name','user.profile_background_color',
                 'user.profile_background_tile','user.profile_link_color','user.profile_sidebar_border_color',
                 'user.profile_sidebar_fill_color','user.profile_text_color','user.profile_use_background_image',
                 'user.screen_name','user.statuses_count']
    data = pd.concat([data, df0[cols]], axis=0)
    df_user = pd.concat([df_user, df0[cols_user]], axis=0)
#%%
# remove duplicate users
df_user = df_user.drop_duplicates(['user.id'])
# coordinates
data['lon'] = data['coordinates.coordinates'].apply(lambda x: x.split(',')[0][1:])
data['lat'] = data['coordinates.coordinates'].apply(lambda x: x.split(',')[1][:-1])
data['lon'] = data['lon'].astype(float)
data['lat'] = data['lat'].astype(float)
data = data.drop(['coordinates.coordinates'], axis=1)

data.to_csv(result_folder+'twitter_data.csv', index=False)
df_user.to_csv(result_folder+'twitter_users.csv', index=False)
