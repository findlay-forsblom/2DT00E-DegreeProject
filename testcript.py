#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 14:34:37 2020

@author: findlayforsblom
"""

import pandas as pd
import numpy as np
from functools import reduce

snowdepth = pd.read_csv('./Datasets/SnowDepth.csv', delimiter=';')

airtemp = pd.read_csv('./Datasets/Airtemperature.csv', delimiter=';' )

typeofFall = pd.read_csv('./Datasets/Precipitation.csv',  delimiter=';' )

fallAmount = pd.read_csv('./Datasets/FallAmount.csv',delimiter=';')

luftFuktighet = pd.read_csv('./Datasets/humidity.csv', delimiter=';')

snowdepth.drop(['Tid (UTC)','Kvalitet', 'Unnamed: 4', 'Unnamed: 5'], axis=1,inplace = True)
snowdepth.rename(columns={'Datum':'Date', 'Snödjup':'Snow Depth'},inplace = True )

airtemp.drop(['Från Datum Tid (UTC)','Till Datum Tid (UTC)', 'Kvalitet', 'Unnamed: 5', 'Unnamed: 6'], axis=1,inplace = True)
airtemp.rename(columns={'Representativt dygn':'Date', 'Lufttemperatur':'Temp'},inplace = True )

fallAmount.drop(['Från Datum Tid (UTC)','Till Datum Tid (UTC)', 'Kvalitet', 'Unnamed: 5', 'Unnamed: 6'], axis=1,inplace = True)
fallAmount.rename(columns={'Representativt dygn':'Date', 'Nederbördsmängd':'Precip Amount'},inplace = True )

typeofFall.drop(['Från Datum Tid (UTC)','Till Datum Tid (UTC)', 'Kvalitet', 'Unnamed: 5', 'Unnamed: 6'], axis=1,inplace = True)
typeofFall.rename(columns={'Representativt dygn':'Date', 'Nederbörd':'Precipitation'},inplace = True )

luftFuktighet.drop(['Unnamed: 4', 'Unnamed: 5', 'Tid (UTC)','Kvalitet'], axis=1,inplace = True)
luftFuktighet.rename(columns={'Datum':'Date', 'Relativ Luftfuktighet':'Luftfuktighet'},inplace = True )

grouped = luftFuktighet.groupby('Date')
luftFuktighet = grouped.mean()

dfs = [snowdepth, airtemp, typeofFall, fallAmount, luftFuktighet]

df_final = reduce(lambda left,right: pd.merge(left,right,on='Date', how='left'), dfs)

dataset = df_final.copy()

dataset['Precipitation']= dataset['Precipitation'].fillna(value='none')
dataset['Precip Amount']= dataset['Precip Amount'].fillna(value=dataset['Precip Amount'].mean())
dataset['Luftfuktighet'] = dataset['Luftfuktighet'].fillna(value=dataset['Luftfuktighet'].mean()) 
dataset['Precip Amount'] = dataset['Precip Amount'] * (10**-3) 

#test = df_final.copy()
col = df_final['Snow Depth']
 
col.drop(col.head(1).index,inplace=True)
col= col.append(pd.Series([6]), ignore_index=True)

dataset['Depth +day1'] = col
dataset.drop(dataset.tail(1).index,inplace=True)
dataset.dropna(inplace=True) #Drops only the missing temperature values


dataset = dataset[dataset['Temp'] < 10]
