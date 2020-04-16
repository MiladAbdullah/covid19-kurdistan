# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 18:49:39 2020

@author: Milad
"""
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure 
import numpy as np
# web scraper
def TotalTrend (cities,times,filename="Total Trend"):
    plt.ion()
    figure(num=None, figsize=(8, 6), dpi=300, facecolor='w', edgecolor='k')
    for city in cities:
        plt.plot(times, cities[city], label = city) 

    # naming the x axis 
    plt.xlabel('Dates') 
    # naming the y axis 
    plt.ylabel(filename) 
    # giving a title to my graph 
    plt.title('COVID-19 in Kurdistan Region, March-April 2020') 
    plt.xticks(rotation=90)
    plt.grid()
    # show a legend on the plot 
    plt.legend() 
    plt.savefig('../charts/%s.png'%filename)
    # function to show the plot 
    #plt.show()

def showBarR (cities,times,filename="Total Trend Bar"):
    plt.ioff()
    figure(num=None, figsize=(8, 6), dpi=300, facecolor='w', edgecolor='k')
    for city in cities:
        plt.bar(times, cities[city], label = city) 
    plt.xlabel('Dates') 
    # naming the y axis 
    plt.ylabel(filename) 
    # giving a title to my graph 
    plt.title('COVID-19 in Kurdistan Region, March-April 2020') 
    plt.xticks(rotation=90)
    plt.grid()
    # show a legend on the plot 
    plt.legend() 
    plt.savefig('../charts/%s.png'%filename)

def showBar (k, g, times,filename='bar.png'):

    plt.bar(k,g, tick_label = times) 
        # naming the x axis 
    plt.xlabel('Dates') 
    # naming the y axis 
    plt.ylabel('Rates Per Person') 
    # giving a title to my graph 
    plt.title('COVID-19 in Kurdistan Region, March-April 2020') 
    plt.xticks(rotation=90)
    # show a legend on the plot 
    plt.legend() 
    plt.savefig('../charts/%s'%filename)
    # function to show the plot 
    plt.show()
    