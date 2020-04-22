"""
Lines

The Huang Lab uses flow cytometry to investigate interactions between split fluorescent protein fragments. 
This module contains functions to scale and fit FACS data.

Functions:
plotFit          -
rescale          - 
rescalePlot      -
piecewise_linear -
fitGated         - 

Requirements:
numpy
pandas
matplotlib
scipy

"""

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy import stats
from scipy import optimize

def plotFit(data, x_channel, y_channel, **kwargs):
    '''plot FACS with linear regression line'''
    
    linecolor = kwargs.get('linecolor', 'red')
    
    scatter_settings = {}
    scatter_settings['s']      = kwargs.get('s',2)
    scatter_settings['c']      = kwargs.get('c', 'g')
    scatter_settings['alpha']  = kwargs.get('alpha', 0.2)
    
    x = data[x_channel]
    y = data[y_channel]
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    print("slope:%f intercept:%f p_value: %f std_err:%f " % (slope, intercept, p_value, std_err))
    
    plt.scatter(x, y, **scatter_settings)
    
    xx = pd.Series([x.min(), x.max()])
   
    yy = xx.apply(lambda xx: slope*xx+intercept)
    
    plt.plot(xx, yy, c=linecolor);
    

def rescale(y, slope:float, intercept: float):
    ''' rescale data based on a control fit'''
    
    yy = (y-intercept)/slope
    
    return yy

def rescalePlot(data, x_channel:str, y_channel:str, slope:float, intercept:float, **kwargs):
    """  """
    
    
    x = data[x_channel]
    y = data[y_channel]
    yy = rescale(y, slope, intercept)
    
    scatter_settings = {}
    scatter_settings['s']      = kwargs.get('s',2)
    scatter_settings['c']      = kwargs.get('c', 'g')
    scatter_settings['alpha']  = kwargs.get('alpha', 0.2)
    
    x_limits = kwargs.get('x_limits', (1,5))
    y_limits = kwargs.get('y_limits', (1,5))
    x_label  = kwargs.get('x_label', x_channel)
    y_label  = kwargs.get('y_label', y_channel+' - normalized')
    
    diagonal_color = kwargs.get('linecolor', 'k')
    
    #Plot the scatter plot
    plt.scatter(x, yy, **scatter_settings);
    plt.xlim(*x_limits);
    plt.ylim(*y_limits);
    plt.xlabel(x_label);
    plt.ylabel(y_label);
    
    #Set the axis to be equal
    plt.gca().set_aspect('equal');
    
    #Add diagonal line
    plt.plot(x_limits, y_limits, c=diagonal_color);
    
    plt.yticks([1,2,3,4,5]); 


def piecewise_linear(x, x0, y0, k1, k2):
    return np.piecewise(x, [x < x0], [lambda x:k1*x + y0-k1*x0, lambda x:k2*x + y0-k2*x0])

def fitGated(data, x_channel, y_channel):
    '''this function allows y_gated data to be fitted accurately
    
    Along the lines of the strategy employed in our split-sfCherry3 paper.
    https://static-content.springer.com/esm/art%3A10.1038%2Fs42003-019-0589-x/MediaObjects/42003_2019_589_MOESM1_ESM.pdf
    '''
    
    x=data[x_channel]
    y=data[y_channel]

    plt.scatter(x, y, s=2, alpha=0.3, c='green')
    plt.xlim(1,5);
    plt.ylim(1,5);
    plt.yticks([1,2,3,4,5]);
    plt.xlabel(x_channel);
    plt.ylabel(y_channel); 

    #Set the axis to be equal
    plt.gca().set_aspect('equal');

    #Fit y against x
    slope, intercept, r_value, p_value, std_err = stats.linregress(y, x)
    #In this case both slope and intercept are fitted parameters.
    
    gradient = 1/slope
    offset   = -intercept/slope
    
    print("slope:%f intercept:%f p_value: %f std_err:%f " % (gradient, offset, p_value, std_err))

    xx = pd.Series([x.min(), x.max()])

    yy = xx.apply(lambda xx: gradient*xx+offset)

    plt.plot(xx, yy, c='red');
    #plt.title(file_info.loc[file_num, 'Description']);
