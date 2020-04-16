# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 21:08:57 2020

@author: Milad
"""

# Exponential smoothing

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure 
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt


def Simple(_data, _alpha=0, _optimized=False):
    if _alpha>0:
        fit = SimpleExpSmoothing(_data).fit(smoothing_level=_alpha,optimized=_optimized)
    else:
        fit = SimpleExpSmoothing(_data).fit()
    return fit

def Forecast(models,steps):
    casts = {}
    for model in models:
        casts[model] = [cast.forecast(steps) for cast in models[model]]
    return casts


def PlotSimple (forecast_list, 
                real_data,
                models,
                filename,
                color_list):
    figure(num=None, figsize=(8, 6), dpi=300, facecolor='w', edgecolor='k')
    pl = real_data.plot(color='black',label='Real Observations',legend=True)
    
    #for fore in forecast_list:
        #fore.rename(r'$\alpha=%s$'%fore.model.params['smoothing_level'])
    
    for i in range(0,3):
        forecast_list[i].rename(r'$\alpha=%s$'%models[i].model.params['smoothing_level']).plot(ax=pl, color=color_list[i], marker="o", legend=True)
        models[i].fittedvalues.plot(ax=pl, label='',color=color_list[i],legend=False)
    # naming the x axis 
    plt.xlabel('Dates') 
    # naming the y axis 
    plt.ylabel(filename) 
    # giving a title to my graph 
    plt.title('Exponential Smoothing Model for Confirmed Cases in Kurdistan-Iraq') 
    plt.xticks(rotation=90)
    plt.grid()
    # show a legend on the plot 
    plt.legend() 
    plt.savefig('../charts/Models/Simple_%s.png'%filename)