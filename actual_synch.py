#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 18:37:19 2018

@author: chinta
"""

import pandas as pd

import numpy as np

#reading day and ight files
df_vem_night = pd.read_csv('/home/chinta/Documents/final_project/BIGDIVE7-dataset/VEM/cleaned_data/cleantop_2018_01_20_night.csv',
                           parse_dates=['date']).iloc[:,2:]

df_vem_day = pd.read_csv('/home/chinta/Documents/final_project/BIGDIVE7-dataset/VEM/cleaned_data/cleantop_2018_01_20_day.csv',
                         parse_dates=['date']).iloc[:,2:]


# joining day and night dataframe
df_vem = pd.concat([df_vem_day, df_vem_night], axis = 0)

del df_vem_night, df_vem_day


#creating a minute column from hour and minute
df_vem['minute'] = df_vem['date'].dt.hour *60 + df_vem['date'].dt.minute
df_vem = df_vem.sort_values(by = ['date'])


#an axulary column for later use in groupby
df_vem['counter'] = np.ones(df_vem.shape[0])

#setting the initial and final time from vem
initial_time = list(pd.to_datetime(df_vem['date']))[0]
final_time = list(pd.to_datetime(df_vem['date']))[-1]

#################################################################

#reading inrim file: 
#------------------ CHECK the date-------------------------

df_inrim_20 = pd.read_csv('/home/chinta/Documents/final_project/BIGDIVE7-dataset/INRIM/per Topix/180120_05Hz_epoch.csv', 
                          header = None, names = ['datetime', 'amplitude'])

#converting to date time and adding the daylight saving time
df_inrim_20.datetime = df_inrim_20.datetime + 60*60


#making a column only with minutes
df_inrim_20['datetime'] = pd.to_datetime(df_inrim_20['datetime'],unit='s')
df_inrim_20['minute'] = df_inrim_20['datetime'].dt.hour * 60 + df_inrim_20['datetime'].dt.minute


#slecting the data between the initial and final time
df_inrim_20 = df_inrim_20[(df_inrim_20['datetime'] > initial_time) & (df_inrim_20['datetime'] < final_time)]

#taking absolute amplitude
df_inrim_20['abs_amplitude'] = df_inrim_20.amplitude.apply(np.abs)


#counting mean fibre noise by minute. a form of re - sampling
fibre_noise_mean = df_inrim_20.groupby('minute', as_index=False).agg({"abs_amplitude": "mean"})

#moving average for smoothing by hour
fibre_noise_mean['mva'] = fibre_noise_mean.abs_amplitude.rolling(60).mean() 


#counting number of car per minute
vem_traffic_sum = df_vem.groupby('minute', as_index=False).agg({"counter": "sum"})


#synchronized file
synchronized_df = fibre_noise_mean.merge(vem_traffic_sum, how='outer')


# plotting different part of the synchronized file
import matplotlib.pyplot as plt

fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(5,15))

synchronized_df.plot(x='minute', y='mva', style='k.', ax=axes[0])
synchronized_df.plot(x='minute', y='counter', style='k.', ax=axes[1])
synchronized_df.plot(x='mva', y='counter', style='k.', ax=axes[2])

#plot cross-correlation
synchronized_df = synchronized_df.fillna(value = 0.) #send nan values due to the moving average to 0 and also due to merge
axes[3].xcorr(synchronized_df.mva.values, synchronized_df.counter.values, \
  usevlines=True, maxlags=10, normed=True, lw=2)






