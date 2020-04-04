import sys
import numpy as np
import pandas as pd

def transformFluorescenceChannels(data: pd.DataFrame, channels: list, transform, inplace=False)->pd.DataFrame:
    '''Transform values in list'''
    
    if inplace:
        for channel in channels:
            data.loc[:,channel] = transform(data.loc[:,channel])
        return data
    
    else:
        output = data.copy()

        for channel in channels:
            output.loc[:,channel] = transform(data.loc[:,channel])
        return output

def autothresholdChannel(data, channel, **kwargs)->float:
    '''
    Determine a threshold of a channel by mean + n_stdevs * std or by a set percentile.
    '''
    
    #Get **kwargs
    percentile = kwargs.get('percentile', 0.999)
    n_stdevs   = kwargs.get('n_stdevs', None)
    
    if n_stdevs is not None:
        # mean + n * standard deviation method
        threshold = data[channel].mean() + n_stdevs*data[channel].std()
    
    else:
        # percentile method
        threshold = data[channel].quantile(percentile)
    
    return threshold

def autothreshold(data, channels,  **kwargs)->dict:
    '''
    threshold each channel in the list
    '''
    
    #Get **kwargs
    percentile = kwargs.get('percentile', 0.999)
    n_stdevs   = kwargs.get('n_stdevs', None)
    
    thresholds_dict = dict()
    
    for channel in channels:
        
        if n_stdevs is not None:
            # mean + n * standard deviation method
            thresholds_dict[channel] = autothresholdChannel(data, channel, n_stdevs=n_stdevs)
            
        else:
            # percentile method
            thresholds_dict[channel] = autothresholdChannel(data, channel, percentile=percentile)
            
    return thresholds_dict
    
def channelGate(data, channels, thresholds_dict):
    '''Add boolean gates for each channel in the list
    based on a dictionary of thresholds.
    '''
    
    for channel in channels:
        gate_name = channel+"+"
        
        #Add boolean gates
        data.loc[:, gate_name] = data[channel] > thresholds_dict[channel]
        #Should these modify the input or just return the booleans?
       
    return data