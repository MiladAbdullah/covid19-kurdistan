# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 16:23:30 2020

@author: Milad
"""

import pandas as pn
import matplotlib.pyplot as plt
import numpy as np


LATEST_DATE = 16

def plot_actives (filename):
    labels = ['Erbil','Sulaymaniyah','Duhok','Halabja']
    
    recovered = [int(total_data[k][1]) for k in labels]
    death = [int(total_data[k][2]) for k in labels]
    active_case = [int(total_data[k][3]) for k in labels]
    x = np.arange(len(labels))  # the label locations
    fig, ax = plt.subplots()
    width = 0.25  # the width of the bars
    
    rects1 = ax.bar(x-width , recovered, width, label='Recovered')
    rects2 = ax.bar(x , death, width, label='Death')
    rects3 = ax.bar(x+width , active_case, width, label='Active Cases')
    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)
    
    ax.set_ylabel('Cases')
    ax.set_title('COVID-19 Status in Kurdistan Region - Iraq\n Between March 1 & September %d, 2020'%LATEST_DATE)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_xlabel('Provinces of Kurdistan Region - Iraq ')
    ax.legend()
    plt.ylim(0,max(recovered+death+active_case)+1000)
    #fig.tight_layout()
    plt.savefig('%s.png'%filename, dpi=300)
    
    
def plot_per_capital (filename):
    labels = ['Erbil','Sulaymaniyah','Duhok','Halabja']
    population = {
     'Erbil':1986.113,
     'Sulaymaniyah':2082.832,
     'Duhok':1397.515,
     'Halabja':111.355,
     }
    
    digit_level=3
    
    totalcases = [round(total_data[k][0]/population[k],digit_level) for k in labels]
    death = [round(total_data[k][2]/population[k],digit_level) for k in labels]

    x = np.arange(len(labels))  # the label locations
    fig, ax = plt.subplots()
    width = 0.35  # the width of the bars
    
    rects1 = ax.bar(x-width , totalcases, width, label='Total Cases')
    rects2 = ax.bar(x , death, width, label='Death')

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
    autolabel(rects1)
    autolabel(rects2)
    
    ax.set_ylabel('Cases per 1000 residents')
    ax.set_title('COVID-19 Prevalence per 1000 residents in Kurdistan Region - Iraq\n Between March 1 & September %d, 2020'%LATEST_DATE)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_xlabel('Provinces of Kurdistan Region - Iraq ')
    ax.legend()
    plt.ylim(0,max(totalcases+death)+1)
    #fig.tight_layout()
    plt.savefig('%s.png'%filename, dpi=300)
    

def plot_per_gender (filename):
    category_names = ['Male', 'Female']
    labels = ['Erbil','Sulaymaniyah','Duhok','Halabja','Total']
    results={}
    for label in labels:
        results[label]=[total_data[label][4],total_data[label][5]]
   
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.get_cmap('Pastel2')(np.linspace(0, 1, data.shape[1]))

    fig, ax = plt.subplots(figsize=(13, 5))
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())
    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        ax.barh(labels, widths, left=starts, height=0.5, label=colname, color=color)
        xcenters = starts + widths / 2
    
        
        text_color = 'black'
        for y, (x, c) in enumerate(zip(xcenters, widths)):
            ax.text(x, y, '%0.2f%%'%round(c*100,2), ha='center', va='center', color=text_color)
    ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1), loc='lower left')
    #ax.set_ylabel('Provinces')
    plt.tight_layout()
    #ax.set_title('COVID-19 cases of gender rates in Kurdistan Region - Iraq\n Between March 1 & September %d, 2020\n'%LATEST_DATE)
    ax.set_xlabel('COVID-19 Cas')
    plt.savefig('%s.png'%filename, dpi=300)
    
def plot_per_age (filename):
    category_names = ['Above 70','60-69','50-59','40-49','30-39','20-29','Under 20']
    labels = ['Erbil','Sulaymaniyah','Duhok','Halabja','Total']
    results={}
    for label in labels:
        results[label]=[]
        for i in range(len(category_names)):
            results[label].append(total_data[label][i+6])
   
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.get_cmap('Pastel2')(np.linspace(0, 1, data.shape[1]))

    fig, ax = plt.subplots(figsize=(13, 5))
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())
    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        ax.barh(labels, widths, left=starts, height=0.5, label=colname, color=color)
        xcenters = starts + widths / 2
    
        
        text_color = 'black'
        for y, (x, c) in enumerate(zip(xcenters, widths)):
            if i%2==1:
                va='top'
            else:
                va='bottom'
            print(i)
            ax.text(x, y, '%0.1f%%'%round(c*100,2), ha='center', va=va, color=text_color)
    ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1), loc='lower left')
    #ax.set_ylabel('Provinces')
    plt.tight_layout()
    #ax.set_title('COVID-19 cases of age rates in Kurdistan Region - Iraq\n Between March 1 & September %d, 2020\n'%LATEST_DATE)
    ax.set_xlabel('COVID-19 Cas')
    plt.savefig('%s.png'%filename, dpi=300)
    
#def plot_per_gender (filename):
#    labels = ['Erbil','Sulaymaniyah','Duhok','Halabja','Total']
#
#    male = [int(total_data[k][4]*100) for k in labels]
#    female = [int(total_data[k][5]*100) for k in labels]
#
#    x = np.arange(len(labels))  # the label locations
#    fig, ax = plt.subplots()
#    width = 0.20  # the width of the bars
#    
#    rects1 = ax.bar(x-width , male, width, label='Male')
#    rects2 = ax.bar(x , female, width, label='Female')
#
#    def autolabel(rects):
#        """Attach a text label above each bar in *rects*, displaying its height."""
#        for rect in rects:
#            height = rect.get_height()
#            ax.annotate('{}'.format(height),
#                        xy=(rect.get_x() + rect.get_width() / 2, height),
#                        xytext=(0, 3),  # 3 points vertical offset
#                        textcoords="offset points",
#                        ha='center', va='bottom')
#    autolabel(rects1)
#    autolabel(rects2)
#    
#    ax.set_ylabel('Percentage of Cases')
#    ax.set_title('COVID-19 cases of gender rates in Kurdistan Region - Iraq\n Between March 1 & September %d, 2020'%LATEST_DATE)
#    ax.set_xticks(x)
#    ax.set_xticklabels(labels)
#    ax.set_xlabel('Provinces of Kurdistan Region - Iraq ')
#    ax.legend()
#    plt.ylim(0,100)
#    #fig.tight_layout()
#    plt.savefig('%s.png'%filename, dpi=300)
    

def plot_total_pie (filename):
    group_names=["%s: %d"%(total_data['Attribute'][k],total_data['Total'][k]) for k in range(1,4)]
    group_size=[total_data['Total'][k] for k in range(1,4)]
    # Create colors
    main_colors=['forestgreen','Black','darkorange']

    fig, ax = plt.subplots()
    ax.axis('equal')
    mypie, _ = ax.pie(group_size, radius=0.7, labels=group_names, colors= main_colors )
    plt.setp( mypie, width=0.3, edgecolor='white')
    ax.set_title('COVID-19 Total Cases in Kurdistan Region - Iraq\n Between March 1 & September %d, 2020\n Total Cases: %d'%(LATEST_DATE,total_data['Total'][0]))
    plt.legend(loc=(0.9, 0.1))
    handles, labels = ax.get_legend_handles_labels()
    plt.tight_layout()
    plt.savefig('%s.png'%filename, dpi=300)
    
def plot_detail_pie (filename):
    labels = ['Erbil','Sulaymaniyah','Duhok','Halabja']
    group_names=["%s: %d"%(total_data['Attribute'][k],total_data['Total'][k]) for k in range(1,4)]
    group_size=[total_data['Total'][k] for k in range(1,4)]
    
    # for more beuaty
    group_size.insert(1,400)
    group_size.insert(3,400)
    group_size.insert(0,400)
    group_names.insert(1,'')
    group_names.insert(3,'')
    group_names.insert(0,'')
    # Create colors
    main_colors=['white','forestgreen','white','Black','white','darkorange']
    province_colors=[]
    subgroup_names_legs=labels
    subgroup_names=[]
    subgroup_size=[]
    for k in range(1,4):
        subgroup_size.extend( [total_data[l][k] for l in labels])
        subgroup_names.extend([int(total_data[l][k]) for l in labels])
        province_colors.extend(['silver','lightsteelblue','wheat','pink'])
            

    subgroup_size.insert(8,400)
    subgroup_size.insert(4,400)
    subgroup_size.insert(0,400)
    subgroup_names.insert(8,'')
    subgroup_names.insert(4,'')
    subgroup_names.insert(0,'')
    province_colors.insert(8,'white')
    province_colors.insert(4,'white')
    province_colors.insert(0,'white')
    
    fig, ax = plt.subplots()
   
    ax.set_title('COVID-19 Total Cases in Kurdistan Region - Iraq\n Between March 1 & September %d, 2020\n Total Cases: %d'%(LATEST_DATE,total_data['Total'][0]))
    ax.axis('equal')
    mypie, _ = ax.pie(group_size, radius=0.9, labels=group_names, colors= main_colors )
    plt.setp( mypie, width=0.1, edgecolor='white')
    
    # Second Ring (Inside)
    explode = (0, 0,0,0,0,0,0.1,0.1,0.1,0.05,0,0,0, 0, 0) 
    mypie2, _ = ax.pie(subgroup_size, explode=explode, radius=0.9-0.2,labels=subgroup_names, labeldistance=0.8, colors=province_colors,textprops={'fontsize': 4})
    
    plt.setp( mypie2, width=0.3)
    plt.margins(0,0)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[3:], subgroup_names_legs, loc=(0.9, 0.1))
    plt.tight_layout()
    plt.savefig('%s.png'%filename, dpi=300)

def plot_time_series(collection,title,filename):
    fig, ax = plt.subplots()
    for sample in collection:
        line1, = ax.plot(collection[sample][0], 
                         collection[sample][1], label=sample)
        if len(collection[sample][0])<100:
            plt.xticks(rotation=90)
    
    
    ax.set_title(title)
    ax.legend()
    ax.set_ylabel('Number of Cases')
    ax.set_xlabel('Date')
    plt.grid(True)
    
    plt.savefig('%s.png'%filename, dpi=300)
    
def plot_detail_iraq (filename):
    
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    #labels = ['Erbil','Sulaymaniyah','Duhok','Halabja']
    # Example data
    cities = iraq_data['city']
    y_pos = np.arange(len(cities))
    cases = iraq_data['Total Cases']
    ax.barh(y_pos, cases, align='center')
    for index, value in enumerate(cases):
        plt.text(value, index, str(value),va='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(cities)
    plt.xlim(0,max(cases)*1.2)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Total COVID-19 Cases')
    ax.set_ylabel('Iraq Provinces')
    ax.set_title('COVID-19 Total Cases in Iraq\n Between March 1 & September %d, 2020\n Total Cases: %d'%(LATEST_DATE,sum(iraq_data['Total Cases'][:])))
    plt.tight_layout()
    plt.savefig('%s.png'%filename, dpi=300)

def plot_rate_iraq (filename):
    
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    kurdistan_region = ['Erbil','Sulaymaniyah','Duhok','Halabja']
    iraq_cities = []
    kurdistan_cities =[]
    iraq_cases =[]
    kurdistan_cases =[]
    for index, value in enumerate(iraq_data['city']):
        if iraq_data['city'][index] in kurdistan_region:
            kurdistan_cities.append(iraq_data['city'][index])
            kurdistan_cases.append(iraq_data['infection rate'][index])
        else:
            iraq_cities.append(iraq_data['city'][index])
            iraq_cases.append(iraq_data['infection rate'][index])
    # Example data
    #iraq_cities = iraq_data['city'][0:14]
    #kurdistan_cities = iraq_data['city'][15:]
   
    #iraq_cases = iraq_data['infection rate'][0:14]
    #kurdistan_cases = iraq_data['infection rate'][15:]
    ax.barh(iraq_cities, iraq_cases,label="Iraqi Provinces", align='center')
    ax.barh(kurdistan_cities, kurdistan_cases,label="Kurdistan Region Provinces", align='center')
    for index, value in enumerate(iraq_cases):
        plt.text(value, index, round(value,2),va='center')
    for index, value in enumerate(kurdistan_cases):
        plt.text(value, index+15, round(value,2),va='center')
    
    #ax.set_yticklabels(cities)
    plt.xlim(0,20)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Total COVID-19 cases per 1000 resident')
    ax.set_ylabel('Provinces')
    ax.legend()
    ax.set_title('COVID-19 cases per 1000 resident in Iraq\n Between March 1 & September %d, 2020\n'%LATEST_DATE)
    plt.tight_layout()
    plt.savefig('%s.png'%filename, dpi=300) 

def plot_deathrate_iraq (filename):
    
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    kurdistan_region = ['Erbil','Sulaymaniyah','Duhok','Halabja']
    iraq_cities = []
    kurdistan_cities =[]
    iraq_cases =[]
    kurdistan_cases =[]
    for index, value in enumerate(iraq_data['city']):
        if iraq_data['city'][index] in kurdistan_region:
            kurdistan_cities.append(iraq_data['city'][index])
            kurdistan_cases.append(iraq_data['death per case'][index])
        else:
            iraq_cities.append(iraq_data['city'][index])
            iraq_cases.append(iraq_data['death per case'][index])
    #iraq_cities = iraq_data['city'][0:14]
    #kurdistan_cities = iraq_data['city'][15:]
   
    #iraq_cases = iraq_data['death per case'][0:14]
    #kurdistan_cases = iraq_data['death per case'][15:]
    ax.barh(iraq_cities, iraq_cases,label="Iraqi Provinces", align='center')
    ax.barh(kurdistan_cities, kurdistan_cases,label="Kurdistan Region Provinces", align='center')
    for index, value in enumerate(iraq_cases):
        plt.text(value, index, round(value,3),va='center')
    for index, value in enumerate(kurdistan_cases):
        plt.text(value, index+15, round(value,3),va='center')
    
    #ax.set_yticklabels(cities)
    plt.xlim(0,0.1)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Total COVID-19 death per case')
    ax.set_ylabel('Provinces')
    ax.legend()
    ax.set_title('COVID-19 death per case in Iraq\n Between March 1 & September %d, 2020\n'%LATEST_DATE)
    plt.tight_layout()
    plt.savefig('%s.png'%filename, dpi=300) 
    
def plot_iraq_neighbour (filename):
    
    fig = plt.figure(figsize=(7, 5))
    ax = fig.add_subplot(111)
    #labels = ['Erbil','Sulaymaniyah','Duhok','Halabja']
    # Example data
    iraq = [middle_east['country'][0]]
    neighbour = middle_east['country'][1:]
   

    iraq_cases = [middle_east['case per 1000'][0]]
    neighbour_cases = middle_east['case per 1000'][1:]
    
    ax.barh(iraq, iraq_cases,label="Iraq", align='center')
    ax.barh(neighbour, neighbour_cases,label="Iraq Neighbours", align='center')
 
        
    for index, value in enumerate(iraq_cases):
        plt.text(value, index, round(value,2),va='center')

    for index, value in enumerate(neighbour_cases):
        plt.text(value, index+1, round(value,2),va='center')
    
    #ax.set_yticklabels(cities)
    plt.xlim(0,30)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Total COVID-19 cases per 1000 resident')
    ax.set_ylabel('Countries')
    ax.legend()
    ax.set_title('COVID-19 cases per 1000 resident in Iraq and its Neighbour Countries\n Between March 1 & September %d, 2020\n'%LATEST_DATE)
    plt.tight_layout()
    plt.savefig('%s.png'%filename, dpi=300) 
    
def plot_iraq_neighbour_death (filename):
    
    fig = plt.figure(figsize=(7, 5))
    ax = fig.add_subplot(111)
    #labels = ['Erbil','Sulaymaniyah','Duhok','Halabja']
    # Example data
    iraq = [middle_east['country'][0]]
    neighbour = middle_east['country'][1:]
   

    iraq_cases = [middle_east['death per 1000'][0]]
    neighbour_cases = middle_east['death per 1000'][1:]
    
    ax.barh(iraq, iraq_cases,label="Iraq", align='center')
    ax.barh(neighbour, neighbour_cases,label="Iraq Neighbours", align='center')
 
        
    for index, value in enumerate(iraq_cases):
        plt.text(value, index, round(value,2),va='center')

    for index, value in enumerate(neighbour_cases):
        plt.text(value, index+1, round(value,2),va='center')
    
    #ax.set_yticklabels(cities)
    plt.xlim(0,0.1)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Total COVID-19 death per case')
    ax.set_ylabel('Countries')
    ax.legend(loc=4)
    ax.set_title('COVID-19 Death per Case in Iraq and its Neighbour Countries \nBetween March 1 & September %d, 2020\n'%LATEST_DATE)
    plt.tight_layout()
    plt.savefig('%s.png'%filename, dpi=300) 

def get_data():
    total_data = pn.read_excel('../TotalData.xlsx')
    labels = ['Erbil','Sulaymaniyah','Duhok','Halabja','Total']
    times = {
            lab:pn.read_excel('../Kurdistan Data.xlsx',sheet_name=lab,header=3)
            for lab in labels}
    
    computed = {T:[times[T]['Date'],
                   times[T]['New Case'],
                   times[T]['Total Cases']]
                for T in times
            }
    iraq_data = pn.read_excel('../IraqData.xlsx')
    middle_east = pn.read_excel('../MiddleEast.xlsx')
    return total_data,computed,iraq_data,middle_east

total_data,computed,iraq_data,middle_east= get_data()
#plot_actives('total_cases_per_province')
#plot_per_capital('total_cases_per_capita')
plot_per_gender('total_cases_gender')
plot_per_age('total_case_ages')
#plot_total_pie('total_pie_chart')
#plot_detail_pie('total_detail_chart')
#plot_time_series({'Kurdistan Region':computed['Total']},
#                 "COVID-19 Daily Cases in Kurdistan Region - Iraq\n Between March 1 & September 16, 2020",
#                 'time_series_kurdistan_region')
#plot_time_series({'Erbil Province':computed['Erbil']},
#                 "COVID-19 Daily Cases in Erbil, Kurdistan Region - Iraq\n Between March 1 & September 16, 2020",
#                 'time_series_erbil')
#plot_time_series({'Sulaymaniyah Province':computed['Sulaymaniyah']},
#                 "COVID-19 Daily Cases in Sulaymaniyah, Kurdistan Region - Iraq\n Between March 1 & September 16, 2020",
#                 'time_series_sulaymaniyah')
#plot_time_series({'Duhok Province':computed['Duhok']},
#                 "COVID-19 Daily Cases in Duhok, Kurdistan Region - Iraq\n Between March 1 & September 16, 2020",
#                 'time_series_Duhok')
#plot_time_series({'Halabja Province':computed['Halabja']},
#                 "COVID-19 Daily Cases in Halabja, Kurdistan Region - Iraq\n Between March 1 & September 16, 2020",
#                 'time_series_halabja')
#
#plot_time_series({'Kurdistan Region':[computed['Total'][0][0:91],computed['Total'][1][0:91]]},
#                 "COVID-19 Daily Cases in Kurdistan Region - Iraq\n Between March 1 & May 31, 2020",
#                 'time_series_kurdistan_march_may')
#plot_time_series({'Kurdistan Region':[computed['Total'][0][31:121],computed['Total'][1][31:121]]},
#                 "COVID-19 Daily Cases in Kurdistan Region - Iraq\n Between April 1 & June 30, 2020",
#                 'time_series_kurdistan_april_june')
#plot_time_series({'Kurdistan Region':[computed['Total'][0][61:152],computed['Total'][1][61:152]]},
#                 "COVID-19 Daily Cases in Kurdistan Region - Iraq\n Between May 1 & July 31, 2020",
#                 'time_series_kurdistan_may_july')
#plot_time_series({'Kurdistan Region':[computed['Total'][0][92:],computed['Total'][1][92:]]},
#                 "COVID-19 Daily Cases in Kurdistan Region - Iraq\n Between June 1 & September 16, 2020",
#                 'time_series_kurdistan_june_august')
#plot_time_series({'Erbil':computed['Erbil'],'Sulaymaniyah':computed['Sulaymaniyah'],'Duhok':computed['Duhok'],'Halabja':computed['Halabja']},
#                 "COVID-19 Daily Cases in Kurdistan Region - Iraq\n Between March 1 & September 16, 2020",
#                 'time_series_all_provinces')
#plot_time_series({'Cumulated':[computed['Total'][0],computed['Total'][2]]},
#                 "COVID-19 Cumulated Cases in Kurdistan Region - Iraq\n Between March 1 & September 16, 2020",
#                 'time_series_all_Cumulated')
#
#plot_detail_iraq('iraq_detail_cases')
#plot_rate_iraq('iraq_rate_cases')
#plot_deathrate_iraq('iraq_deathrate_cases')
#plot_iraq_neighbour_death('iraq_neighbours_cases_death')
#plot_iraq_neighbour('iraq_neighbours_cases')
