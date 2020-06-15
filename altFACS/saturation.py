import sys
import pandas as pd

# Mask channel
def maskChannelSaturation(df: pd.DataFrame, channel: str, lower: float, upper: float)-> pd.DataFrame:
    """
    replace channel values below lower or above upper with NaN
    
    Parameters:
    df: pd.DataFrame
    data containing the column to be masked 
    
    channel: str
    the name of the column to be masked 
    
    lower: float
    the threshold below which, values will be replaced with NaN.
    
    upper: float
    the threshold above which, values will be replaced with NaN.
    
    Returns:
    mask: pd.DataFrame
    a dataframe like df except with values in df[channel] outside lower and upper replace with NaN.
    values are not removed so mask.shape == df.shape.
    
    """

    # Is the value above the lower threshold?  
    return df[channel].mask(~df[channel].between(lower, upper, inclusive = False))


# Iterate through channels
def maskSaturation(df: pd.DataFrame, limit_dict: dict, **kwargs):
    '''replace values outside channel limits with NaN'''
    
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
    '''tag events with values outside channel limits by adding a boolean 'Saturated' column to the DataFrame.'''
    
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
    '''make a limit_dictionary from a list of channels'''
    
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