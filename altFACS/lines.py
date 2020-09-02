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
    '''
    plot FACS with linear regression line
    
    Parameters:
    data: pd.DataFrame
    The data to be plotted and fit. 
    
    x_channel: str
    The name of the column containing the x-coordinates. 
    
    y_channel: str
    The name of the column containing the y-coordinates. 
    
    kwargs: dict
    additional arguments to be passed to the scatter plot or line plot functions.
    
    s: int
    The size of the scatter plot markers
    
    c: str
    The colour of the scatter plot markers
    
    alpha: str
    The opacity of the scatter plot markers
    
    linecolor: str
    The color of the fit line.
    
    Returns:
    slope: float
    The gradient of the linear regression
    
    intercept: float
    The value at which a linear regression would cross the y axis.
    
    r_value: float
    
    p_value: float
    
    std_err: float  
        
    
    '''
    
    linecolor = kwargs.get('linecolor', 'red')
    
    scatter_settings = {}
    scatter_settings['s']      = kwargs.get('s',2)
    scatter_settings['c']      = kwargs.get('c', 'g')
    scatter_settings['alpha']  = kwargs.get('alpha', 0.2)
    
    x = data[x_channel]
    y = data[y_channel]
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
    plt.scatter(x, y, **scatter_settings)
    
    xx = pd.Series([x.min(), x.max()])
   
    yy = xx.apply(lambda xx: slope*xx+intercept)
    
    plt.plot(xx, yy, c=linecolor);
    
    return slope, intercept, r_value, p_value, std_err
    

def rescale(y, slope:float, intercept: float):
    ''' 
    Rescale data based on parameters from a control fit
    
    
    Parameters:
    y: y values
        
    slope: float
    The slope or gradient of the line you want to normalise
    
    intercept:
    the intercept of offset of the line you want to normalise
    
    
    Returns:
    yy: 
    Rescaled or normalised y values
    '''
    
    yy = (y-intercept)/slope
    
    return yy

def rescalePlot(data, x_channel:str, y_channel:str, slope:float, intercept:float, **kwargs):
    """  
    Plot rescaled or 'normalised' y values without altering the input DataFrame.
    
    Parameters:
    data: pd.DataFrame
    
    x_channel: str
    The name of the column containing x values

    y_channel: str
    The name of the column containing y values
    
    slope: float
    The slope or gradient of the line you want to normalise
    
    intercept:
    the intercept of offset of the line you want to normalise
    
    Optional Parameters:
    s: int
    marker size
    
    c: str
    color
    
    alpha: float (0-1)
    marker transparancy
    
    x_limits: tuple (lower, upper)
    
    y_limits: tuple (lower, upper)
    
    x_label: str
    x axis label. Defaults to x_channel
       
    y_label: str
    y axis label. Defaults to y_channel
    
    diagonal_color: str
    choose the color of the diagonal line
    
    
    Returns:
    None. Just plots the graph
    
    
    """
    
    
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

def zeroSlopeFirst(df: pd.DataFrame, x: str, y: str, **kwargs):
    '''
    Fit data with a model comprised to two linear sections,
    where the first section has a fixed gradient of 0.
    
    This function is intended to fit data, where the intensity on the y axis is initially below the background.
    
    
    Parameters:
    df:
    
    x:
    
    y:
    
    Optional Parameters:
    s: int
    marker size
    
    c: str
    color
    
    alpha: float (0-1)
    marker transparancy
    
    p0: list of length 3
    
    k1_fixed: float
    Fixed gradient of the first section. Default is 0.
    
    
    Returns:
    k1_fixed:
    
    k2:
    
    x0: 
    
    e:
    error
    
    '''
    
    x=df[x]
    y=df[y]

    s     = kwargs.get('s', 2)
    c     = kwargs.get('c', 'green')
    alpha = kwargs.get('s', 0.1)

    p0       = kwargs.get('p0', [3.5, 2.5, 1])  #Initial guesses
    k1_fixed = kwargs.get('k1_fixed', 0)        #Fixed gradient   

    plt.scatter(x, y, s=s, alpha=alpha, c=c)
    plt.xlim(1,5);
    plt.ylim(1,5);
    plt.yticks([1,2,3,4,5]);

    #Set the axis to be equal
    plt.gca().set_aspect('equal');

    x = np.array(x)
    y = np.array(y)

    #Use lambda to fix the first gradient 'k1'
    k1_fixed = 0

    p , e = optimize.curve_fit(lambda x, x0, y0, k2: piecewise_linear(x, x0, y0, k1_fixed, k2), x, y, p0)

    #get parameters
    x0, y0, k2 = p

    xd = np.linspace(x.min(), x.max(), 100)

    plt.plot(xd, piecewise_linear(xd, x0, y0, k1_fixed, k2), c='r');

    return k1_fixed, k2, x0, e


def fitGated(df: pd.DataFrame, x_channel: str, y_channel: str, **kwargs):
    """
    Plot and fit data accurately despite a sharp artifical cut off.
    
    FACS data are often threshold gated, which produces a sharp artificial cut off. 
    This can generate asymmetry (which fitting algorithms expect in y, but not in x),
    which biases the linear regression. One way to overcome this issue is to swap the axis before fitting, 
    and then reverse our equation.
    
    """
    
    s         = kwargs.get('s', 2)
    c         = kwargs.get('c', 'green')
    linecolor = kwargs.get('linecolor', 'magenta')
    alpha     = kwargs.get('s', 0.1)
       
    x=df[x_channel]
    y=df[y_channel]

    plt.scatter(x, y, s=s, alpha=alpha, c=c)
    plt.xlim(1,5);
    plt.ylim(1,5);
    plt.yticks([1,2,3,4,5]);
    plt.xlabel(x_channel);
    plt.ylabel(y_channel); 

    #Set the axis to be equal
    plt.gca().set_aspect('equal');

    #Fit y against x
    slope, intercept, r_value, p_value, std_err = stats.linregress(y, x)
    
    gradient = 1/slope
    offset   = -intercept/slope

    xx = pd.Series([x.min(), x.max()])

    yy = xx.apply(lambda xx: gradient*xx+offset)

    plt.plot(xx, yy, c=linecolor);
    
    return gradient, offset, p_value, std_err


def add_slope(x, y, slope, sigfig=2, c='k'):
    
    plt.text(x, y, s='Slope = '+str(round(slope, sigfig)), c=c);