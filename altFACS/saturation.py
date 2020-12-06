import sys
import pandas as pd

# Mask channel
def maskChannelSaturation(df: pd.DataFrame, channel: str, lower: float, upper: float)-> pd.DataFrame:
    """
    Replace channel values below lower or above upper with NaN.
  
    Parameters:
    df: pd.DataFrame
    FACS data containing the column to be masked. 
    
    channel: str
    the name of the column to be masked. 
    
    lower: float
    the threshold below which, values will be replaced with NaN.
    
    upper: float
    the threshold above which, values will be replaced with NaN.
    
    Returns:
    mask: pd.DataFrame
    a dataframe like df except with values in df[channel] outside lower and upper replaced with NaN.
    values are not removed so mask.shape == df.shape.
    
    """

    # Is the value above the lower threshold?  
    return df[channel].mask(~df[channel].between(lower, upper, inclusive = False))


# Iterate through channels
def maskSaturation(df: pd.DataFrame, limit_dict: dict, **kwargs):
    '''
    Replace values outside channel limits with NaN.
    
    Parameters:
    df: pd.DataFrame
    FACS data containing the columns to be masked.
    
    limit_dict: dict
    A dictionary defining the minimum and maximum values for each channels. 
    This will be used to remove saturation, by excluding events outside this set of limits.
    Events outside the limits in any channel will be excluded from further analysis in all channels.
    
    Optional Parameters:
    verbose: bool (Deafult True)
    Print input events, and unsaturated events?
    
    
    Returns:
    mask: pd.DataFrame
    A dataframe like df except with values outside limit_dict replaced with NaN.
    Values are not removed so mask.shape == df.shape.
    
    '''
    
    # Get **kwargs
    verbose     = kwargs.get('verbose', True)
    
    if verbose:
        print('Input events =', len(df))

    # Use pd.DataFrame.copy() otherwise you will generate a view which will get overwritten
    mask = df.copy()

    for channel in df.columns:
        if channel in limit_dict.keys():
        
            if verbose:
                print('Removing',channel, 'saturation')

            # Retrive channel specific limits from dictionary
            lower = limit_dict[channel]['lower_limit']
            upper = limit_dict[channel]['upper_limit']

            # Mask events not between the upper and lower limits
            mask[channel] = maskChannelSaturation(mask, channel, lower, upper)
    
    if verbose:
        print('Unsaturated events =', len(mask.dropna()))

    return mask


def tagSaturation(df: pd.DataFrame, limit_dict: dict, **kwargs):
    '''
    Tag events with values outside channel limits by adding a boolean 'Saturated' column to the DataFrame.
    
    Parameters:
    df: pd.DataFrame
    FACS data containing the columns to be masked.
    
    limit_dict: dict
    A dictionary defining the minimum and maximum values for each channels. 
    This will be used to remove saturation, by excluding events outside this set of limits.
    Events outside the limits in any channel will be excluded from further analysis in all channels.
    
    
    Optional Parameters:
    verbose: bool (Deafult True)
    Print input events, and unsaturated events?
    
    
    Returns:
    df: pd.DataFrame
    FACS data with a new boolean column 'Saturated'.
    
    '''
    
    # Get **kwargs
    verbose     = kwargs.get('verbose', False)
    
    if verbose:
        print('Input events =', len(df))
        
    # Use pd.DataFrame.copy() otherwise you will generate a view which will get overwritten
    saturated = df.copy()

    channels = list(limit_dict.keys())

    #For each channel is event within limits?
    for channel in df.columns:
        if channel in channels:

            # Retrive channel specific limits from dictionary
            lower = limit_dict[channel]['lower_limit']
            upper = limit_dict[channel]['upper_limit']

            # Identify saturation in each channel
            saturated[channel] = ~df[channel].between(lower, upper, inclusive = False)

            # tag events with saturation in one or more channels
            df.loc[:, 'Saturated'] = saturated.loc[:,saturated.columns.isin(channels)].any(axis=1)

    return df


def makeLimitDict(channels: list, **kwargs):
    '''
    Make a limit_dictionary from a list of channels.
    
    Parameters:
    channels: list
    
    lower_limit: float
    
    upper_limit: float
    
    
    Returns:
    limit_dict: dict
    A dictionary defining the minimum and maximum values for each channels. 
    This will be used to remove saturation, by excluding events outside this set of limits.
    Events outside the limits in any channel will be excluded from further analysis in all channels.
    
    '''
    
    # Get **kwargs
    verbose     = kwargs.get('verbose', False)
    lower_limit = kwargs.get('lower_limit', 0)
    upper_limit = kwargs.get('upper_limit', 262143.0)
    
    #Initialise dictionary
    limit_dict=dict()

    #For each channel is event within limits?
    for channel in channels:
        
        if verbose:
            print('Generating limts for ', channel)

        # Set channel specific limits
        limit_dict[channel]= {'lower_limit': lower_limit, 'upper_limit': upper_limit}

    return limit_dict