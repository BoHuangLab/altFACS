import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from altFACS.saturation  import *
from altFACS.contours import *
from altFACS.singlets import *

def processExperiment(experiment: pd.DataFrame, limit_dict: dict, polygon: matplotlib.patches.Polygon, singlet_threshold: float):
    '''
    remove saturation, gate event scattering based on a supplied polygon and eliminate doublet events
    
    Parameters:
    experiment: pd.DataFrame
    
    limit_dict: dict
    A dictionary of lower and upper values for each channel.
    
    polygon: matplotlib.patches.Polygon
    
    singlet_threshold: float
    The FSC-H / FSC-A threshold above which events are considered singlet. Returned by processControl() or singletThreshold()
    
    
    Returns:
    singlets: pd.DataFrame
    A subset of the input experiment dataframe, limited to singlet events.
    
    '''
    
    #[1] Remove saturation
    mask = maskSaturation(experiment, limit_dict)
    unsaturated = mask.dropna()
    
    #[2] Scatter gate
    scatterGate(unsaturated, polygon)
    
    #[3] Singlet gate
    singlets = singletGate(unsaturated, singlet_threshold)
    
    #[4] Limit to singlets
    singlets = singlets[singlets['Scatter+'] & singlets['Singlet+']].copy()
    
    return singlets