# altFACS
Author: David Brown

Last Edited: 2020-August-07

## Aim:
This package is intended to standardise and simplify the investigation of protein-protein interactions by flow cytometry.

## Explanation:
In the [Huang Lab](http://huanglab.ucsf.edu/) we are interested in developing new tools to examine biological interactions. Split fluorescent proteins have proven to be a useful tool for the tagging and study of endogenous proteins in living cells, and we have been trying to maximise their utility. Appropriate use of a split fluorescent protein as a probe requires a good understanding of the complementation process, whereby the two halves of the split meet and fold to form the mature fluorescent protein. Complementation can be studied biochemically, however we can exploit the self-reporting nature of fluorescent proteins to study complementation in vivo by microscopy or or flow cytometry which offers a higher throughput. 

Flow cytometry and fluorescence activated cell sorting (FACS) are more frequently used to distinguish cell populations based on a characteristic intensity profile. In our case we often use it to study how proteins behave at a range of concentrations. This alternative approach to FACS is the main purpose of the altFACS package.

## Installation
Currently, altFACS is available on GitHub or on the [test.Pypi](https://test.pypi.org/project/altFACS/1.0.7/) site. 
Most [requirements](https://github.com/BoHuangLab/altFACS/blob/master/requirements.txt) will install automatically, but you may need to install fcsparser before installing altFACS.






