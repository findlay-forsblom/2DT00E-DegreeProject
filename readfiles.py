#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 08:02:51 2020

@author: findlayforsblom
"""
import pandas as pd
import numpy as np
from functools import reduce

class ReadFiles:
    def __init__(self, files):
        self.files = files
        
        
    def createDataset(self):
        dataset = self.__readFromFile__()
        return dataset
    
    def __readFromFile__(self):
        files = self.files
        snowdepth = pd.read_csv(files[0], delimiter=';')
        airtemp = pd.read_csv(files[1], delimiter=';' )
        typeofFall = pd.read_csv(files[2],  delimiter=';' )
        fallAmount = pd.read_csv(files[3],delimiter=';')
        luftFuktighet = pd.read_csv(files[4], delimiter=';')
        (snowdepth, airtemp, typeofFall, fallAmount, luftFuktighet) =self.__dropColumns__(snowdepth, airtemp, typeofFall, fallAmount, luftFuktighet)
        
        col = snowdepth['Snow Depth']
        col.drop(col.head(1).index,inplace=True)
        col= col.append(pd.Series([6]), ignore_index=True)
        snowdepth['Depth +day1'] = col
        snowdepth.drop(snowdepth.tail(1).index,inplace=True)
        
        dfs = [snowdepth, airtemp]
        
        df_final = reduce(lambda left,right: pd.merge(left,right,on='Date', how='left'), dfs)
        
        df_final.dropna(inplace=True)
        dfs = [df_final, typeofFall, fallAmount, luftFuktighet]
        df_final = reduce(lambda left,right: pd.merge(left,right,on='Date', how='left'), dfs)
        
        dataset = df_final.copy()
        
        dataset['Precipitation']= dataset['Precipitation'].fillna(value='none')
        dataset['Precip Amount']= dataset['Precip Amount'].fillna(value=dataset['Precip Amount'].mean())
        dataset['Luftfuktighet'] = dataset['Luftfuktighet'].fillna(value=dataset['Luftfuktighet'].mean()) 
        dataset['Precip Amount'] = dataset['Precip Amount'] * (10**-3)
        
        return dataset
        
    
    def __dropColumns__(self, snowdepth, airtemp, typeofFall, fallAmount, luftFuktighet):
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
        
        return snowdepth, airtemp, typeofFall, fallAmount, luftFuktighet
    
        
        