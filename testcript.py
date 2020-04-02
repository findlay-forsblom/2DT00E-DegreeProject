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
snowdepth.rename(columns={'Datum':'Date', 'Snö Djup':'Snow Depth'},inplace = True )

airtemp.drop(['Från Datum Tid (UTC)','Till Datum Tid (UTC)', 'Kvalitet'], axis=1,inplace = True)
airtemp.rename(columns={'Representativt dygn':'Date', 'Lufttemperatur':'Temp'},inplace = True )

fallAmount.drop(['Från Datum Tid (UTC)','Till Datum Tid (UTC)', 'Kvalitet'], axis=1,inplace = True)
fallAmount.rename(columns={'Representativt dygn':'Date', 'Nederbördsmängd':'Precip Amount'},inplace = True )

typeofFall.drop(['Från Datum Tid (UTC)','Till Datum Tid (UTC)', 'Kvalitet'], axis=1,inplace = True)
typeofFall.rename(columns={'Representativt dygn':'Date', 'Nederbörd':'Precipitation'},inplace = True )



luftFuktighet.rename(columns={'Datum':'Date', 'Relativ Luftfuktigh':'Luftfuktighet'},inplace = True )
grouped = luftFuktighet.groupby('Date')
luftFuktighet = grouped.mean()

dfs = [snowdepth, airtemp, fallAmount, typeofFall, luftFuktighet]

df_final = reduce(lambda left,right: pd.merge(left,right,on='Date', how='left'), dfs)

df_final['Precipitation']= df_final['Precipitation'].fillna(value='none')
df_final['Precip Amount']= df_final['Precip Amount'].fillna(value=0)

df_final[df_final['Temp'] < 10]

dataset = pd.merge(left=snowdepth, right=airtemp, left_on='Date', right_on='Date', how='outer')
dataset = pd.merge(left=dataset, right=typeofFall, left_on='Date', right_on='Date', how='outer')
dataset = pd.merge(left=dataset, right=fallAmount, left_on='Date', right_on='Date', how='outer')


snowdepth = snowdepth.iloc[:, [0, -1]].values
airtemp = airtemp.iloc[:, [-2, -1]].values
df1 = pd.DataFrame(airtemp, ['Date', 'Temp'])
df2 = pd.DataFrame(snowdepth)
df3 = pd.merge(df1, df2)
merged_inner = pd.merge(left=df1, right=df2, left_on=0, right_on=0)
    
"""
f = None
with open('./Datasets/snowdepth.csv') as fp:
  file = fp.readlines()
  #lines = lines.replace(";", ",")
  for row in file:
      line = row.replace(";", ",")
      line = line[:len(line)- 5]
      f = open("demofile2.csv", "a")
      f.write(line +'\n')
      print(line)
f.close()
"""

snowdepth = pd.read_csv('demofile2.csv')
      
"""
snowdepth = pd.read_csv('demofile2.csv')
fallamount = pd.read_csv('fallamount.csv')
typeofFall = pd.read_csv('typeofFall.csv')
airTemperature = pd.read_csv('airtemperature.csv')
"""
