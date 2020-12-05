import unittest

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# from ..altFACS.contours import *
from altFACS.contours import *

#Define fixings
seed=5
np.random.seed(seed) #set the seed to make a stable test

x = np.random.normal(0,1,100)
y = np.random.normal(0,1,100)

test_df = pd.DataFrame()
test_df['x'] = x
test_df['y'] = y

class TestContours(unittest.TestCase):

    def test_getContours_gives_poly(self):
        """The getContours functions should return a matplotlib.patches.Polygon"""

        poly = getContours(test_df, x='x', y='y')
        self.assertIsInstance(poly, Polygon), "getContours should return a matplotlib.patches.Polygon"
    
if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
