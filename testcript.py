#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 14:34:37 2020

@author: findlayforsblom
"""

import pandas as pd
import numpy as np
from functools import reduce

def convert2Csv(filename, writeFileName, num):
    w = open(writeFileName, "w")
    with open(filename) as fp:
      file = fp.readlines()
      #lines = lines.replace(";", ",")
      for row in file:
          line = row.replace(";", ",")
          line = line.strip()
          line = line[:num]
          w.write(line +'\n')
          print(line)
    w.close()
    return writeFileName 

filename = convert2Csv('./Datasets/snowdepth.csv','./Datasets/snowdepthnew.csv', -2)
snowdepth = pd.read_csv(filename)

filename = convert2Csv('./Datasets/airtemperature.csv','./Datasets/airtemperatureNew.csv', -2)
airtemp = pd.read_csv(filename)

filename = convert2Csv('./Datasets/typeofFall.csv','./Datasets/typeofFallNew.csv', -2)
typeofFall = pd.read_csv(filename)

filename = convert2Csv('./Datasets/fallamount.csv','./Datasets/fallamountNew.csv', -2)
fallAmount = pd.read_csv(filename)

filename = convert2Csv('./Datasets/humid','./Datasets/humid.csv', -2)
luftFuktighet = pd.read_csv(filename)

snowdepth.drop(['Tid (UTC)','Kvalitet'], axis=1,inplace = True)
snowdepth.rename(columns={'Datum':'Date', 'Snödjup':'Snow Depth'},inplace = True )

airtemp.drop(['Från Datum Tid (UTC)','Till Datum Tid (UTC)', 'Kvalitet'], axis=1,inplace = True)
airtemp.rename(columns={'Representativt dygn':'Date', 'Lufttemperatur':'Temp'},inplace = True )

fallAmount.drop(['Från Datum Tid (UTC)','Till Datum Tid (UTC)', 'Kvalitet'], axis=1,inplace = True)
fallAmount.rename(columns={'Representativt dygn':'Date', 'Nederbördsmängd':'Precip Amount'},inplace = True )

typeofFall.drop(['Från Datum Tid (UTC)','Till Datum Tid (UTC)', 'Kvalitet'], axis=1,inplace = True)
typeofFall.rename(columns={'Representativt dygn':'Date', 'Nederbörd':'Precipitation'},inplace = True )

luftFuktighet.rename(columns={'Datum':'Date', 'Relativ Luftfuktigh':'Luftfuktighet'},inplace = True )

grouped = luftFuktighet.groupby('Date')
luftFuktighet = grouped.mean()

dfs = [snowdepth, airtemp, typeofFall, fallAmount, luftFuktighet]

df_final = reduce(lambda left,right: pd.merge(left,right,on='Date', how='left'), dfs)

dataset = df_final.copy()

dataset['Precipitation']= dataset['Precipitation'].fillna(value='none')
dataset['Precip Amount']= dataset['Precip Amount'].fillna(value=0)
dataset['Precip Amount'] = dataset['Precip Amount'] * (10**-3) 

#test = df_final.copy()
col = df_final['Snow Depth']
 
col.drop(col.head(1).index,inplace=True)
col= col.append(pd.Series([6]), ignore_index=True)

dataset['Depth +day1'] = col
dataset.drop(dataset.tail(1).index,inplace=True)
dataset.dropna(inplace=True) #Drops only the missing temperature values


dataset[dataset['Temp'] < 10]
