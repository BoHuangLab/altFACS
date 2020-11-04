import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from altFACS.density import densityScatterPlot

def quadCounts(df: pd.DataFrame, channel1, channel1_threshold, channel2, channel2_threshold):
    '''
    function to count and return events in each quadrant
    
    Parameters:
    df: pd.DataFrame
    Input DataFrame containing channel1 and channel2 as columns.
    
    channel1: str
    
    channel2: str
    
    
    Returns:
    double_neg:
    number of events below threshold in both channels
    
    c1_pos:
    number of events above threshold in channel1, but below threshold in channel2

    c2_pos:
    number of events below threshold in channel1, but above threshold in channel2

    double_pos:
    number of events above threshold in both channels

    '''

    #These names are not very accurate. 
    double_neg = np.logical_and(df[channel1] <= channel1_threshold, df[channel2] <= channel2_threshold).sum()
    c1_pos     = np.logical_and(df[channel1] > channel1_threshold, df[channel2] <= channel2_threshold).sum()
    c2_pos     = np.logical_and(df[channel1] <= channel1_threshold, df[channel2] > channel2_threshold).sum()
    double_pos = np.logical_and(df[channel1] > channel1_threshold, df[channel2] > channel2_threshold).sum()
    
    assert len(df) == sum([double_neg, c1_pos, c2_pos, double_pos])
    
    return double_neg, c1_pos, c2_pos, double_pos


##Quadrant plots
def quadPlot(df: pd.DataFrame, x_channel, x_channel_threshold, y_channel, y_channel_threshold, **kwargs):
    '''
    function to generate a scatter plot with the quadrants annotated
    
    Parameters:
    plot: bool 
    Default = True.
    
    ax:
    This is useful to call quadPlot as a subplot.
    
    title: str      
    What would you like to title your plot? Default = 'quadPlot_figure.pdf'.
    
    percentage: bool
    Default = True.
    
    density: bool     
    Default = True.
    
    x_limits: tuple
    (min, max). Default = (-1000,10000))
    
    y_limits:
    (min, max). Default = (-1000,10000))
    
    save: bool      
    Would you like to save the plot? Default = False.
    
    savepath: str
    Where would you like the plot saved?
    
    
    '''
    
    #Get **kwargs
    plot       = kwargs.get('plot', True)
    ax         = kwargs.get('ax', plt.gca())
    title      = kwargs.get('title', 'quadPlot_figure.pdf')
    percentage = kwargs.get('percentage', True)
    density    = kwargs.get('density', True)
    x_limits   = kwargs.get('x_limits', (-1000,10000))
    y_limits   = kwargs.get('y_limits', (-1000,10000))
    save       = kwargs.get('save', False)
    savepath   = kwargs.get('savepath', './')
    
    double_neg, c1_pos, c2_pos, double_pos = quadCounts(df, x_channel, x_channel_threshold, y_channel, y_channel_threshold)
    
    if plot==False:
        plt.ioff()
    
    if density:
        densityScatterPlot(df, x_channel, y_channel, **kwargs);
    else:
        df.plot.scatter(x=x_channel, y=y_channel, ax=ax, title=title);
        
    ax.axvline(x_channel_threshold);
    ax.axhline(y_channel_threshold);
    
    if percentage:
        total=len(df)
        dec = 2
    else:
        total=100
        dec=0
    
    #Convert to rounded percentages
    Q1 = str(np.round((c2_pos/total)*100, dec))
    Q2 = str(np.round((double_pos/total)*100, dec))
    Q3 = str(np.round((double_neg/total)*100, dec))
    Q4 = str(np.round((c1_pos/total)*100, dec))

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