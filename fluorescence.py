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

def autothresholdChannel(data, channel, percentile=0.999)->float:
    '''
    Find the 99.9th percentile of a channel.
    '''
    return data[channel].quantile(percentile)

def autothreshold(data, channels, percentile=0.999)->dict:
    '''
    threshold each channel in the list
    '''
    thresholds_dict = dict()
    
    for channel in channels:
        thresholds_dict[channel] = autothresholdChannel(data, channel, percentile)
    
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