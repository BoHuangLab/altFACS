import sys
import numpy as np
import pandas as pd

def transformFluorescenceChannels(df: pd.DataFrame, channels: list, transform, inplace=False)->pd.DataFrame:
    '''Transform values in list'''
    
    if inplace:
        for channel in channels:
            df.loc[:,channel] = transform(df.loc[:,channel])
        return df
    
    else:
        output = df.copy()

        for channel in channels:
            output.loc[:,channel] = transform(df.loc[:,channel])
        return output

    
def autothresholdChannel(df: pd.DataFrame, channel: str, **kwargs)->float:
    '''
    Determine a threshold of a channel by mean + n_stdevs * std or by a set percentile.
    '''
    
    #Get **kwargs
    percentile = kwargs.get('percentile', 0.999)
    n_stdevs   = kwargs.get('n_stdevs', None)
    
    if n_stdevs is not None:
        # mean + n * standard deviation method
        threshold = df[channel].mean() + n_stdevs*df[channel].std()
    
    else:
        # percentile method
        threshold = df[channel].quantile(percentile)
    
    return threshold


def autothreshold(df: pd.DataFrame, channels: list,  **kwargs)->dict:
    '''
    threshold each channel in the list
    
    Parameters:
    df: pd.DataFrame
    data containing the columns for thresholding 
    
    channels: list
    A list containing the column names for thresholding 
    
    
    Optional Key Word Argument Parameters:
    percentile: float
    the percentile at which to set the threshold. This value will not be used if n_stdevs is given.
    
    n_stdevs: float
    the number of standard deviations above the mean to set the threshold.
    
    
    Returns:
    thresholds_dict: dict
    a dictionary containing the threshold for each channel in channels.
    
    '''
    
    #Get **kwargs
    percentile = kwargs.get('percentile', 0.999)
    n_stdevs   = kwargs.get('n_stdevs', None)
    
    thresholds_dict = dict()
    
    for channel in channels:
        
        if n_stdevs is not None:
            # mean + n * standard deviation method
            thresholds_dict[channel] = autothresholdChannel(df, channel, n_stdevs=n_stdevs)
            
        else:
            # percentile method
            thresholds_dict[channel] = autothresholdChannel(df, channel, percentile=percentile)
            
    return thresholds_dict


def channelGate(df: pd.DataFrame, channels: list, thresholds_dict: dict):
    '''Add boolean gates for each channel in the list
    based on a dictionary of thresholds.
    '''
    
    for channel in channels:
        gate_name = channel+"+"
        
        #Add boolean gates
        df.loc[:, gate_name] = df[channel] > thresholds_dict[channel]
        #Should these modify the input or just return the booleans?
       
    return df
