import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from ..altFACS.contours import *

def test_getContours_gives_poly():
    """The getContours functions should return a matplotlib.patches.Polygon"""

    x = np.arange(1, 10)
    y = x.reshape(-1, 1)
    h = x * y

    cs = plt.contourf(h, levels=[10, 30, 50],
        colors=['#808080', '#A0A0A0', '#C0C0C0'], extend='both')
    cs.cmap.set_over('red')
    cs.cmap.set_under('blue')
    cs.changed()
    
    #Define the contour and population of interest
    contour=1
    population=0

    #Extract desired contour
    coords = cs.allsegs[contour][population]

    #Convert to a list
    coord_list=list()
    for point in coords:
        coord_list.append([point[0], point[1]])
    coord_list

    #Convert to an array
    coord_array = np.array(coord_list)

    #Pull out coordinates
    xp = coord_array.T[0]
    yp = coord_array.T[1]

    #Define polygon
    poly = Polygon(np.column_stack([xp, yp]), fill=False)

    assert isinstance(poly, Polygon), "getContours should return a matplotlib.patches.Polygon"
    
if __name__ == "__main__":
    test_getContours_gives_poly()
    print("Everything passed")
