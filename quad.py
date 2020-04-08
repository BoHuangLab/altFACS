import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from alternativeFACS.alternativeFACS.helpers.density import densityScatterPlot

def quadCounts(df, channel1, channel1_threshold, channel2, channel2_threshold):
    '''function to count and return events in each quadrant'''

    double_neg = np.logical_and(df[channel1] <= channel1_threshold, df[channel2] <= channel2_threshold).sum()
    c1_pos     = np.logical_and(df[channel1] > channel1_threshold, df[channel2] <= channel2_threshold).sum()
    c2_pos     = np.logical_and(df[channel1] <= channel1_threshold, df[channel2] > channel2_threshold).sum()
    double_pos = np.logical_and(df[channel1] > channel1_threshold, df[channel2] > channel2_threshold).sum()
    
    assert len(df) == sum([double_neg, c1_pos, c2_pos, double_pos])
    
    return double_neg, c1_pos, c2_pos, double_pos

##Quadrant plots
def quadPlot(data, x_channel, x_channel_threshold, y_channel, y_channel_threshold, **kwargs):
    '''function to generate a scatter plot with the quadrants annotated'''
    
    #Get **kwargs
    plot       = kwargs.get('plot', True)
    title      = kwargs.get('title', 'quadPlot_figure.pdf')
    percentage = kwargs.get('percentage', True)
    density    = kwargs.get('density', True)
    x_limits   = kwargs.get('x_limits', (-1000,10000))
    y_limits   = kwargs.get('y_limits', (-1000,10000))
    save       = kwargs.get('save', False)
    savepath   = kwargs.get('savepath', './')
    
    double_neg, c1_pos, c2_pos, double_pos = quadCounts(data, x_channel, x_channel_threshold, y_channel, y_channel_threshold)
    
    if plot==False:
        plt.ioff()
    
    if density:
        densityScatterPlot(data, x_channel, y_channel);
    else:
        data.plot.scatter(x=x_channel, y=y_channel);
        
    plt.axvline(x_channel_threshold, y_limits[0], y_limits[1]);
    plt.axhline(y_channel_threshold, x_limits[0], x_limits[1]);
    plt.xlim(x_limits)
    plt.ylim(y_limits)
    
    if percentage:
        total=len(data)
        dec = 2
    else:
        total=100
        dec=0
    
    Q1 = str(np.round((c2_pos/total)*100, dec))
    Q2 = str(np.round((double_pos/total)*100, dec))
    Q3 = str(np.round((double_neg/total)*100, dec))
    Q4 = str(np.round((c1_pos/total)*100, dec))

    ax=plt.gca()
    plt.text(0.01,0.99, 'Q1: '+Q1, transform=ax.transAxes, verticalalignment='top');
    plt.text(0.99,0.99, 'Q2: '+Q2, transform=ax.transAxes, horizontalalignment='right', verticalalignment='top');
    plt.text(0.01,0.01, 'Q3: '+Q3, transform=ax.transAxes);
    plt.text(0.99,0.01, 'Q4: '+Q4, transform=ax.transAxes, horizontalalignment='right');
    
    if save:
        plt.savefig(savepath+title)
    
    if plot==False:
        plt.close()
    
    #Restore interactive plotting
    plt.ion()