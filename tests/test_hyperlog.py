import unittest

import numpy as np

from ..altFACS.hyperlog import *

#Define fixings (input data)
test_array = np.array([-100, -10, -1, 0, 1, 10, 100, 1000, 10000])

hlog_result = np.array([-3.66959885e+02, -3.67371939e+01, -3.67407265e+00,  0.00000000e+00,
                        3.67407265e+00,  3.67371939e+01,  3.66959885e+02,  3.42866112e+03,
                        7.20802323e+03])

#How accurate should equalities be
places = None
delta  = 0.0001 #use delta rather than places as we are dealing wiht log scales.

class TestHyperlog(unittest.TestCase):
    
    def test_hlog(self):
        #Test the default behaviour of hlog is as expected
        for n in range(len(test_array)):
            self.assertAlmostEqual(hlog_result[n], hlog(test_array[n]), places, "Default parameters should give this expected result.", delta) 
        
if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)