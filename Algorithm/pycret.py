# -*- coding: utf-8 -*-
"""
Created on Sat May 16 11:43:54 2020

@author: findl
"""

from pycaret.datasets import get_data
diabetes = get_data('diabetes')

from pycaret.classification import *
exp1 = setup(diabetes, target = 'Class variable')

lol = compare_models()
