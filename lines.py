import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy import stats
from scipy import optimize

def plotFit(data, x_channel, y_channel, **kwargs):
    '''plot FACS with linear regression line'''
    
    linecolor = kwargs.get('linecolor', 'red')
    
    x = data[x_channel]
    y = data[y_channel]
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    print("slope:%f intercept:%f p_value: %f std_err:%f " % (slope, intercept, p_value, std_err))
    
    plt.scatter(x, y, **kwargs)
    
    xx = pd.Series([x.min(), x.max()])
   
    yy = xx.apply(lambda xx: slope*xx+intercept)
    
    plt.plot(xx, yy, c=linecolor);
    

def rescale(y, slope:float, intercept: float):
    ''' rescale data based on a control fit'''
    
    yy = (y-intercept)/slope
    
    return yy

def rescalePlot(data, x_channel:str, y_channel:str, slope:float, intercept:float, **kwargs):
    ''' '''
    
    
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
