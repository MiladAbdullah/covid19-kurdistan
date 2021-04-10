# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 14:47:39 2020

@author: Milad
"""


import numpy as np
import pandas as pn
import matplotlib.pyplot as plt
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
import random
import math

def read_files ():
    labels = ['Erbil','Sulaymaniyah','Duhok','Halabja','Total']
    times = {
            lab:pn.read_excel('../Kurdistan Data.xlsx',sheet_name=lab,header=3)
            for lab in labels}
    
    computed = {T:[times[T]['Date'],
                   times[T]['New Case'],
                   times[T]['Total Cases']]
                for T in times
            }
    return computed

def plot_time_series(collection,title,filename):
    fig = plt.figure(figsize=(7, 5))
    ax = fig.add_subplot(111)
    colors = ['black','green','blue','red','yellow']
    for i,sample in enumerate(collection):
        if collection[sample][1]==None:
            line1, = ax.plot(collection[sample][0],color=colors[i], label=sample)
        else:
            line1, = ax.plot(collection[sample][0],color=colors[i], marker=".", label=sample,linewidth=0.2)
        
    
    for i,sample in enumerate(collection):
        if collection[sample][1]==None:
            continue
        line2, = ax.plot(collection[sample][1].fittedvalues,color=colors[i],linestyle='dashed', markersize=4)
    
    plt.xticks(rotation=90)
    ax.set_title(title)
    ax.legend()
    ax.set_ylabel('Number of Cases')
    ax.set_xlabel('Date')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('%s.png'%filename, dpi=300)


def TrainSimple(train_data,real_data,prediction_days):

    fit1 = ExponentialSmoothing(train_data).fit(smoothing_level=0.1,optimized=True)
    fit2 = ExponentialSmoothing(train_data).fit(optimized=True)
    fit3 = ExponentialSmoothing(train_data).fit(smoothing_level=0.9,optimized=True)

    fcast1 = fit1.forecast(prediction_days)
    fcast2 = fit2.forecast(prediction_days)
    fcast3 = fit3.forecast(prediction_days)

    plot_time_series(
            {
                    r'Real Data':[real_data,None],
                    r'1.Simple Exponential, $\alpha=%0.2f$'%fit1.params['smoothing_level']:[fcast1,fit1],
                    r'2.Simple Exponential, $\alpha=%0.2f$'%fit2.params['smoothing_level']:[fcast2,fit2],
                    r'3.Simple Exponential, $\alpha=%0.2f$'%fit3.params['smoothing_level']:[fcast3,fit3],
                       },
                    'Prediction of COVID-19 Cases in Kurdistan-Region,Iraq\n Using Simple Exponential Smoothing on Daily Cases Data of March-May 2020\n',
                    'simple_models_default')
    
#    
    return [fit1,fit2,fit3]

def Train(train_data,real_data,prediction_days):

    fit1 = Holt(train_data).fit()
    fit2 = Holt(train_data,exponential=True,damped=True).fit()

   
    
    fcast1 = fit1.forecast(prediction_days)
    fcast2 = fit2.forecast(prediction_days)

    plot_time_series(
            {
                    r'Real Data':[real_data,None],
                    r'4.Additive, $\alpha=%0.2f$  &  $\beta=%0.2f$'%(fit1.params['smoothing_level'],fit1.params['smoothing_slope']):[fcast1,None],
                    r'5.Multiplicative, $\theta=%0.2f$ '%fit2.params['damping_slope']:[fcast2,None]
                    },
                    'Prediction of COVID-19 Cases in Kurdistan-Region,Iraq\n Using Holt’s Methods on Cumulative Data\n',
                    'holt_models_default')
    
    
    return [fit1,fit2]
def Test(model,real_data,prediction_days):

    fcast1 = model.forecast(prediction_days)

    plot_time_series(
            {
                    r'Real Data':[real_data,None],
                    r'6.Holt’s Method: Multiplicative, $\alpha=%0.2f$  &  $\beta=%0.2f$'%(model.params['smoothing_level'],model.params['smoothing_slope']):[fcast1,None]
                    },
                    'Prediction of COVID-19 Cumlative Cases in Kurdistan-Region,Iraq\n Using Holt’s Method with best fitted Model\n',
                    'best_model_cases')
    
    
    return fcast1

def CreateRandom (train_data,test_data,gen,plot=False):
    
    list_of_models=[]
    the_sqr_size = math.sqrt(gen)
    alpha = np.linspace(0,1,the_sqr_size)
    beta= np.linspace(0,1,the_sqr_size)
    
    optimized = True
    exponential = True

    for i in range(0,len(alpha)):
        for j in range(0,len(beta)):
            try:
                child = Holt(train_data,damped=False,exponential=exponential).fit(smoothing_level=alpha[i],smoothing_slope=beta[j],optimized=optimized)
                fcast1 = child.forecast(len(test_data))
                mse = [(fcast1[x]-test_data[x])*(fcast1[x]-test_data[x]) for x in range(0,len(test_data))]
                mse = sum(mse)/len(test_data)
                list_of_models.append({'model':child,'mse':mse})
            except:
                pass
    list_of_models.sort(key=lambda x: x['mse'], reverse=False)
    if plot:
        fig = plt.figure(figsize=(7, 5))
        ax1 = fig.add_subplot(111)
        #ax2 = fig.add_subplot(222)
        
        TOP=20
        
        colors = ['black','green','blue']
        sum_mse = max([k['mse'] for k in list_of_models[:(TOP*5)]])
        mse_plot=[k['mse']/sum_mse for k in list_of_models[:TOP]]
        sm_l=[k['model'].params['smoothing_level'] for k in list_of_models[:TOP]]
        sm_s=[k['model'].params['smoothing_slope'] for k in list_of_models[:TOP]]
        
        ax1.plot(mse_plot,color=colors[0], label='Holt\'s Model')
        ax1.scatter(range(0,TOP),sm_l,color=colors[1], label='smoothing level')
        ax1.scatter(range(0,TOP),sm_s,color=colors[2], label='smoothing slope')
    
        plt.xticks(rotation=90)
        ax1.set_title('Comparing Holt’s Methods with tuning smoothing levels and slopes\napplied on data of COVID-19 cases in September 2020, Kurdistan Region, Iraq')
        ax1.legend(loc=7)
        ax1.set_ylabel('MSE / Summation of MSE of Top %d models'%(TOP*5))
        ax1.set_xlabel('Top %d Models'%TOP)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('holts_tests.png', dpi=300)
    return list_of_models[0]

data = read_files()


daily_march = pn.Series(list(data['Total'][1][:31]), pn.date_range(start='2020-03-01', end='2020-03-31',freq='D'))
daily_april = pn.Series(list(data['Total'][1][31:61]), pn.date_range(start='2020-04-01', end='2020-04-30',freq='D'))
daily_may = pn.Series(list(data['Total'][1][61:86]), pn.date_range(start='2020-05-01', end='2020-05-25',freq='D'))
daily_march_april = pn.concat([daily_march,daily_april])
daily_actual_data= pn.concat([daily_march_april,daily_may])

rec_june = pn.Series(list(data['Total'][2][92:122]), pn.date_range(start='2020-06-01', end='2020-06-30',freq='D'))
rec_july = pn.Series(list(data['Total'][2][122:153]), pn.date_range(start='2020-07-01', end='2020-07-31',freq='D'))
rec_august = pn.Series(list(data['Total'][2][153:184]), pn.date_range(start='2020-08-01', end='2020-08-31',freq='D'))
rec_sep =pn.Series(list(data['Total'][2][184:]), pn.date_range(start='2020-09-01', end='2020-09-16',freq='D'))
rec_june_july_aug = pn.concat([rec_june,rec_july,rec_august])
rec_actual_data= pn.concat([rec_june_july_aug,rec_sep])

                           
simple_models = TrainSimple(daily_march_april,daily_actual_data,25)
holt_models = Train(rec_june_july_aug,rec_actual_data,60)
best_model = CreateRandom(rec_june_july_aug,rec_sep,6400,True)
Test(best_model['model'],rec_actual_data,60)

simple_models.extend(holt_models)
simple_models.append(best_model['model'])

params = ['smoothing_level', 'smoothing_slope', 'damping_slope', 'initial_level', 'initial_slope']
results=pn.DataFrame(index=[r'$\alpha$',r"$\beta$",r"$\phi$",r"$l_0$",r"$b_0$","SSE"] ,columns=["1", "2", "3","4'", "5", "6"])
results["1"] = [simple_models[0].params[p] for p in params] + [simple_models[0].sse]
results["2"] = [simple_models[1].params[p] for p in params] + [simple_models[1].sse]
results["3"] = [simple_models[2].params[p] for p in params] + [simple_models[2].sse]
results["4"] = [simple_models[3].params[p] for p in params] + [simple_models[3].sse]
results["5"] = [simple_models[4].params[p] for p in params] + [simple_models[4].sse]
results["6"] = [simple_models[5].params[p] for p in params] + [simple_models[5].sse]
results.to_csv('all_models_default.csv')
file1 = open("results.txt","w") 

for m in simple_models:
    file1.write(m.summary().as_text())
    file1.write("\n")
file1.close()