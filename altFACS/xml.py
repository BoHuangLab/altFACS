import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.colors import Normalize
from matplotlib import cm
from matplotlib.patches import Polygon
from matplotlib import path

import xml.etree.ElementTree as ET

from altFACS.density import *


def gate_to_xy(gate: ET.Element, path_to_points: str):
    
    #Check gate is polygon?
        
    x=[]
    y=[]
    
    for point in gate.findall(path_to_points):
    
        x.append(float(point.attrib['x']))
        y.append(float(point.attrib['y']))
    
    # reshape 'x and y' into a 2D array, 'xy'
    xy = np.vstack((x, y)).T
    
    return xy